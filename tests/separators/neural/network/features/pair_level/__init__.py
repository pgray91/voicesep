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
        # feature = getattr(vs.separators.neural.network.features.pair_level, name)
        #
        # self.data = feature.generate(voice, active_voices)

    def test_position_difference(self):

        feature = vs.separators.neural.network.features.pair_level.PositionDifference

        note1 = vs.Note("C", 4, (0, 0), pitch=60, index=0)
        note2 = vs.Note("D", 4, (0, 0), pitch=61, index=1)
        note3 = vs.Note("E", 4, (0, 1), pitch=62, index=0)

        voice1 = vs.Voice(note1)
        voice2 = vs.Voice(note2)

        active_voices = vs.ActiveVoices()
        active_voices.insert([voice1, voice2])

        data = feature.generate(note3, voice1, active_voices)
        
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0], 1)


if __name__ == "__main__":
    unittest.main()
