import theano
import theano.tensor as T
import unittest

import voicesep as vs


class Test(unittest.TestCase):

    def setUp(self):

        name = self._testMethodName.split("_", 1)[1]

        y_hat_var = T.dscalar("y_hat")
        y_var = T.dscalar("y")
        function_var = getattr(vs.separators.neural.costs, name)(y_hat_var, y_var)

        self.function = theano.function([y_hat_var, y_var], function_var)

    def test_binary_crossentropy(self):

        self.assertAlmostEqual(self.function(0.7, 0.8), 0.526134, places=5)


if __name__ == "__main__":
    unittest.main()
