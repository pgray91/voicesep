import os
import unittest

import voicesep as vs


class Test(unittest.TestCase):

    def setUp(self):

        path = os.path.dirname(os.path.abspath(__file__))
        score = vs.Score("{}/test.musicxml".format(path))
        chord = score[0]

        name = "".join(part.title() for part in self._testMethodName.split("_")[1:])
        feature = getattr(vs.separators.neural.network.features.voice_level, name)

        self.data = feature.generate(voice, active_voices)

    def test_average_pitch_range(self):

        MIN_PITCH = vs.separators.neural.network.features.constants.MIN_PITCH
        MAX_PITCH = vs.separators.neural.network.features.constants.MAX_PITCH
        INTERVAL = vs.separators.neural.network.features.constants.INTERVAL

        data = [0] * len(range(MIN_PITCH, MAX_PITCH, INTERVAL))
        data[1] = 1

        self.assertEqual(self.data, data)


if __name__ == "__main__":
    unittest.main()
