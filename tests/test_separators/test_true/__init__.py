import logging
import sys
import unittest

import voicesep as vs

#logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

class Test(unittest.TestCase):

    def setUp(self):

        name = self._testMethodName
        sheet = "{}.musicxml".format(name)

        self.score = vs.Score(name, sheet)

    def test_separate_one_to_many(self):

        expected_pairs = {
            (self.score[0][0], self.score[1][0]),
            (self.score[0][0], self.score[1][1]),
            (self.score[0][1], self.score[1][1]),
            (self.score[0][1], self.score[1][2]),
            (self.score[1][0], self.score[2][1]),
            (self.score[1][0], self.score[2][2]),
            (self.score[1][1], self.score[2][3]),
            (self.score[1][2], self.score[2][3]),
            (self.score[2][1], self.score[3][0]),
            (self.score[2][2], self.score[3][1])
        }
        true_pairs = self.score.separate(one_to_many=True).pairs()

        self.assertEqual(expected_pairs, true_pairs)

    def test_separate_one_to_many_convergence(self):

        expected_pairs = {
            (self.score[0][0], self.score[1][0]),
            (self.score[0][1], self.score[1][0])
        }
        true_pairs = self.score.separate(one_to_many=True).pairs()

        self.assertEqual(expected_pairs, true_pairs)

    def test_separate_one_to_many_divergence(self):

        expected_pairs = {
            (self.score[0][0], self.score[1][0]),
            (self.score[0][0], self.score[1][1])
        }
        true_pairs = self.score.separate(one_to_many=True).pairs()

        self.assertEqual(expected_pairs, true_pairs)

    def test_separate_one_to_one(self):

        expected_pairs = {
            (self.score[0][0], self.score[1][0]),
            (self.score[0][1], self.score[1][1]),
            (self.score[1][0], self.score[2][1]),
            (self.score[1][1], self.score[2][3]),
            (self.score[2][1], self.score[3][0]),
            (self.score[2][2], self.score[3][1])
        }
        true_pairs = self.score.separate(one_to_many=False).pairs()

        self.assertEqual(expected_pairs, true_pairs)


if __name__ == "__main__":
    unittest.main()
