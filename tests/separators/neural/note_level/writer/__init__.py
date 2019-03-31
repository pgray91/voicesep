import h5py
import numpy as np
import os
import unittest

import voicesep as vs


class Test(unittest.TestCase):

    def setUp(self):

        self.path = os.path.dirname(os.path.abspath(__file__))
        self.score = vs.Score("{}/test.musicxml".format(self.path))

        self.fp = h5py.File("{}/test.hdf5".format(self.path), "w")

        self.group = self.fp.create_group(self.score.name)

        self.writer = vs.separators.neural.note_level.Writer(self.score, self.group)

    def tearDown(self):

        self.fp.close()
        os.remove("{}/test.hdf5".format(self.path))

    def test_init(self):

        self.assertTrue("0" in self.group)
        self.assertTrue("1" in self.group)

    def test_run(self):

        voice1 = vs.Voice(self.score[0][0])
        voice2 = vs.Voice(self.score[0][1])
        voice3 = vs.Voice(self.score[1][0])
        voice4 = vs.Voice(self.score[1][1])
        voice5 = vs.Voice(self.score[1][2])

        active_voices = vs.ActiveVoices()

        active_voices.insert([voice1, voice2])

        voice1.link(voice3)
        voice1.link(voice4)
        voice2.link(voice3)
        voice2.link(voice4)

        chord = self.score[1]
        assignment = [voice3, voice4, voice5]

        self.writer.run(chord, active_voices, assignment)

        self.assertEqual(self.writer.length, 9)

        self.assertEqual(self.writer.features_dataset.shape, (9, 145))
        self.assertTrue(self.writer.features_dataset[7].any())

        labels = [[1], [1], [0], [1], [1], [0], [0], [0], [1]]
        self.assertFalse((self.writer.labels_dataset[:] - labels).any())


if __name__ == "__main__":
    unittest.main()
