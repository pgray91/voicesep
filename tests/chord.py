import unittest

import voicesep as vs


class Test(unittest.TestCase):

    def setUp(self):

        self.note = vs.Note(
            name="C",
            octave=4,
            location=(0, 0)
        )
        self.chord = vs.Chord(
            notes=[self.note],
            attribute=True
        )

    def test_attribute(self):

        self.assertTrue(self.chord.attribute)

    def test_index(self):

        self.assertEqual(self.chord[0], self.note)

    def test_iter(self):

        self.assertEqual(list(self.chord), [self.note])

    def test_len(self):

        self.assertEqual(len(self.chord), 1)

    def test_str(self):

        self.assertEqual(str(self.chord), f"Chord({self.note})")


if __name__ == "__main__":
    unittest.main()
