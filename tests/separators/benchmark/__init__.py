import logging
import os
import unittest

import voicesep as vs


class Test(unittest.TestCase):

    def setUp(self):

        path = os.path.dirname(os.path.abspath(__file__))
        name = self._testMethodName
        sheet = "{}/{}.musicxml".format(path, name)

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

    def test_one_to_many(self):

        expected_pairs = [
            (self.voices[0], self.voices[2]),
            (self.voices[0], self.voices[3]),
            (self.voices[1], self.voices[3]),
            (self.voices[1], self.voices[4]),
            (self.voices[2], self.voices[6]),
            (self.voices[2], self.voices[7]),
            (self.voices[3], self.voices[8]),
            (self.voices[4], self.voices[8]),
            (self.voices[6], self.voices[9]),
            (self.voices[7], self.voices[10])
        ]

        for pair in expected_pairs:
            with self.subTest("({}, {})".format(pair[0], pair[1])):
                self.assertTrue(pair[1] in pair[0].right)

    def test_one_to_many_convergence(self):

        expected_pairs = [
            (self.voices[0], self.voices[2]),
            (self.voices[1], self.voices[2])
        ]

        for pair in expected_pairs:
            with self.subTest("({}, {})".format(pair[0], pair[1])):
                self.assertTrue(pair[1] in pair[0].right)

    def test_one_to_many_divergence(self):

        expected_pairs = [
            (self.voices[0], self.voices[1]),
            (self.voices[0], self.voices[2])
        ]

        for pair in expected_pairs:
            with self.subTest("({}, {})".format(pair[0], pair[1])):
                self.assertTrue(pair[1] in pair[0].right)

    def test_one_to_one(self):

        expected_pairs = [
            (self.voices[0], self.voices[2]),
            (self.voices[1], self.voices[3]),
            (self.voices[2], self.voices[6]),
            (self.voices[3], self.voices[8]),
            (self.voices[6], self.voices[9]),
            (self.voices[7], self.voices[10])
        ]

        for pair in expected_pairs:
            with self.subTest("({}, {})".format(pair[0], pair[1])):
                self.assertTrue(pair[1] in pair[0].right)


if __name__ == "__main__":
    unittest.main()
