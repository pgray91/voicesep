# import logging
import os
# import sys
import unittest

import voicesep as vs

#logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

class Test(unittest.TestCase):

    RED="#FF0000"

    def setUp(self):

        path = os.path.dirname(os.path.abspath(__file__))
        name = self._testMethodName
        sheet = "{}/{}.musicxml".format(path, name)

        self.score = vs.Score(sheet)

    def test_chord_index(self):

        chord = self.score[0]
        self.assertEqual(chord.index, 0)

    def test_chord_index_second(self):

        chord = self.score[1]
        self.assertEqual(chord.index, 1)

    def test_chord_length_with_multiple_clefs(self):

        chord = self.score[0]
        self.assertEqual(len(chord), 2)

    def test_duration_after_time_signature_change(self):

        note = self.score[0][0]
        self.assertEqual(note.duration, 2)

    def test_duration_in_eighth_denomination(self):

        note = self.score[0][0]
        self.assertEqual(note.duration, 1)

    def test_duration_in_chord(self):

        chord = self.score[0]
        for note in chord:
            with self.subTest("{}".format(note)):
                self.assertEqual(note.duration, 1)

    def test_duration_in_quarter_denomination(self):

        note = self.score[0][0]
        self.assertEqual(note.duration, 1)

    def test_duration_in_split_chord(self):

        chord = self.score[0]
        for note in chord:
            with self.subTest("{}".format(note)):
                self.assertEqual(note.duration, note.index + 1)

    def test_offset(self):

        note = self.score[0][0]
        self.assertEqual(note.offset, 1)

    def test_offset_in_second_onset(self):

        note = self.score[0][0]
        self.assertEqual(note.offset, 2)

    def test_onset_after_time_signature_change(self):

        chord = self.score[0]
        self.assertEqual(chord.onset, 6)

    def test_onset_in_eighth_denomination(self):

        chord = self.score[0]
        self.assertEqual(chord.onset, 2)

    def test_onset_in_quarter_denomination(self):

        chord = self.score[0]
        self.assertEqual(chord.onset, 1)

    def test_name(self):

        self.assertEqual(self.score.name, "test_name")

    def test_note_chord_degree(self):

        note = self.score[0][0]
        self.assertEqual(note.chord_degree, 1)

    def test_note_color(self):

        note = self.score[0][0]
        self.assertEqual(note.color, Test.RED)

    def test_note_degree(self):

        note = self.score[0][0]
        self.assertEqual(note.degree, 1)

    def test_note_degree_after_scale_change(self):

        note = self.score[0][0]
        self.assertEqual(note.degree, 7)

    def test_note_index(self):

        note = self.score[0][0]
        self.assertEqual(note.index, 0)

    def test_note_index_in_chord(self):

        note = self.score[0][1]
        self.assertEqual(note.index, 1)

    def test_note_location(self):

        note = self.score[0][0]
        self.assertEqual(note.location, (1,1))

    def test_note_location_in_chord(self):

        note = self.score[0][1]
        self.assertEqual(note.location, (1,1))

    def test_note_location_in_second_chord_in_second_measure(self):

        note = self.score[2][0]
        self.assertEqual(note.location, (2,2))

    def test_note_location_following_two_tied_notes(self):

        note = self.score[1][0]
        self.assertEqual(note.location, (1,3))

    def test_note_lyric(self):

        note = self.score[0][0]
        self.assertEqual(note.lyric, ["1"])

    def test_note_lyric_in_chord(self):

        note = self.score[0][1]
        self.assertEqual(note.lyric, ["2"])

    def test_note_lyric_in_split_chord(self):

        note = self.score[0][1]
        self.assertEqual(note.lyric, ["2"])

    def test_note_with_multiple_lyrics(self):

        note = self.score[0][0]
        self.assertEqual(note.lyric, ["1", "2", "3"])

    def test_note_name(self):

        note = self.score[0][0]
        self.assertEqual(note.name, "C")

    def test_note_octave(self):

        note = self.score[0][0]
        self.assertEqual(note.octave, 4)

    def test_note_pitch(self):

        note = self.score[0][0]
        self.assertEqual(note.pitch, vs.Score.MIDDLE_C)

    def test_note_pitch_after_scale_change(self):

        note = self.score[0][0]
        self.assertEqual(note.pitch, vs.Score.MIDDLE_C + 1)

    def test_score_length_one_chord(self):

        self.assertEqual(len(self.score), 1)

    def test_score_length_two_chords(self):

        self.assertEqual(len(self.score), 2)

    def test_score_length_with_tied_notes(self):

        self.assertEqual(len(self.score), 2)

    def test_score_note_count_with_graces_ties_and_multiple_clefs(self):

        self.assertEqual(sum(len(chord) for chord in self.score), 3)

    def test_stacatto(self):

        note = self.score[0][0]
        self.assertEqual(note.duration, 0.5)

    def test_stacatto_in_chord(self):

        chord = self.score[0]
        for note in chord:
            with self.subTest("{}".format(note)):
                self.assertEqual(note.duration, 0.5)

    def test_stacatto_in_split_chord(self):

        chord = self.score[0]
        for note in chord:
            with self.subTest("{}".format(note)):
                self.assertEqual(note.duration, 0.5)

    def test_tied_chord(self):

        chord = self.score[0]
        for note in chord:
            with self.subTest("{}".format(note)):
                self.assertEqual(note.duration, 2)

    def test_tied_split_chord(self):

        chord = self.score[0]
        for note in chord:
            with self.subTest("{}".format(note)):
                self.assertEqual(note.duration, 2)

    def test_tied_duration(self):

        note = self.score[0][0]
        self.assertEqual(note.duration, 2)

    def test_tied_duration_with_three_notes(self):

        note = self.score[0][0]
        self.assertEqual(note.duration, 3)

    def test_tied_note_count(self):

        self.assertEqual(len(self.score), 1)

    def test_tied_notes_in_succession(self):

        note1 = self.score[0][0]
        note2 = self.score[1][0]

        with self.subTest("{}".format(note1)):
            self.assertEqual(note1.duration, 2)

        with self.subTest("{}".format(note2)):
            self.assertEqual(note2.duration, 4)


if __name__ == "__main__":
    unittest.main()
