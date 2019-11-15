import h5py
import numpy as np
import os
import unittest

import voicesep as vs


class Test(unittest.TestCase):

    def setUp(self):

        self.path = os.path.dirname(os.path.abspath(__file__))
        self.score = vs.Score(f"{self.path}/test.musicxml")

        self.dataset = vs.separators.neural.network.Dataset(
            f"{self.path}/test",
            vs.separators.neural.network.Dataset.Writer.NOTE_LEVEL
        )

        self.dataset.write(self.score, beat_horizon=4, one_to_many=True)

    def tearDown(self):

        del self.dataset
        os.remove(f"{self.path}/test.hdf5")

    def test_length(self):

        self.score.name = "test2"
        self.dataset.write(self.score, beat_horizon=4, one_to_many=True)

        self.assertEqual(len(self.dataset), 22)

    def test_open(self):

        del self.dataset

        self.dataset = vs.separators.neural.network.Dataset(
            f"{self.path}/test",
            vs.separators.neural.network.Dataset.Writer.NOTE_LEVEL
        )

        expected = ["/test"]
        true = [group.name for group in self.dataset.groups]

        self.assertEqual(true, expected)

    def test_index_single(self):

        true = [
            self.dataset.groups[0]["0"][2],
            self.dataset.groups[0]["1"][2]
        ]
        expected = self.dataset[2]

        self.assertTrue(expected[0].any())
        self.assertFalse((true[0] - expected[0]).any())
        self.assertFalse((true[1] - expected[1]).any())

    def test_index_slice_all(self):

        self.score.name = "test2"
        self.dataset.write(self.score, beat_horizon=4, one_to_many=True)

        true = [
            np.concatenate(
                (
                    self.dataset.groups[0]["0"][:],
                    self.dataset.groups[1]["0"][:]
                )
            ),
            np.concatenate(
                (
                    self.dataset.groups[0]["1"][:],
                    self.dataset.groups[1]["1"][:]
                )
            )
        ]
        expected = self.dataset[:]

        self.assertFalse((true[0] - expected[0]).any())
        self.assertFalse((true[1] - expected[1]).any())

    def test_index_slice_half(self):

        self.score.name = "test2"
        self.dataset.write(self.score, beat_horizon=4, one_to_many=True)

        true = [
            np.concatenate(
                (
                    self.dataset.groups[0]["0"][5:],
                    self.dataset.groups[1]["0"][:5]
                )
            ),
            np.concatenate(
                (
                    self.dataset.groups[0]["1"][5:],
                    self.dataset.groups[1]["1"][:5]
                )
            )
        ]
        expected = self.dataset[5:16]

        self.assertFalse((true[0] - expected[0]).any())
        self.assertFalse((true[1] - expected[1]).any())

    def test_index_slice_first_half(self):

        self.score.name = "test2"
        self.dataset.write(self.score, beat_horizon=4, one_to_many=True)

        true = [
            self.dataset.groups[0]["0"][1:5],
            self.dataset.groups[0]["1"][1:5]
        ]
        expected = self.dataset[1:5]

        self.assertFalse((true[0] - expected[0]).any())
        self.assertFalse((true[1] - expected[1]).any())

    def test_index_slice_second_half(self):

        self.score.name = "test2"
        self.dataset.write(self.score, beat_horizon=4, one_to_many=True)

        true = [
            self.dataset.groups[1]["0"][1:5],
            self.dataset.groups[1]["1"][1:5]
        ]
        expected = self.dataset[12:16]

        self.assertFalse((true[0] - expected[0]).any())
        self.assertFalse((true[1] - expected[1]).any())

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
