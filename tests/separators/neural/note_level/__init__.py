import logging
import os
import unittest

import voicesep as vs


class Test(unittest.TestCase):

    def setUp(self):

        path = os.path.dirname(os.path.abspath(__file__))
        score = vs.Score(f"{path}/test.musicxml")
        network = f"{path}/test.npy"

        waterfall = [
            {
                "neural.NoteLevel": {
                    "network": network,
                    "assignment_threshold": .7
                }
            }
        ]
        beat_horizon = 4

        assignments = vs.separate(score, waterfall, beat_horizon)
        self.voices = [voice for assignment in assignments for voice in assignment]

    def test_pairs(self):

        expected_pairs = [
            (self.voices[0], self.voices[2]),
            (self.voices[1], self.voices[4]),
            (self.voices[1], self.voices[5]),
            (self.voices[2], self.voices[6]),
            (self.voices[4], self.voices[7]),
            (self.voices[5], self.voices[7])
        ]

        for pair in expected_pairs:
            with self.subTest(f"({pair[0]}, {pair[1]})"):
                self.assertTrue(pair[1] in pair[0].right)

    def test_count(self):

        counts = [0, 0, 1, 0, 1, 1, 1, 2]

        for voice, count in zip(self.voices, counts):
            with self.subTest(f"{voice}"):
                self.assertEqual(len(voice.left), count)


if __name__ == "__main__":
    unittest.main()
