import unittest

import voicesep as vs


class Test(unittest.TestCase):

    def setUp(self):

        self.left_note = vs.Note(
            name="C",
            octave=4,
            location=(0, 0)
        )
        self.right_note = vs.Note(
            name="C",
            octave=4,
            location=(0, 1)
        )

        self.left_voice = vs.Voice(self.left_note)
        self.right_voice = vs.Voice(self.right_note)
        self.left_voice.link(self.right_voice)

        self.assignments = vs.Assignments()
        self.assignments.append([self.left_voice])
        self.assignments.append([self.right_voice])

    def test_index(self):

        self.assertEqual(self.assignments[0], [self.left_voice])

    def test_iter(self):

        self.assertEqual(list(self.assignments), [[self.left_voice], [self.right_voice]])

    def test_len(self):

        self.assertEqual(len(self.assignments), 2)

    def test_pairs(self):

        pairs = self.assignments.pairs()

        pair = next(iter(pairs))
        left_note, right_note = pair[0], pair[1]

        with self.subTest("length"):
            self.assertEqual(len(pairs), 1)

        with self.subTest("left note"):
            self.assertEqual(left_note, self.left_note)

        with self.subTest("right note"):
            self.assertEqual(right_note, self.right_note)


if __name__ == "__main__":
    unittest.main()
