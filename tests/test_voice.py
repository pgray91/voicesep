import unittest

import voicesep as vs


class Test(unittest.TestCase):

    def setUp(self):

        self.note = vs.Note(
            name="C",
            octave=4,
            location=(0, 0)
        )
        self.voice = vs.Voice(self.note)

    def test_append(self):

        right_voice = vs.Voice(self.note)
        self.voice.append(right_voice)

        with self.subTest("left voice left length"):
            self.assertEqual(len(self.voice.left), 0)

        with self.subTest("left voice right length"):
            self.assertEqual(len(self.voice.right), 1)

        with self.subTest("right voice left length"):
            self.assertEqual(len(right_voice.left), 1)

        with self.subTest("right voice right length"):
            self.assertEqual(len(right_voice.right), 0)

        with self.subTest("left voice right value"):
            self.assertEqual(next(iter(self.voice.right)), right_voice)

        with self.subTest("right voice left value"):
            self.assertEqual(next(iter(right_voice.left)), self.voice)

    def test_str(self):

        self.assertEqual(str(self.voice), "Voice({})".format(self.note))


if __name__ == "__main__":
    unittest.main()
