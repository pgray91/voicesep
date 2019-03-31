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

        self.assertTrue(expected["input0"].any())
        self.assertFalse((true["input0"] - expected["input0"]).any())
        self.assertFalse((true["input1"] - expected["input1"]).any())

    def test_index_slice_all(self):

        self.score.name = "test2"
        self.dataset.write(self.score, beat_horizon=4, one_to_many=True)

        true = {
            "input0": np.concatenate(
                (
                    self.dataset.groups[0]["input0"][:],
                    self.dataset.groups[1]["input0"][:]
                )
            ),
            "input1": np.concatenate(
                (
                    self.dataset.groups[0]["input1"][:],
                    self.dataset.groups[1]["input1"][:]
                )
            )
        }
        expected = self.dataset[:]

        self.assertFalse((true["input0"] - expected["input0"]).any())
        self.assertFalse((true["input1"] - expected["input1"]).any())

    def test_index_slice_half(self):

        self.score.name = "test2"
        self.dataset.write(self.score, beat_horizon=4, one_to_many=True)

        true = {
            "input0": np.concatenate(
                (
                    self.dataset.groups[0]["input0"][5:],
                    self.dataset.groups[1]["input0"][:5]
                )
            ),
            "input1": np.concatenate(
                (
                    self.dataset.groups[0]["input1"][5:],
                    self.dataset.groups[1]["input1"][:5]
                )
            )
        }
        expected = self.dataset[5:16]

        self.assertFalse((true["input0"] - expected["input0"]).any())
        self.assertFalse((true["input1"] - expected["input1"]).any())

    def test_index_slice_first_half(self):

        self.score.name = "test2"
        self.dataset.write(self.score, beat_horizon=4, one_to_many=True)

        true = {
            "input0": self.dataset.groups[0]["input0"][1:5],
            "input1": self.dataset.groups[0]["input1"][1:5],
        }
        expected = self.dataset[1:5]

        self.assertFalse((true["input0"] - expected["input0"]).any())
        self.assertFalse((true["input1"] - expected["input1"]).any())

    def test_index_slice_first_half(self):

        self.score.name = "test2"
        self.dataset.write(self.score, beat_horizon=4, one_to_many=True)

        true = {
            "input0": self.dataset.groups[1]["input0"][1:5],
            "input1": self.dataset.groups[1]["input1"][1:5],
        }
        expected = self.dataset[1:5]

        self.assertFalse((true["input0"] - expected["input0"]).any())
        self.assertFalse((true["input1"] - expected["input1"]).any())

    def test_length(self):

        length = sum(len(next(iter(group.values()))) for group in self.dataset.groups)

        self.assertEqual(length, 11)

    def test_sort(self):

        self.score.name = "test2"
        self.dataset.write(self.score, beat_horizon=4, one_to_many=True)

        self.score.name = "test3"
        self.dataset.write(self.score, beat_horizon=4, one_to_many=True)

        expected_order = ["test2", "test", "test3"]
        self.dataset.sort(expected_order)

        true_order = [os.path.basename(group.name) for group in self.dataset.groups]

        self.assertEqual(true_order, expected_order)


if __name__ == "__main__":
    unittest.main()
