import os
import unittest

import voicesep as vs


class Test(unittest.TestCase):

    def setUp(self):

        path = os.path.dirname(os.path.abspath(__file__))
        sheet = "{}/test.musicxml".format(path)

        score = vs.Score(sheet)
        waterfall = [
            {
                "Benchmark": {
                    "one_to_many": True
                }
            }
        ]
        beat_horizon = 2

        assignments = vs.separate(score, waterfall, beat_horizon)
        self.voices = [voice for assignment in assignments for voice in assignment]

    def test_success(self):

        with self.subTest("left empty"):
            self.assertEqual(len(self.voices[0].left), 0)

        with self.subTest("right connected"):
            self.assertEqual(len(self.voices[0].right), 1)

        with self.subTest("right voice"):
            self.assertEqual(list(self.voices[0].right)[0], self.voices[1])


if __name__ == "__main__":
    unittest.main()
