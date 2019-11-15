import os
import unittest

import voicesep as vs


class Test(unittest.TestCase):

    def setUp(self):

        path = os.path.dirname(os.path.abspath(__file__))
        score = vs.Score(f"{path}/test.musicxml")
        note = score[0][0]

        name = "".join(part.title() for part in self._testMethodName.split("_")[1:])
        feature = getattr(vs.separators.neural.network.features.note_level, name)

        self.data = feature.generate(note)

    def test_chord_position(self):

        data = [0] * vs.separators.neural.network.features.constants.MAX_CHORD_LENGTH
        data[0] = 1

        self.assertEqual(self.data, data)


if __name__ == "__main__":
    unittest.main()
