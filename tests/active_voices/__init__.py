import os
import unittest

import voicesep as vs


class Test(unittest.TestCase):

    def setUp(self):

        path = os.path.dirname(os.path.abspath(__file__))
        name = self._testMethodName
        sheet = f"{path}/{name}.musicxml"

        score = vs.Score(sheet)
        waterfall = [
            {
                "Benchmark": {
                    "one_to_many": True
                }
            }
        ]
        beat_horizon = None

        assignments = vs.separate(score, waterfall, beat_horizon)

        self.active_voices = vs.ActiveVoices(beat_horizon)
        for assignment in assignments:
            self.active_voices.insert(assignment)

        self.voices = [voice for assignment in assignments for voice in assignment]

    def test_blocked_above(self):

        voice = self.active_voices[2]
        self.assertTrue(self.active_voices.blocked(voice.note))

    def test_blocked_below(self):

        voice = self.active_voices[0]
        self.assertTrue(self.active_voices.blocked(voice.note))

    def test_blocked_same_pitch(self):

        voice = self.active_voices[2]
        self.assertTrue(self.active_voices.blocked(voice.note))

    def test_blocked_not(self):

        voice = self.active_voices[2]
        self.assertFalse(self.active_voices.blocked(voice.note))

    def test_crossing_offset(self):

        left_voice = self.active_voices[5]
        right_voice = self.active_voices[3]
        self.assertTrue(self.active_voices.crossing(left_voice.note, right_voice.note))

    def test_crossing_onset(self):

        left_voice = self.active_voices[1]
        right_voice = self.active_voices[2]
        self.assertTrue(self.active_voices.crossing(left_voice.note, right_voice.note))

    def test_crossing_single(self):

        left_voice = self.active_voices[2]
        right_voice = self.active_voices[0]
        self.assertTrue(self.active_voices.crossing(left_voice.note, right_voice.note))

    def test_crossing_not(self):

        left_voice = self.active_voices[4]
        right_voice = self.active_voices[5]
        self.assertFalse(self.active_voices.crossing(left_voice.note, right_voice.note))

    def test_deactivate(self):

        voice = self.active_voices[2]

        self.active_voices.deactivate(self.active_voices[0])
        self.active_voices.deactivate(self.active_voices[0])
        self.active_voices.deactivate(self.active_voices[1])

        with self.subTest("voice"):
            self.assertEqual(self.active_voices[0], voice)

        with self.subTest("length"):
            self.assertEqual(len(self.active_voices), 1)

        with self.subTest("inactive"):
            self.assertEqual(len(self.active_voices.inactive), 3)

    def test_filter(self):

        voice = self.active_voices[-1]

        self.active_voices.beat_horizon = 1
        self.active_voices.filter(onset=2)

        with self.subTest("voice"):
            self.assertEqual(self.active_voices[0], voice)

        with self.subTest("length"):
            self.assertEqual(len(self.active_voices), 1)

    def test_filter_inactive(self):

        voice = self.active_voices[-1]

        self.active_voices.deactivate(self.active_voices[0])

        self.active_voices.beat_horizon = 1
        self.active_voices.filter(onset=2)

        with self.subTest("voice"):
            self.assertEqual(self.active_voices[0], voice)

        with self.subTest("length"):
            self.assertEqual(len(self.active_voices), 1)

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

    def test_index(self):

        self.assertEqual(self.active_voices.index(self.voices[4]), 8)


if __name__ == "__main__":
    unittest.main()
