import unittest

import voicesep as vs


class Test(unittest.TestCase):

    def setUp(self):

        self.note = vs.Note(
            name="C",
            octave=4,
            location=(0, 0),
            attribute=True
        )

    def test_pitch(self):

        self.assertEqual(self.note.pitch, 60)

    def test_attribute(self):

        self.assertTrue(self.note.attribute)

    def test_equal(self):

        note = vs.Note(
            name="C",
            octave=4,
            location=(0, 0)
        )

        with self.subTest("equal"):
            self.assertEqual(self.note, note)

        with self.subTest("hash"):
            self.assertEqual(hash(self.note), hash(note))

    def test_not_equal(self):

        note = vs.Note(
            name="D",
            octave=4,
            location=(0, 0)
        )

        self.assertNotEqual(self.note, note)

    def test_less_than(self):

        note_d = vs.Note(
            name="D",
            octave=4,
            location=(0, 0)
        )

        self.assertLess(self.note, note_d)

    def test_str(self):

        self.assertEqual(str(self.note), "Note<M0,C0>(C4)")


if __name__ == "__main__":
    unittest.main()
