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

    def test_equal(self):

        note = vs.Note(
            name="C",
            octave=4,
            location=(0, 0)
        )
        voice = vs.Voice(note)

        with self.subTest("equal"):
            self.assertEqual(self.voice, voice)

        with self.subTest("hash"):
            self.assertEqual(hash(self.voice), hash(voice))

    def test_link(self):

        right_voice = vs.Voice(self.note)
        self.voice.link(right_voice)

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

    def test_not_equal(self):

        note = vs.Note(
            name="D",
            octave=4,
            location=(0, 0)
        )
        voice = vs.Voice(note)

        self.assertNotEqual(self.voice, voice)

    def test_less_than(self):

        note_d = vs.Note(
            name="D",
            octave=4,
            location=(0, 0)
        )
        voice_d = vs.Voice(note_d)

        self.assertLess(self.voice, voice_d)

    def test_str(self):

        self.assertEqual(str(self.voice), "Voice({self.note})")


if __name__ == "__main__":
    unittest.main()
