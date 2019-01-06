import theano
import theano.tensor as T
import unittest

import voicesep as vs


class Test(unittest.TestCase):

    def setUp(self):

        name = self._testMethodName.split("_", 1)[1]

        X_var = T.dvectors("X")
        function_var = getattr(vs.separators.neural.activations, name)(X_var)

        self.function = theano.function([X_var], function_var)

    def test_linear(self):

        self.assertEqual(float(self.function([0.7])), 0.7)

    def test_sigmoid(self):

        self.assertAlmostEqual(float(self.function([0.7])), 0.668187, places=5)

    def test_relu(self):

        self.assertAlmostEqual(float(self.function([-0.7])), 0.0)

    def test_softmax(self):

        self.assertAlmostEqual(float(self.function([0.7])), 1.0)


if __name__ == "__main__":
    unittest.main()
