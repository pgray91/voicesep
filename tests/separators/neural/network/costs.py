import theano
import theano.tensor as T
import unittest

import voicesep as vs

theano.config.floatX = "float64"


class Test(unittest.TestCase):

    def setUp(self):

        self.y_hat_var = T.matrix("y_hat", dtype=theano.config.floatX)

    def test_binary_crossentropy(self):

        cost_var, cost_inputs = vs.separators.neural.network.costs.binary_crossentropy(
            self.y_hat_var
        )
        cost = theano.function([self.y_hat_var, cost_inputs[0]], cost_var)

        self.assertAlmostEqual(cost([[0.7]], [[0.8]]), 0.526134, places=5)

    def test_max(self):

        cost_var, _ = vs.separators.neural.network.costs.max(
            self.y_hat_var, assignment_limit=2, margin=1
        )
        cost = theano.function([self.y_hat_var], cost_var)

        self.assertEqual(cost([[1], [2], [3], [4]]), 2)


if __name__ == "__main__":
    unittest.main()
