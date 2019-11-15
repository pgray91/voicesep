import numpy as np
import os
import unittest

import voicesep as vs
import voicesep.separators.neural.network as vs_network


class Test(unittest.TestCase):

    def test_train(self):

        path = os.path.dirname(os.path.abspath(__file__))
        score = vs.Score(f"{path}/test.musicxml")

        dataset = vs_network.Dataset(
            f"{path}/test",
            vs_network.Dataset.Writer.NOTE_LEVEL
        )
        dataset.write(score, beat_horizon=4, one_to_many=True)

        network = vs_network.Network()

        count = vs_network.Features.count(vs_network.Features.Level.PAIR)

        network.build(
            dimensions=(count, 150, 1),
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

        network.train(dataset, epochs=200, batch_size=10)

        x, y = dataset[:]
        os.remove(f"{path}/test.hdf5")

        y_hat = network.predict([x])

        result = sum((y_hat > .7) == y) / len(y)

        self.assertGreater(result, 0.89)

    def test_write_read(self):

        network_file = (
            f"{os.path.splitext(os.path.abspath(__file__))[0]}.test_write_read.npy"
        )

        network = vs_network.Network()
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

        network = vs_network.Network()

        network.read(network_file)

        os.remove(network_file)

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


if __name__ == "__main__":
    unittest.main()
