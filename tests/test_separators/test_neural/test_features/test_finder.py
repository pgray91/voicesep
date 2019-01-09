import inspect
import os
import sys
import unittest

import voicesep as vs


module = sys.modules[__name__]

class Test(unittest.TestCase, vs.separators.neural.network.features.Feature):

    def generate(x):

        return [x == i for i in Test.range()]

    def range():

        return range(3)

    def test_count(self):

        self.assertEqual(
            vs.separators.neural.network.features.finder.count(module), 3
        )

    def test_find(self):

        classes = vs.separators.neural.network.features.finder.find(module)

        with self.subTest("Test"):
            self.assertEqual(next(classes), Test)

        with self.subTest("length"):
            self.assertRaises(StopIteration , next, classes)

    def test_generate(self):

        classes = vs.separators.neural.network.features.finder.find(module)

        actual_feature = next(classes).generate(2)
        expected_feature = [0, 0, 1]
        
        self.assertEqual(actual_feature, expected_feature)


if __name__ == "__main__":
    unittest.main()
