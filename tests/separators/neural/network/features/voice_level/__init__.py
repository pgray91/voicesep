import numpy as np
import os
import unittest

import voicesep as vs


class Test(unittest.TestCase):

    def setUp(self):

        pass
        # path = os.path.dirname(os.path.abspath(__file__))
        # score = vs.Score(f"{path}/test.musicxml")
        # chord = score[0]
        #
        # name = "".join(part.title() for part in self._testMethodName.split("_")[1:])
        # feature = getattr(vs.separators.neural.network.features.voice_level, name)
        #
        # self.data = feature.generate(voice, active_voices)

    def test_average_pitch_range(self):

        feature = vs.separators.neural.network.features.voice_level.AveragePitchRange

        note1 = vs.Note("C", 4, (0, 0), onset=0)
        note2 = vs.Note("G", 4, (0, 0), onset=1)

        voice1 = vs.Voice(note1)
        voice2 = vs.Voice(note2)

        voice1.link(voice2)

        active_voices = vs.ActiveVoices()

        MIN_PITCH = vs.separators.neural.network.features.constants.MIN_PITCH
        MAX_PITCH = vs.separators.neural.network.features.constants.MAX_PITCH
        GRANULARITY = vs.separators.neural.network.features.constants.GRANULARITY

        interval = (MAX_PITCH - MIN_PITCH) / GRANULARITY

        true_data = [0] * len(np.arange(MIN_PITCH, MAX_PITCH, interval))
        true_data[5] = 1

        expected_data = feature.generate(voice2, active_voices)

        self.assertEqual(true_data, expected_data)


if __name__ == "__main__":
    unittest.main()
