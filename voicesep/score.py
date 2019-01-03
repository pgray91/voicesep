from fractions import Fraction as F
import logging
import music21 as m21
import random

from voicesep.chord import Chord
from voicesep.note import Note
from voicesep.voice import Voice

logger = logging.getLogger(__name__)


class Score:

    QUARTER = 4
    MIDDLE_C = 60

    def __init__(self, name, sheet):

        self.name = name
        logger.info("{} | initializing".format(self.name))

        self.score = m21.converter.parse(sheet)
        self.chords = []

        denomination = 0
        scale = None

        onset_origin = F()
        ql_origin = F()

        tie_map = {}

        measures = self.score.semiFlat.getElementsByClass("Measure").stream()
        measure_groups = map(
            m21.stream.Stream,
            m21.stream.iterator.OffsetIterator(measures)
        )
        for measure_index, measure_group in enumerate(measure_groups, start=1):
            top_measure = measure_group[0]

            if top_measure.getElementsByClass("TimeSignature"):
                logger.debug("m{} | changing time signature".format(measure_index))

                ql_distance = top_measure.offset - ql_origin

                onset_origin += ql_distance * denomination / Score.QUARTER
                ql_origin = F(top_measure.offset)

                timesig = top_measure.getElementsByClass("TimeSignature")[0]
                denomination = timesig.denominator

            if top_measure.getElementsByClass("KeySignature"):
                logger.debug("m{} | changing key signature".format(measure_index))

                keysig = top_measure.getElementsByClass("KeySignature")[0]
                scale = keysig.getScale()

            chords = measure_group.flat.notes.stream()
            chord_groups = m21.stream.iterator.OffsetIterator(chords)
            for chord_index, chord_group in enumerate(chord_groups, start=1):
                top_chord = chord_group[0]

                ql_distance = top_chord.offset - ql_origin

                onset = onset_origin + ql_distance * denomination / Score.QUARTER
                beat = top_chord.beat

                notes = []
                for chord_part in chord_group:
                    if chord_part.duration.isGrace:
                        continue

                    note_group = chord_part if chord_part.isChord else [chord_part]

                    has_staccato = any(
                        articulation.name == "staccato"
                        for articulation in chord_part.articulations
                    )

                    lyrics = [lyric.text.split(",") for lyric in chord_part.lyrics]

                    chord_stepper = m21.chord.Chord(note_group)
          
                    for note_index, note_part in enumerate(reversed(note_group)):

                        ql_duration = F(note_part.duration.quarterLength)
                        if has_staccato:
                            ql_duration *= 0.5

                        duration = ql_duration * denomination / Score.QUARTER
                        offset = onset + duration

                        if note_part.tie and note_part.tie.type != "start":
                            note = tie_map[note_part.pitch.ps]
                            logger.debug("{} | adjusting tied duration".format(note))

                            note.duration += duration
                            note.offset += duration
                            continue

                        degree = scale.getScaleDegreeFromPitch(
                            note_part.name, comparisonAttribute="step"
                        )

                        for chord_degree in range(1, 8):
                            chord_step = chord_stepper.getChordStep(chord_degree)

                            if not chord_step:
                                continue

                            if chord_step.step == note_part.step:
                                break

                        lyric = lyrics[note_index] if lyrics else []
                        color = note_part.style.color

                        note = Note(
                            name=note_part.name,
                            octave=note_part.octave,
                            location=(measure_index, chord_index),

                            pitch=int(note_part.pitch.ps),

                            onset=onset,
                            duration=duration,
                            offset=offset,

                            index=len(notes),

                            degree=degree,
                            chord_degree=chord_degree,

                            lyric=lyric,
                            color=color
                        )
                        notes.append(note)

                        if note_part.tie:
                            logger.debug("{} | inserting into tie map".format(note))
                            tie_map[note_part.pitch.ps] = note

                if len(notes) == 0:
                    continue

                chord = Chord(
                    notes,

                    onset=onset,

                    index=len(self.chords),

                    beat=beat
                )
                self.chords.append(chord)

    # def write(self, sheet, assignments):
    #
    #     logger.info("{} | {} | writing assignments to file".format(self.name, sheet))
    #
    #     rint = lambda: random.randint(0,255)
    #     lyric_map = {}
    #     color_map = {}
    #     tie_map = {}
    #     lyric_index = 1
    #
    #     chord_index = 0
    #     chords = self.score.flat.notes.stream()
    #     chord_groups = chords.groupElementsByOffset()
    #     for chord_group in chord_groups:
    #
    #         note_index = 0
    #         for chord_part in chord_group:
    #             if chord_part.duration.isGrace:
    #                 continue
    #
    #             assignment = assignments[chord_index]
    #             show_lyrics = False
    #             lyrics = []
    #
    #             note_group = chord_part if chord_part.isChord else [chord_part]
    #
    #             for note_part in sorted(note_group, reverse=True):
    #
    #                 if note_part.tie and note_part.tie.type != "start":
    #
    #                     note_part.color = tie_map[note_part.pitch.ps]
    #                     lyrics.append("X")
    #                     continue
    #
    #                 voice = assignment[note_index]
    #                 note_index += 1
    #
    #                 note_lyric = []
    #
    #                 if len(voice.left) == 0:
    #
    #                     note_lyric.append(lyric_index)
    #                     lyric_index += 1
    #
    #                 for left_voice in voice.left:
    #
    #                     note_lyric.append(
    #                       lyric_map[left_voice][left_voice.right.index(voice)]
    #                     )
    #
    #                 for _ in range(len(note_lyric), len(voice.right)):
    #
    #                     note_lyric.append(lyric_index)
    #                     lyric_index += 1
    #
    #                 lyric_map[voice] = note_lyric
    #
    #                 note_part.color = color_map.setdefault(
    #                     note_lyric[0], "#{:02X}#{:02X}#{:02X}".format(
    #                         rint(), rint(), rint()
    #                     )
    #                 )
    #                 if note_part.tie:
    #                     tie_map[note_part.pitch.ps] = note_part.color
    #
    #                 show_lyrics = show_lyrics or (
    #                   len(converged) != 1 or
    #                   len(diverged) > 1 or
    #                   len(converged[0].diverged(voiceid)) > 1 or
    #                   (len(diverged) == 1 and len(diverged[0].converged(voiced)) > 1)
    #                 )
    #
    #                 lyrics.append(",".join(lyric for lyric in note_lyric))
    #
    #           if show_lyrics:
    #               map(chord_part.addLyric, lyrics)
    #
    #         chord_index += note_index > 0
    #
    #     self.score.write(fp=sheet)
    #
    def __len__(self):
        return len(self.chords)

    def __getitem__(self, index):
        return self.chords[index]

    def __iter__(self):
        return iter(self.chords)
