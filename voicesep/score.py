import logging
import music21 as m21
import os
import random

from fractions import Fraction as F

from voicesep.chord import Chord
from voicesep.note import Note

logger = logging.getLogger(__name__)


class Score:

    QUARTER = 4
    MIDDLE_C = 60

    def __init__(self, sheet):

        self.name = os.path.splitext(os.path.basename(sheet))[0]
        logger.debug(f"{self.name} | initializing")

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
                logger.debug(f"m{measure_index} | changing time signature")

                ql_distance = top_measure.offset - ql_origin

                onset_origin += ql_distance * denomination / Score.QUARTER
                ql_origin = F(top_measure.offset)

                timesig = top_measure.getElementsByClass("TimeSignature")[0]
                denomination = timesig.denominator

            if top_measure.getElementsByClass("KeySignature"):
                logger.debug(f"m{measure_index} | changing key signature")

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

                    for part_index, note_part in enumerate(reversed(note_group)):

                        ql_duration = F(note_part.duration.quarterLength)
                        if has_staccato:
                            ql_duration *= 0.5

                        duration = ql_duration * denomination / Score.QUARTER
                        offset = onset + duration

                        if note_part.tie and note_part.tie.type != "start":
                            note = tie_map[note_part.pitch.ps]
                            logger.debug(f"{note} | adjusting tied duration")

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

                        lyric = lyrics[part_index] if lyrics else []
                        color = note_part.style.color

                        note = Note(
                            name=note_part.name,
                            octave=note_part.octave,
                            location=(measure_index, chord_index),

                            onset=onset,
                            duration=duration,
                            offset=offset,

                            index=-1,

                            degree=degree,
                            chord_degree=chord_degree,

                            lyric=lyric,
                            color=color
                        )
                        notes.append(note)

                        if note_part.tie:
                            logger.debug(f"{note} | inserting into tie map")
                            tie_map[note_part.pitch.ps] = note

                if len(notes) == 0:
                    continue

                notes.sort(reverse=True)
                for i, note in enumerate(notes):
                    note.index = i

                chord = Chord(
                    notes,

                    onset=onset,

                    index=len(self.chords),

                    beat=beat
                )
                self.chords.append(chord)

    def write(self, sheet, assignments):

        logger.info(f"name={self.name}, sheet={sheet} | writing")

        rgb = lambda: "".join(f"{random.randint(0,255):02x}".upper() for _ in range(3))
        lyric_map = {}
        color_map = {}
        tie_map = {}
        lyric_index = 1

        chord_index = 0
        chords = self.score.flat.notes.stream()
        chord_groups = m21.stream.iterator.OffsetIterator(chords)
        for chord_group in chord_groups:

            for chord_part in chord_group:
                if chord_part.duration.isGrace:
                    continue

                note_group = chord_part if chord_part.isChord else [chord_part]
                tied = all(
                    note_part.tie and note_part.tie.type != "start"
                    for note_part in note_group
                )
                if not tied:
                    break
            else:
                continue

            note_parts = []
            for chord_part in chord_group:
                if chord_part.duration.isGrace:
                    continue

                chord_part.lyric = ""

                note_group = chord_part if chord_part.isChord else [chord_part]
                for note_part in note_group:
                    note_parts.append(note_part)

            note_parts.sort(key=lambda note_part: note_part.pitch.ps, reverse=True)

            assignment = assignments[chord_index]

            lyrics = [[] for _ in range(len(note_parts))]
            note_index = 0
            for lyric, note_part in zip(lyrics, note_parts):

                if note_part.tie and note_part.tie.type != "start":
                    note_part.style.color = tie_map[note_part.pitch.ps]
                    lyric.append("X")
                    continue

                if note_part.tie:
                    tie_map[note_part.pitch.ps] = note_part.style.color

                voice = assignment[note_index]
                note_index += 1

                if len(voice.left) == 0:

                    lyric.append(str(lyric_index))
                    lyric_index += 1

                else:
                    left_voices = sorted(voice.left, reverse=True)
                    for left_voice in left_voices:
                        right_voices = sorted(voice.right, reverse=True)

                        # if left voice only connects to you
                        left_lyric = lyric_map[left_voice]
                        lyric.append(
                            left_lyric[
                                sorted(
                                    left_voice.right,
                                    key=lambda v: v.note.pitch,
                                    reverse=True
                                ).index(voice)
                            ]
                        )

                for _ in range(len(lyric), len(voice.right)):

                    lyric.append(str(lyric_index))
                    lyric_index += 1

                lyric_map[voice] = lyric

                note_part.style.color = color_map.setdefault(lyric[0], f"#{rgb()}")

            for chord_part in chord_group:
                if chord_part.duration.isGrace:
                    continue

                note_group = chord_part if chord_part.isChord else [chord_part]

                note_index = 0
                for note_part in note_parts:
                    if note_part.tie and note_part.tie.type != "start":
                        continue

                    voice = assignment[note_index]
                    note_index += 1

                    if note_part not in note_group:
                        continue

                    show = (
                        len(voice.left) != 1 or
                        len(voice.right) > 1 or
                        any(
                            len(left_voice.right) > 1
                            for left_voice in voice.left
                        ) or
                        any(
                            len(right_voice.left) > 1
                            for right_voice in voice.right
                        )
                    )
                    if show:
                        break

                else:
                    continue

                for note_part in reversed(note_group):
                    lyric = lyrics[note_parts.index(note_part)]
                    chord_part.addLyric(",".join(lyric))

            chord_index += 1

        self.score.write(fp=sheet)

    def __len__(self):
        return len(self.chords)

    def __getitem__(self, index):
        return self.chords[index]

    def __iter__(self):
        return iter(self.chords)
