import logging
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
                "Envelope": {}
            }
        ]
        beat_horizon = 2

        assignments = vs.separate(score, waterfall, beat_horizon)
        self.voices = [voice for assignment in assignments for voice in assignment]

    def test_pairs(self):

        expected_pairs = [
            (self.voices[0], self.voices[2]),
            (self.voices[1], self.voices[5]),
            (self.voices[2], self.voices[3]),
            (self.voices[3], self.voices[4])
        ]

        for pair in expected_pairs:
            with self.subTest("({}, {})".format(pair[0], pair[1])):
                self.assertTrue(pair[1] in pair[0].right)

    def test_count(self):

        for voice in self.voices:
            with self.subTest("{}".format(voice)):
                self.assertTrue(len(voice.left) <= 1)


if __name__ == "__main__":
    unittest.main()
