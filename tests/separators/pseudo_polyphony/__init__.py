import logging
import os
import unittest

import voicesep as vs


class Test(unittest.TestCase):

    def setUp(self):

        path = os.path.dirname(os.path.abspath(__file__))
        sheet = f"{path}/test.musicxml"

        score = vs.Score(sheet)
        waterfall = [
            {
                "PseudoPolyphony": {
                    "repeat_limit": 2
                }
            }
        ]
        beat_horizon = 2

        assignments = vs.separate(score, waterfall, beat_horizon)
        self.voices = [voice for assignment in assignments for voice in assignment]

    def test_success(self):

        expected_pairs = [
            (self.voices[0], self.voices[3]),
            (self.voices[3], self.voices[6])
        ]

        for pair in expected_pairs:
            with self.subTest(f"({pair[0]}, {pair[1]})"):
                self.assertTrue(pair[1] in pair[0].right)

        expected_empty = [
            self.voices[1],
            self.voices[2],
            self.voices[4],
            self.voices[5]
        ]

        for empty in expected_empty:
            with self.subTest(f"{empty}"):
                self.assertEqual(len(empty.left), 0)


if __name__ == "__main__":
    unittest.main()
