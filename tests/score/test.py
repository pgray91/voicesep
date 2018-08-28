from   fractions import Fraction as F
import music21 as m21
import unittest

import voicesep as vs

# read from file for now and come back
# with tinynotation

RED="#FF0000"
GREEN="#00FF00"
BLUE="#0000FF"

class TestScore(unittest.TestCase):
    # Test
    # Timesig change
    # Keysig change
    # Test onset origin
    # ql_origin
    # onset
    # beat
    # beat strength
    # measure index
    # chord index
    # real chord index
    # Test grace

    # Tie test
    # Test simple melody separation
    # convergence
    # divergence
    # test one_to_one separation
    # Test voice connections
    # when testing chord and note just test string rep


    def test_chord_step_note(self):

        score = vs.Score("xml/test_chord_step_note.xml")
        chord = self.score[0]
        note = chord[0]

        self.assertEqual(note.chord_step, 0)
        
    def test_color_note(self):

        score = vs.Score("xml/test_color_note.xml")
        chord = self.score[0]
        note = chord[0]
        
    def test_degree_note(self):

        score = vs.Score("xml/test_degree_note.xml")
        chord = self.score[0]
        note = chord[0]

        self.assertEqual(note.degree, 0)


        self.assertEqual(note.color, BLUE)

    def test_duration_note(self):

        score = vs.Score("xml/test_duration_note.xml")
        chord = self.score[0]
        note = chord[0]

        self.assertEqual(note.duration, 4)

    def test_index_note(self):

        score = vs.Score("xml/test_index_note.xml")
        chord = self.score[0]
        note = chord[0]

        self.assertEqual(note.index, 0)

    def test_location_note(self):

        score = vs.Score("xml/test_location_note.xml")
        chord = self.score[0]
        note = chord[0]

        measure_index, chord_index = 0, 0

        self.assertEqual(note.location, (measure_index, chord_index))

    def test_lyric_note(self):

        score = vs.Score("xml/test_lyric_note.xml")
        chord = self.score[0]
        note = chord[0]

        self.assertEqual(note.lyric, ["1"])

    def test_name_note(self):

        score = vs.Score("xml/test_name_note.xml")
        chord = self.score[0]
        note = chord[0]

        self.assertEqual(note.name, "C")

    def test_offset_note(self):

        score = vs.Score("xml/test_octave_note.xml")
        chord = self.score[0]
        note = chord[0]

        self.assertEqual(note.octave, 4)

    def test_offset_note(self):

        score = vs.Score("xml/test_offset_note.xml")
        chord = self.score[0]
        note = chord[0]

        self.assertEqual(note.offset, 4)

    def test_pitch_note(self):

        score = vs.Score("xml/test_pitch_note.xml")
        chord = self.score[0]
        note = chord[0]

        self.assertEqual(note.pitch, 60)

    def test_stacatto(self):

        with self.subTest(subtest="single note")
            score = vs.Score("single_note.xml")
            chord = score[0]
            note = chord[0]

            self.assertEqual(note.duration, 2)

    def test_stacatto_chord(self):

        score = vs.Score("xml/test_stacatto.xml")
        chord = self.score[0]

        for note in chord:
              with self.subTest(note=note):
                  self.assertEqual(note.duration, 2)

    def test_stacatto_split_chord(self):

        score = vs.Score("xml/test_stacatto_split_chord.xml")
        chord = self.score[0]

        durations = [2, 2, 1, 1]

        for note, duration in zip(chord, duration):
              with self.subTest(note=note):
                  self.assertEqual(note.duration, duration)

    def test_tie_chord_count_note(self):

        score = vs.Score("xml/test_tie_note.xml")
        chord = self.score[0]
        note = chord[0]

        self.assertEqual(note.duration, 2)


    def test_01_note_count(self):
        note_count = 0
        for chord in self.score:
          note_count += len(chord)
        self.assertEqual(note_count, 66)

    def test_02_chord_length(self):
        expected_chord_length = [
          1, 1, 2, 3, 2, 3, 1, 2, 1, 4, 
          1, 2, 3, 4, 2, 7, 1, 1, 1, 1,
          1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
          1, 1, 1, 1, 2, 2, 2, 1, 2
        ]

       for i, chord in enumerate(self.score):
          with self.subTest(test_id=("Chord Length 1: Chord Index %d" % i)):
            self.assertEqual(len(chord), expected_chord_length[i])

        i = 0 
        for chord in self.score:
          for note in chord:
            with self.subTest(test_id=("Chord Length 2: Note Index %d" % i)):
              self.assertEqual(note.chord_length, len(chord))
            i += 1

class TestChord(unittest.TestCase):

    def test_str(self):
        

class TestNote(unittest.TestCase):

    def test_str(self):
        
        note = Note(
            name="C",
            octave=4,
            measure_index=0,
            chord_index=0
        )

        self.assertEqual("Note<M0,C0>(C5)", note)

class TestVoice(unittest.TestCase):
    pass


if __name__ == "__main__":
    unittest.main()
