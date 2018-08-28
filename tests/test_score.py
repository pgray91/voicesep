from   fractions import Fraction as F
import music21 as m21
import unittest

import voicesep as vs

class TestScore(unittest.TestCase):
    # Test
    # Timesig change
    # Keysig change
    # Test onset origin
    # ql_origin
    # stacatto
    # onset
    # beat
    # beat strength
    # measure index
    # chord index
    # real chord index
    # Test grace

    # name
    # octave
    # pitch space
    # duration
    # offset
    # note index
    # degree
    # chord step
    # lyric
    # color

    # Tie test
    # Test simple melody separation
    # convergence
    # divergence
    # test one_to_one separation
    # Test voice connections
    # when testing chord and note just test string rep


    def test_note_name(self):

        self.assertEqual(len(self.score), 39)

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
