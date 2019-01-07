import numpy as np
import theano
import theano.tensor as T
import unittest

import voicesep as vs


class Test(unittest.TestCase):

    def setUp(self):

        self.X_var = T.dmatrix("X")
        self.layer = vs.separators.neural.Layer(
            self.X_var,
            input_size=1,
            output_size=1,
            activation="linear"
        )

    def test_random_weights(self):

        original_W = self.layer.get_weights()[0]
        original_b = np.zeros((1,))

        self.layer.random_weights()
        random_params = self.layer.get_weights()

        with self.subTest("W"):
            self.assertNotEqual(original_W, random_params[0])

        with self.subTest("b"):
            self.assertEqual(original_b, random_params[1])

    def test_set_weights(self):

        W = np.array([[10]], dtype=theano.config.floatX)
        b = np.array([10], dtype=theano.config.floatX)

        self.layer.set_weights(W, b)

        params = self.layer.get_weights()

        with self.subTest("W"):
            self.assertEqual(W, params[0])

        with self.subTest("b"):
            self.assertEqual(b, params[1])

    def test_y_hat_var(self):

        function = theano.function([self.X_var], self.layer.y_hat_var)

        W = np.array([[1]], dtype=theano.config.floatX)
        b = np.array([1], dtype=theano.config.floatX)

        self.layer.set_weights(W, b)

        self.assertEqual(float(function([[1]])), 2)


if __name__ == "__main__":
    unittest.main()
