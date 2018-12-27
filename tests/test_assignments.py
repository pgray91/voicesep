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

        left_voice = vs.Voice(self.left_note)
        right_voice = vs.Voice(self.right_note)
        left_voice.append(right_voice)

        self.assignments = vs.Assignments()
        self.assignments.append([left_voice])
        self.assignments.append([right_voice])

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
