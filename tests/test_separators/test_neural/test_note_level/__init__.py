import numpy as np
import os
import theano
import unittest

from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

import voicesep as vs

theano.config.floatX = "float64"

class Test(unittest.TestCase):

    def test_train(self):

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

        train_X1 = train_X
        train_X2 = train_X[:225]
        train_X1 = train_X1.astype(theano.config.floatX)
        train_X2 = train_X2.astype(theano.config.floatX)

        test_X1 = test_X.astype(theano.config.floatX)
        test_X2 = test_X.astype(theano.config.floatX)
        train_y = train_y.astype(theano.config.floatX)

        # train_y = train_y.reshape(train_y.shape[0], 1)[:225]
        # test_y = test_y.reshape(test_y.shape[0], 1)[:225]
        train_y = train_y.reshape(train_y.shape[0], 1)
        test_y = test_y.reshape(test_y.shape[0], 1)

        network = vs.separators.neural.Network()

        network.build(
            # dimensions=((train_X1.shape[1], 10, 4), train_X2.shape[1], 20, 1),
            dimensions=(train_X.shape[1], 20, 1),
            hidden_activations="relu",
            output_activation="sigmoid"
        )

        network.compile(
            cost_type="binary_crossentropy",
            cost_args=(),
            gradient_type="adadelta",
            gradient_args=(),
            L2_reg=0.01
        )

        # network.train([train_X1, train_X2, train_y], epochs=10, batch_size=20)
        network.train([train_X, train_y], epochs=10, batch_size=20)

        # y_hat = network.predict([test_X1, test_X2])
        # # y_hat = network.predict([test_X2])
        #
        # result = np.sum(np.round(y_hat) == test_y) / len(test_y)
        #
        # self.assertGreater(result, 0.9)

    def test_write_read(self):

        network_file = "{}.test_write_read.npy".format(
            os.path.splitext(os.path.abspath(__file__))[0]
        )

        network = vs.separators.neural.Network()
        network.build(
            dimensions=((10, 15, 4), 10, 20, 1),
            hidden_activations="relu",
            output_activation="sigmoid"
        )

        for layer in network.layers:
            layer.random_weights()

        write_dimensions = network.dimensions
        write_hidden_activations = network.hidden_activations
        write_output_activation = network.output_activation
        write_params = []
        for layer in network.layers:
            write_params.extend(map(str, layer.get_weights()))

        network.write(network_file)

        network = vs.separators.neural.Network()

        network.read(network_file)

        read_dimensions = network.dimensions
        read_hidden_activations = network.hidden_activations
        read_output_activation = network.output_activation
        read_params = []
        for layer in network.layers:
            read_params.extend(map(str, layer.get_weights()))

        with self.subTest("dimensions"):
            self.assertEqual(read_dimensions, write_dimensions)

        with self.subTest("hidden activations"):
            self.assertEqual(read_hidden_activations, write_hidden_activations)

        with self.subTest("output activation"):
            self.assertEqual(read_output_activation, write_output_activation)

        with self.subTest("params"):
            self.assertEqual(read_params, write_params)

        os.remove(network_file)


if __name__ == "__main__":
    unittest.main()
