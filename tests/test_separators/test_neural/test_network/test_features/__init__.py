import os
import unittest

import voicesep as vs


class Test(unittest.TestCase):

    def setUp(self):

        path = os.path.dirname(os.path.abspath(__file__))
        self.score = vs.Score("{}/test.musicxml".format(path))

        voice1 = vs.Voice(self.score[0][0])
        voice2 = vs.Voice(self.score[0][1])
        voice3 = vs.Voice(self.score[1][0])
        voice4 = vs.Voice(self.score[1][1])

        self.active_voices = vs.ActiveVoices()

        self.active_voices.insert([voice1, voice2])

        voice1.link(voice3)
        voice1.link(voice4)
        voice2.link(voice3)
        voice2.link(voice4)

        self.active_voices.insert([voice3, voice4])

    def test_level_pair(self):

        Features = vs.separators.neural.network.Features
        features = Features(self.score[1], self.active_voices)


        data = features.level(Features.Level.PAIR)

        self.assertEqual(len(data), 10)
        self.assertEqual(len(data[0]), Features.count(Features.Level.PAIR))

    def test_count_pair(self):

        Features = vs.separators.neural.network.Features

        self.assertEqual(Features.count(Features.Level.PAIR), 100)

    def test_pad(self):

        Features = vs.separators.neural.network.Features
        features = Features(self.score[1], self.active_voices)

        data = features.level(Features.Level.PAIR)
        Features.pad(data, len(data) + 2)

        self.assertEqual(len(data), 12)
        self.assertEqual(data[-1], data[-2])
        self.assertEqual(data[-1], data[-3])
        self.assertNotEqual(data[-1], data[-4])


if __name__ == "__main__":
    unittest.main()
