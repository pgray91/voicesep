import unittest

import voicesep as vs


class Test(unittest.TestCase):

    def setUp(self):

        name = self._testMethodName
        sheet = "{}.musicxml".format(name)

        score = vs.Score(name, sheet)
        assignments = score.separate(one_to_many=True)

        self.active_voices = vs.ActiveVoices()
        for assignment in assignments:
            self.active_voices.insert(assignment)

        self.voices = [voice for assignment in assignments for voice in assignment]

    def test_insertion_simple(self):

        expected_order = [
            self.voices[2],
            self.voices[4],
            self.voices[0],
            self.voices[1],
            self.voices[5],
            self.voices[3]
        ]
        true_order = list(self.active_voices)

        self.assertEqual(expected_order, true_order)

    def test_insertion_crossing_voice(self):

        expected_order = [
            self.voices[0],
            self.voices[1],
            self.voices[5],
            self.voices[4],
            self.voices[6],
            self.voices[3],
            self.voices[2]
        ]
        true_order = list(self.active_voices)
         
        self.assertEqual(expected_order, true_order)

    def test_insertion_empty_voice(self):

        expected_order = [
            self.voices[0],
            self.voices[2],
            self.voices[4],
            self.voices[5],
            self.voices[3],
            self.voices[1]
        ]
        true_order = list(self.active_voices)

        self.assertEqual(expected_order, true_order)


if __name__ == "__main__":
    unittest.main()
