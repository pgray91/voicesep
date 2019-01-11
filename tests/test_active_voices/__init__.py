import unittest

import voicesep as vs


class Test(unittest.TestCase):

    def setUp(self):

        path = os.path.dirname(os.path.abspath(__file__))
        name = self._testMethodName
        sheet = "{}/{}.musicxml".format(path, name)

        score = vs.Score(name, sheet)
        waterfall = [
            {
                "True": {
                    "one_to_may": True
                }
            }
        ]
        beat_horizon = None

        assignments = vs.separate(score, waterfall, beat_horizon)

        self.active_voices = vs.ActiveVoices(beat_horizon)
        for assignment in assignments:
            self.active_voices.insert(assignment)

        self.voices = [voice for assignment in assignments for voice in assignment]

    def test_insertion_blocking_complex(self):

        expected_order = [
            self.voices[10],
            self.voices[5],
            self.voices[11],
            self.voices[7],
            self.voices[6],
            self.voices[0],
            self.voices[1],
            self.voices[3],
            self.voices[4],
            self.voices[2],
            self.voices[9],
            self.voices[12],
            self.voices[8]
        ]
        true_order = list(self.active_voices)

        self.assertEqual(expected_order, true_order)

    def test_insertion_blocking_simple(self):

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


    def test_insertion_convergence(self):

        expected_order = [
            self.voices[0],
            self.voices[1],
            self.voices[3],
            self.voices[2]
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

    def test_insertion_divergence(self):

        expected_order = [
            self.voices[1],
            self.voices[0],
            self.voices[2],
            self.voices[3]
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
