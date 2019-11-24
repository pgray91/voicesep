import logging
import os
import unittest

import voicesep as vs


class Test(unittest.TestCase):

    def setUp(self):

        path = os.path.dirname(os.path.abspath(__file__))
        name = self._testMethodName
        sheet = f"{path}/{name}.musicxml"

        self.score = vs.Score(sheet)
        self.beat_horizon = 2

    def test_one_to_many(self):

        waterfall = [
            {
                "Benchmark": {
                    "one_to_many": True
                }
            }
        ]

        assignments = vs.separate(self.score, waterfall, self.beat_horizon)
        voices = [voice for assignment in assignments for voice in assignment]

        expected_pairs = [
            (voices[0], voices[2]),
            (voices[0], voices[3]),
            (voices[1], voices[3]),
            (voices[1], voices[4]),
            (voices[2], voices[6]),
            (voices[2], voices[7]),
            (voices[3], voices[8]),
            (voices[4], voices[8]),
            (voices[6], voices[9]),
            (voices[7], voices[10])
        ]

        for pair in expected_pairs:
            with self.subTest(f"({pair[0]}, {pair[1]})"):
                self.assertTrue(pair[1] in pair[0].right)

    def test_one_to_many_convergence(self):

        waterfall = [
            {
                "Benchmark": {
                    "one_to_many": True
                }
            }
        ]

        assignments = vs.separate(self.score, waterfall, self.beat_horizon)
        voices = [voice for assignment in assignments for voice in assignment]

        expected_pairs = [
            (voices[0], voices[2]),
            (voices[1], voices[2])
        ]

        for pair in expected_pairs:
            with self.subTest(f"({pair[0]}, {pair[1]})"):
                self.assertTrue(pair[1] in pair[0].right)

    def test_one_to_many_divergence(self):

        waterfall = [
            {
                "Benchmark": {
                    "one_to_many": True
                }
            }
        ]

        assignments = vs.separate(self.score, waterfall, self.beat_horizon)
        voices = [voice for assignment in assignments for voice in assignment]

        expected_pairs = [
            (voices[0], voices[1]),
            (voices[0], voices[2])
        ]

        for pair in expected_pairs:
            with self.subTest(f"({pair[0]}, {pair[1]})"):
                self.assertTrue(pair[1] in pair[0].right)

    def test_one_to_one(self):

        waterfall = [
            {
                "Benchmark": {
                    "one_to_many": False
                }
            }
        ]

        assignments = vs.separate(self.score, waterfall, self.beat_horizon)
        voices = [voice for assignment in assignments for voice in assignment]

        expected_pairs = [
            (voices[0], voices[2]),
            (voices[1], voices[3]),
            (voices[2], voices[6]),
            (voices[3], voices[8]),
            (voices[6], voices[9]),
            (voices[7], voices[10])
        ]

        for pair in expected_pairs:
            with self.subTest(f"({pair[0]}, {pair[1]})"):
                self.assertTrue(pair[1] in pair[0].right)

    def test_one_to_many_clear(self):

        waterfall = [
            {
                "Benchmark": {
                    "one_to_many": True
                }
            }
        ]

        assignments = vs.separate(self.score, waterfall, self.beat_horizon)
        voices = [voice for assignment in assignments for voice in assignment]

        expected_pairs = [
            (voices[0], voices[1]),
            (voices[1], voices[2]),
            (voices[2], voices[3]),
            (voices[2], voices[4])
        ]

        for pair in expected_pairs:
            with self.subTest(f"({pair[0]}, {pair[1]})"):
                self.assertTrue(pair[1] in pair[0].right)

        self.assertFalse(voices[0] in voices[2].left)


if __name__ == "__main__":
    unittest.main()
