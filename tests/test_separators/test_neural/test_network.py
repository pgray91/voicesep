import numpy as np
from sklearn.datasets import make_classification
from sklean.model_selection import train_test_split
import unittest

import voicesep as vs


class Test(unittest.TestCase):

    def test_binary_crossentropy(self):

        X, y = make_classification(
            n_samples=1000,
            n_features=10,
            n_informative=10,
            n_redundant=0,
            n_repeated=0,
            n_classes=2,
            n_clusters_per_class=1
        )

        train_X, test_X, train_y, test_y = train_test_split(X, y, test_size=0.1)

        neural_network = vs.separators.neural.Network()

        neural_network.build(
            dimensions=(train_X.shape[1], 20, 1),
            hidden_activations="relu",
            output_activations="sigmoid"
        )

        L2_reg = 0
        learning_rate = 1e-2
        neural_network.compile(
            cost=("binary_crossentropy", L2_reg), gradient=("sgd", (learning_rate,))
        )

        neural_network.train(train_X, train_y, epochs=300, batch_size=20)

        y_hat = neural_network.predict(test_X).flatten()
        result = np.sqrt(np.mean(np.power(y_hat - test_y, 2)))

        self.assertLess(result, 9)


if __name__ == "__main__":
    unittest.main()
