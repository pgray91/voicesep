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

    def test_str(self):

        self.assertEqual(str(self.note), "Note<M0,C0>(C4)")

    def test_attribute(self):

        self.assertTrue(self.note.attribute)


if __name__ == "__main__":
    unittest.main()
