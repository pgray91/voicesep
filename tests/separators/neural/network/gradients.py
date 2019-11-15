import numpy as np
import theano
import theano.tensor as T
import unittest

import voicesep as vs


class Test(unittest.TestCase):

    def setUp(self):

        name = self._testMethodName.split("_", 1)[1]

        X_var = T.matrix("X", dtype=theano.config.floatX)

        self.layer = vs.separators.neural.network.Layer(
            X_var,
            input_size=1,
            output_size=1,
            activation="linear"
        )

        y_hat_var = self.layer.y_hat_var
        cost_var, cost_inputs = (
            vs.separators.neural.network.costs.binary_crossentropy(y_hat_var)
        )

        updates = getattr(vs.separators.neural.network.gradients, name)(
            self.layer.params, cost_var
        )

        cost = theano.function(
            inputs=[X_var, *cost_inputs],
            outputs=cost_var,
            updates=updates
        )

        W = np.array([[1]], dtype=theano.config.floatX)
        b = np.array([0], dtype=theano.config.floatX)
        self.layer.set_weights(W, b)

        X = np.array([[0.7]], dtype=theano.config.floatX)
        y = np.array([[1]], dtype=np.int16)
        cost(X, y)

    def test_sgd(self):

        W = self.layer.get_weights()[0]
        self.assertEqual(float(W), 2)

    def test_adadelta(self):

        W = self.layer.get_weights()[0]
        self.assertAlmostEqual(float(W), 1.004472, places=5)


if __name__ == "__main__":
    unittest.main()
