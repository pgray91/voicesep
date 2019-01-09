import theano
import theano.tensor as T
import unittest

import voicesep as vs


class Test(unittest.TestCase):

    def setUp(self):

        name = self._testMethodName.split("_", 1)[1]

        y_var = T.dscalar("y")
        y_hat_var = T.dscalar("y_hat")
        function_var = getattr(vs.separators.neural.costs, name)(y_var, y_hat_var)

        self.function = theano.function([y_var, y_hat_var], function_var)

    def test_binary_crossentropy(self):

        self.assertAlmostEqual(self.function(0.8, 0.7), 0.526134, places=5)


if __name__ == "__main__":
    unittest.main()
