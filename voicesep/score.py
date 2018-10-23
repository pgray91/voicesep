from   fractions import Fraction as F
import logging
import music21 as m21
import random

logger = logging.getLogger(__name__)

# log.conf
# User can set logging specifications at root level
# In logging, add time - level - file name.function name.lline number | Score.mMeasure.cChord.nNote | Message

# Split unittests into score, chord, note, voice
# Test b

# Verify pitch is in scale
# verify lyrics and color

class Score:

    QUARTER = 4

    def __init__(self, name, score):

        self.name = name
        logger.info("{} | initializing".format(self.name))

        self.score = m21.converter.parse(score)

        self.chords = []

        timesig = self.score.flat.getElementsByClass("TimeSignature")[0]
        keysig = self.score.flat.getElementsByClass("KeySignature")[0]
        scale = keysig.getScale()

        onset_origin = F()
        ql_origin = F()

        tie_map = {}

        measures = self.score.semiFlat.getElementsByClass("Measure").stream()
        measure_groups = [
            m21.stream.Stream(measure_group)
            for measure_group in measures.groupElementsByOffset()
        ]
        for measure_index, measure_group in enumerate(measure_groups):
            top_measure = measure_group[0]

            if top_measure.getElementsByClass("TimeSignature"):
                logger.debug("m{} | changing time signature".format(measure_index))

                ql_distance = top_measure.offset - ql_origin

                onset_origin += ql_distance * timesig.denominator / Score.QUARTER
                ql_origin = F(top_measure.offset)

                timesig = top_measure.getElementsByClass("TimeSignature")[0]

            if top_measure.getElementsByClass("KeySignature"):
                logger.debug("m{} | changing key signature".format(measure_index))

                keysig = top_measure.getElementsByClass("KeySignature")[0]
                scale = keysig.getScale()

            chords = measure_group.flat.notes.stream()
            chord_groups = chords.groupElementsByOffset()
            for chord_index, chord_group in enumerate(chords_groups):
                top_chord = chord_group[0]

                ql_distance = top_chord.offset - ql_origin

                onset = onset_origin + ql_distance * timesig.denominator / Score.QUARTER
                beat = top_chord.beat

                notes = []
                for chord_part in chord_group:
                    if chord_part.duration.isGrace:
                        continue

                    note_group = chord_part if chord_part.isChord else [chord_part]

                    lyrics = [lyric.split(",") for lyric in chord_part.lyrics]

                    has_staccato = any( 
                        any(
                            articulation.name == "staccato"
                            for articulation in note_part.articulations
                        )
                        for note_part in [note_group[0], note_group[-1]]
                    )

                    chord_stepper = m21.chord.Chord(note_group)
          
                    for note_index, note_part in enumerate(reversed(note_group)):

                        ql_duration = F(note_part.duration.quarterLength)
                        if has_staccato:
                            ql_duration *= 0.5

                        duration = ql_duration * timesig.denominator / Score.QUARTER
                        offset = onset + duration

                        if note.tie and note.tie.type != "start":
                            note = tie_map[note_part.pitch.ps]
                            logger.debug("{} | adjusting tied duration".format(note))

                            note.duration += duration
                            note.offset += duration
                            continue

                        degree = scale.getScaleDegreeFromPitch(
                            note_part.name, comparisonAttribute="step"
                        )

                        for chord_step in map(chord_stepper.getChordStep, range(1,8)):
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

                            pitch=int(note.pitch.ps),

                            duration=duration,
                            offset=offset,

                            index=len(chord) - 1,

                            degree=degree,
                            chord_step=chord_step,

                            lyric=lyric,
                            color=color
                        )
                        notes.append(note)

                        if note_part.tie:
                            logger.debug("{} | inserting into tie map".format(note))
                            tie_map[note_part.pitch.ps] = note

                chord = Chord(
                    notes,

                    onset=onset,

                    index=len(self.chords) - 1,

                    # BRNG BACK BEAT STRENGTH
                    beat=beat
                )


    def separate(self, one_to_many):

        logger.info(
            "{} | one to {} | separating true voices".format(
                self.name, "many" if one_to_many else "one"
            )
        )

        assignments = []

        voice_map = {}
        voiceid_map = {}

        for chord in self.chords:
            assignment = []

            for note in chord:
                voice = Voice(note)

                if one_to_many:
                    if len(note.lyric) > 0:
                        voiceids = note.lyric
                        voiceid_map[note.color] = voiceids

                    else:
                        voiceids = voiceid_map[note.color]

                else:
                    voiceids = [note.color]

                for voiceid in voiceids:
                    if voiceid in voice_map:
                        left_voice = voice_map[voiceid]
                        if left_voice not in voice.left:
                            voice.left.append(left_voice)
                            left_voice.right.append(voice)

                    voice_map[voiceid] = voice

                assignment.append(voice)

            assignments.append(assignment)

        return assignments

    def write(self, score_file, assignments):

        logger.info("{} | {} | writing assignments to file".format(self.name, score_file))

        rint = lambda: random.randint(0,255)
        lyric_map = {}
        color_map = {}
        tie_map = {}
        lyric_index = 1

        chord_index = 0
        chords = self.score.flat.notes.stream()
        chord_groups = chords.groupElementsByOffset()
        for chord_group in chord_groups:

            note_index = 0
            for chord_part in chord_group:
                if chord_part.duration.isGrace:
                    continue

                assignment = assignments[chord_index]
                show_lyrics = False
                lyrics = []

                note_group = chord_part if chord_part.isChord else [chord_part]

                for note_part in sorted(note_group, reverse=True):

                    if note_part.tie and note_part.tie.type != "start":

                        note_part.color = tie_map[note_part.pitch.ps]
                        lyrics.append("X")
                        continue

                    voice = assignment[note_index]
                    note_index += 1

                    note_lyric = []

                    if len(voice.left) == 0:

                        note_lyric.append(lyric_index)
                        lyric_index += 1

                    for left_voice in voice.left:

                        note_lyric.append(
                          lyric_map[left_voice][left_voice.right.index(voice)]
                        )

                    for _ in range(len(note_lyric), len(voice.right)):

                        note_lyric.append(lyric_index)
                        lyric_index += 1

                    lyric_map[voice] = note_lyric

                    note_part.color = color_map.setdefault(
                        note_lyric[0], "#{:02X}#{:02X}#{:02X}".format(
                            rint(), rint(), rint()
                        )
                    )
                    if note_part.tie:
                        tie_map[note_part.pitch.ps] = note_part.color

                    show_lyrics = show_lyrics or (
                      len(converged) != 1 or
                      len(diverged) > 1 or
                      len(converged[0].diverged(voiceid)) > 1 or
                      (len(diverged) == 1 and len(diverged[0].converged(voiced)) > 1)
                    )

                    lyrics.append(",".join(lyric for lyric in note_lyric))

              if show_lyrics:
                  map(chord_part.addLyric, lyrics)

            chord_index += note_index > 0

        self.score.write(fp=score_file)

    def __len__(self):
        return len(self.chords)

    def __getitem__(self, index):
        return self.chords[index]

    def __iter__(self):
        return iter(self.chords)

class Chord:

    def __init__(self, notes, **kwargs):

        self.notes = notes
        # assert all of note type

        for key, value in kwargs.items():
            setattr(self, key, value)

        logger.debug("{} | initializing chord".format(self))


    def __len__(self):

        return len(self.notes)

    def __getitem__(self, index):

        return self.notes[index]

    def __iter__(self):

        return iter(self.notes)

    def __str__(self):

        return "Chord({})".format(", ".join(self.notes))

class Note:

    def __init__(self, name, octave, location, **kwargs):

        self.name = name
        self.octave = octave
        self.location = location

        for key, value in kwargs.items():
            setattr(self, key, value)

        logger.debug("{} | initializing note".format(self))

    def __str__(self):

        return "Note<M{},C{}>({}{})".format(
            *self.location, self.name, self.octave
        )
