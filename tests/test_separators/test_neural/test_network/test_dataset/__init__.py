import h5py
import numpy as np
import os
import unittest

import voicesep as vs


class Test(unittest.TestCase):

    def setUp(self):

        self.path = os.path.dirname(os.path.abspath(__file__))
        self.score = vs.Score("{}/test.musicxml".format(self.path))

        self.dataset = vs.separators.neural.network.Dataset(
            "{}/test".format(self.path),
            vs.separators.neural.network.Dataset.Writer.NOTE_LEVEL
        )

        self.dataset.write(self.score, beat_horizon=4, one_to_many=True)

    def tearDown(self):

        del self.dataset
        os.remove("{}/test.hdf5".format(self.path))

    def test_index_single(self):

        true = {
            "input0": self.dataset.groups[0]["input0"][2],
            "input1": self.dataset.groups[0]["input1"][2],
        }
        expected = self.dataset[2]


        self.assertFalse((true["input0"] - expected["input0"]).any())
        self.assertFalse((true["input1"] - expected["input1"]).any())

        # self.writer.run(chord, active_voices, assignment)
        #
        # self.assertEqual(self.writer.length, 9)
        #
        # self.assertEqual(self.writer.features_dataset.shape, (9, 100))
        # self.assertTrue(self.writer.features_dataset[7].any())
        #
        # labels = [[1], [1], [0], [1], [1], [0], [0], [0], [1]]
        # self.assertFalse((self.writer.labels_dataset[:] - labels).any())


if __name__ == "__main__":
    unittest.main()
