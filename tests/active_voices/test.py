import unittest
import voicesep as vs

# Voices above and below

class TestActiveVoices(unittest.TestCase):

  def test_00_voice_index_update_filter(self):
    expected_voice_names = [
      # Measure 0 - Chord Index 0
      [(0,0), (0,1), (0,2), (0,3), (0,4)],
      [(1,0), (0,0), (1,1), (0,1), (1,2), (0,2), (1,3), (0,3), (1,4), (0,4)],
      [(2,0), (1,0), (0,0), (2,1), (1,1), (0,1), (2,2), (1,2), (0,2), (2,3), 
       (1,3), (0,3), (2,4), (1,4), (0,4)],
      [(3,0), (2,0), (1,0), (0,0), (2,1), (1,1), (0,1), (2,2), (3,1), (1,2), 
       (0,2), (2,3), (1,3), (0,3), (2,4), (1,4), (0,4)],

      # Measure 1 - Chord Index 4
      [(3,0), (2,0), (1,0), (0,0), (4,0), (2,1), (1,1), (0,1), (2,2), (3,1), 
       (1,2), (0,2), (2,3), (4,1), (1,3), (0,3), (2,4), (1,4), (0,4)],
      [(3,0), (2,0), (1,0), (0,0), (4,0), (2,1), (1,1), (0,1), (2,2), (3,1),
       (1,2), (0,2), (2,3), (4,1), (1,3), (0,3), (2,4), (5,0), (1,4), (0,4)],

      # Measure 3 - Chord Index 6
      [(6,0), (6,1)],
      [(6,0), (7,0), (6,1)],
      [(6,0), (8,0), (7,0), (6,1)],
      [(6,0), (9,0), (8,0), (9,1), (7,0), (6,1), (9,2)],

      # Measure 4 - Chord Index 10
      [(6,0), (9,0), (10,0), (8,0), (9,1), (10,1), (7,0), (6,1), (9,2), (10,2)],
      [(6,0), (9,0), (10,0), (8,0), (9,1), (10,1), (7,0), (6,1), (9,2), (11,0),
       (10,2)],

      # Measure 6 - Chord Index 12
      [(10,0), (12,0)],

      # Measure 8 - Chord Index 13
      [(13,0), (13,1), (13,2), (13,3)],
      [(13,0), (14,0), (13,1), (13,2), (14,1), (13,3)],
      [(13,0), (14,0), (15,0), (13,1), (13,2), (14,1), (15,1), (13,3)],
      [(13,0), (14,0), (16,0), (15,0), (13,1), (13,2), (14,1), (16,1), (16,2), 
       (15,1), (13,3), (16,3)],
      [(13,0), (14,0), (16,0), (17,0), (15,0), (13,1), (13,2), (14,1), (16,1),
       (17,1), (16,2), (15,1), (13,3), (16,3)],
      [(13,0), (14,0), (16,0), (18,0), (17,0), (15,0), (13,1), (13,2), (14,1),
       (16,1), (18,1), (17,1), (16,2), (15,1), (18,2), (13,3), (16,3)],
      [(13,0), (14,0), (16,0), (18,0), (19,0), (17,0), (15,0), (13,1), (13,2),
       (14,1), (16,1), (19,1), (18,1), (17,1), (16,2), (15,1), (19,2), (18,2),
       (13,3), (19,3), (16,3)],
      [(20,0), (13,0), (14,0), (16,0), (18,0), (19,0), (17,0), (15,0), (13,1),
       (13,2), (14,1), (16,1), (19,1), (18,1), (17,1), (16,2), (15,1), (19,2), 
       (18,2), (13,3), (19,3), (16,3)],
      [(20,0), (13,0), (14,0), (16,0), (18,0), (19,0), (21,0), (17,0), (15,0), 
       (13,1), (13,2), (14,1), (16,1), (19,1), (18,1), (17,1), (16,2), (15,1), 
       (19,2), (18,2), (13,3), (19,3), (16,3)],
      [(20,0), (13,0), (14,0), (16,0), (18,0), (19,0), (22,0), (21,0), (17,0), 
       (15,0), (13,1), (13,2), (14,1), (16,1), (19,1), (18,1), (17,1), (16,2), 
       (15,1), (19,2), (18,2), (13,3), (19,3), (16,3)],

      # Measure 11 - Chord Index 23
      [(23,0), (23,1), (23,2), (23,3)],
      [(23,0), (24,0), (23,1), (24,1), (24,2), (23,2), (24,3), (23,3)],
      [(23,0), (24,0), (25,0), (25,1), (23,1), (24,1), (24,2), (23,2), (24,3),
       (23,3)],
      [(23,0), (24,0), (25,0), (26,0), (25,1), (26,1), (23,1), (24,1), (24,2), 
       (23,2), (24,3), (23,3)],

      # Measure 13 - Chord Index 27
      [(27,0), (27,1), (27,2), (27,3)],
      [(27,0), (28,0), (27,1), (27,2), (28,1), (27,3)],
      [(27,0), (28,0), (29,0), (27,1), (27,2), (28,1), (29,1), (27,3)],
      [(27,0), (28,0), (30,0), (29,0), (27,1), (27,2), (28,1), (30,1), (29,1),
       (27,3)],
      [(27,0), (28,0), (31,0), (31,1), (30,0), (31,2), (29,0), (27,1), (27,2),
       (28,1), (30,1), (29,1), (27,3)],

      # Measure 15 - Chord Index 32
      [(32,0), (32,1), (32,2), (32,3), (32,4)],
      [(32,0), (33,0), (32,1), (33,1), (32,2), (32,3), (33,2), (32,4)],
      [(32,0), (33,0), (32,1), (33,1), (32,2), (32,3), (33,2), (34,0), (32,4)],
      [(32,0), (33,0), (32,1), (33,1), (32,2), (32,3), (33,2), (35,0), (34,0), 
       (32,4)],

      # Measure 17 - Chord Index 36
      [(36,0), (36,1), (36,2)],
      [(36,0), (37,0), (36,1), (37,1), (36,2)],
      [(36,0), (38,0), (38,1), (38,2), (37,0), (36,1), (37,1), (36,2)],

      # Measure 19 - Chord Index 39
      [(39,0), (39,1), (39,2)],
      [(39,0), (39,1), (40,0), (39,2)],
      [(41,0), (41,1), (41,2), (39,0), (41,3), (41,4), (41,5), (41,6), (39,1),
       (40,0), (39,2)],
      [(41,0), (41,1), (41,2), (39,0), (41,3), (41,4), (41,5), (41,6), (39,1),
       (42,0), (40,0), (39,2)],

      # Measure 21 - Chord Index 43
      [(43,0), (43,1), (43,2)],
      [(43,0), (44,0), (44,1), (43,1), (43,2)],
      [(43,0), (45,0), (44,0), (45,1), (44,1), (43,1), (43,2)],
      [(43,0), (45,0), (46,0), (44,0), (46,1), (45,1), (44,1), (43,1), (43,2)],
      [(43,0), (45,0), (46,0), (47,0), (44,0), (46,1), (47,1), (45,1), (44,1),
       (43,1), (43,2)],
      [(43,0), (45,0), (46,0), (48,0), (47,0), (44,0), (46,1), (47,1), (48,1),
       (45,1), (44,1), (43,1)],

      # Measure 24 - Chord Index 49
      [(49,0), (49,1), (49,2)],
      [(50,0), (49,0), (49,1), (49,2)],
      [(50,0), (49,0), (51,0), (49,1), (51,1), (49,2)],
      [(52,0), (50,0), (49,0), (52,1), (51,0), (49,1), (51,1), (49,2)],

      # Measure 26 - Chord Index 53
      [(53,0), (53,1), (53,2)],
      [(54,0), (53,0), (54,1), (54,2), (53,1), (53,2)],

      # Measure 28 - Chord Index 55
      [(55,0)],
      [(56,0), (55,0), (56,1)],
    ]

    score = vs.Score("test_score.xml", 4, True)
    active_voices = vs.ActiveVoices(
      div_limit=0, lookback_inc=1, lookback_proxs=(20,), allow_overlap=True
    )

    for i, chord in enumerate(score):
      active_voices.filter(chord.beat_onset)
      active_voices.update(chord)

      with self.subTest(
        test="Measure-%d Chord-%d" % (chord.measure_index, chord.mc_index)
      ):
        voice_names = [
          (v.note.chord_index, v.note.index) for v in active_voices
        ]

        self.assertEqual(voice_names, expected_voice_names[i])

  def test_01_blocker_update(self):
    expected_voice_names = [
      # Measure 0 - Chord Index 0
      [(), (), (), (), ()],
      [(), (1,0), (), (1,1), (), (1,2), (), (1,3), (), (1,4)],
      [(), (2,0), (1,0), (), (), (1,1), (), (), (1,2), (), 
       (2,4), (1,3), (), (), (1,4)],
      [(), (), (2,0), (1,0), (), (), (1,1), (), (), (3,1), 
       (1,2), (), (2,4), (1,3), (), (), (1,4)],

      # Measure 1 - Chord Index 4
      [(), (), (2,0), (1,0), (), (), (), (1,1), (), (), 
       (3,1), (1,2), (), (), (2,4), (1,3), (4,1), (), (1,4)],
      [(), (), (2,0), (1,0), (), (), (), (1,1), (), (), 
       (3,1), (1,2), (), (), (2,4), (1,3), (4,1), (), (), (1,4)],

      # Measure 3 - Chord Index 6
      [(6,0), (6,1)],
      [(6,0), (7,0), (6,1)],
      [(6,0), (8,0), (7,0), (6,1)],
      [(6,0), (9,0), (8,0), (9,1), (7,0), (6,1), (9,2)],

      # Measure 4 - Chord Index 10
      [(6,0), (9,0), (10,0), (8,0), (9,1), (10,1), (7,0), (6,1), (9,2), (10,2)],
      [(6,0), (9,0), (10,0), (8,0), (9,1), (10,1), (7,0), (6,1), (9,2), (11,0),
       (10,2)],

      # Measure 6 - Chord Index 12
      [(10,0), (12,0)],

      # Measure 8 - Chord Index 13
      [(13,0), (13,1), (13,2), (13,3)],
      [(13,0), (14,0), (13,1), (13,2), (14,1), (13,3)],
      [(13,0), (14,0), (15,0), (13,1), (13,2), (14,1), (15,1), (13,3)],
      [(13,0), (14,0), (16,0), (15,0), (13,1), (13,2), (14,1), (16,1), (16,2), 
       (15,1), (13,3), (16,3)],
      [(13,0), (14,0), (16,0), (17,0), (15,0), (13,1), (13,2), (14,1), (16,1),
       (17,1), (16,2), (15,1), (13,3), (16,3)],
      [(13,0), (14,0), (16,0), (18,0), (17,0), (15,0), (13,1), (13,2), (14,1),
       (16,1), (18,1), (17,1), (16,2), (15,1), (18,2), (13,3), (16,3)],
      [(13,0), (14,0), (16,0), (18,0), (19,0), (17,0), (15,0), (13,1), (13,2),
       (14,1), (16,1), (19,1), (18,1), (17,1), (16,2), (15,1), (19,2), (18,2),
       (13,3), (19,3), (16,3)],
      [(20,0), (13,0), (14,0), (16,0), (18,0), (19,0), (17,0), (15,0), (13,1),
       (13,2), (14,1), (16,1), (19,1), (18,1), (17,1), (16,2), (15,1), (19,2), 
       (18,2), (13,3), (19,3), (16,3)],
      [(20,0), (13,0), (14,0), (16,0), (18,0), (19,0), (21,0), (17,0), (15,0), 
       (13,1), (13,2), (14,1), (16,1), (19,1), (18,1), (17,1), (16,2), (15,1), 
       (19,2), (18,2), (13,3), (19,3), (16,3)],
      [(20,0), (13,0), (14,0), (16,0), (18,0), (19,0), (22,0), (21,0), (17,0), 
       (15,0), (13,1), (13,2), (14,1), (16,1), (19,1), (18,1), (17,1), (16,2), 
       (15,1), (19,2), (18,2), (13,3), (19,3), (16,3)],

      # Measure 11 - Chord Index 23
      [(23,0), (23,1), (23,2), (23,3)],
      [(23,0), (24,0), (23,1), (24,1), (23,2), (24,2), (24,3), (23,3)],
      [(23,0), (24,0), (25,0), (25,1), (23,1), (24,1), (23,2), (24,2), (24,3),
       (23,3)],
      [(23,0), (24,0), (25,0), (26,0), (25,1), (26,1), (23,1), (24,1), (23,2),
       (24,2), (24,3), (23,3)],

      # Measure 13 - Chord Index 27
      [(27,0), (27,1), (27,2), (27,3)],
      [(27,0), (28,0), (27,1), (27,2), (28,1), (27,3)],
      [(27,0), (28,0), (29,0), (27,1), (27,2), (28,1), (29,1), (27,3)],
      [(27,0), (28,0), (30,0), (29,0), (27,1), (27,2), (28,1), (30,1), (29,1),
       (27,3)],
      [(27,0), (28,0), (31,0), (30,0), (31,2), (29,0), (31,1), (27,1), (27,2),
       (28,1), (30,1), (29,1), (27,3)],

      # Measure 15 - Chord Index 32
      [(32,0), (32,1), (32,2), (32,3), (32,4)],
      [(32,0), (33,0), (32,1), (33,1), (32,2), (32,3), (33,2), (32,4)],
      [(32,0), (33,0), (32,1), (33,1), (32,2), (32,3), (33,2), (34,0), (32,4)],
      [(32,0), (33,0), (32,1), (33,1), (32,2), (32,3), (33,2), (35,0), (34,0), 
       (32,4)],

      # Measure 17 - Chord Index 36
      [(36,0), (36,1), (36,2)],
      [(36,0), (37,0), (36,1), (37,1), (36,2)],
      [(36,0), (38,0), (38,2), (37,0), (38,1), (36,1), (37,1), (36,2)],

      # Measure 19 - Chord Index 39
      [(39,0), (39,1), (39,2)],
      [(39,0), (39,1), (40,0), (39,2)],
      [(41,0), (41,1), (41,2), (39,0), (41,3), (41,4), (41,5), (41,6), (39,1),
       (40,0), (39,2)],
      [(41,0), (41,1), (41,2), (39,0), (41,3), (41,4), (41,5), (41,6), (39,1),
       (42,0), (40,0), (39,2)],

      # Measure 21 - Chord Index 43
      [(43,0), (43,1), (43,2)],
      [(43,0), (44,0), (44,1), (43,1), (43,2)],
      [(43,0), (45,0), (44,0), (45,1), (44,1), (43,1), (43,2)],
      [(43,0), (45,0), (46,0), (44,0), (46,1), (45,1), (44,1), (43,1), (43,2)],
      [(43,0), (45,0), (46,0), (47,0), (44,0), (46,1), (47,1), (45,1), (44,1),
       (43,1), (43,2)],
      [(43,0), (45,0), (46,0), (48,0), (47,0), (44,0), (46,1), (47,1), (48,1),
       (45,1), (44,1), (43,1)],

      # Measure 24 - Chord Index 49
      [(49,0), (49,1), (49,2)],
      [(50,0), (49,0), (49,1), (49,2)],
      [(50,0), (49,0), (51,0), (49,1), (51,1), (49,2)],
      [(52,0), (50,0), (49,0), (52,1), (51,0), (49,1), (51,1), (49,2)],

      # Measure 26 - Chord Index 53
      [(53,0), (53,1), (53,2)],
      [(53,0), (54,2), (54,0), (53,1), (54,1), (53,2)],

      # Measure 28 - Chord Index 55
      [(55,0)],
      [(56,0), (55,0), (56,1)],
    ]

    score = vs.Score("test_score.xml", 4, True)
    active_voices = vs.ActiveVoices(
      div_limit=0, lookback_inc=1, lookback_proxs=(20,), allow_overlap=True
    )

    for i, chord in enumerate(score[:6]):
      active_voices.filter(chord.beat_onset)
      active_voices.update(chord)

      with self.subTest(
        test="Measure-%d Chord-%d" % (chord.measure_index, chord.mc_index)
      ):
        voice_names = [
          () if v.blocker is None else 
          (v.blocker.note.chord_index, v.blocker.note.index) 
          for v in active_voices
        ]

        self.assertEqual(voice_names, expected_voice_names[i])

  # FILL THIS UP
  def test_02_blocked_update(self):
    expected_voice_names = [
      # Measure 0 - Chord Index 0
      [False, False, False, False, False],
      [False, True, False, True, False, True, False, True, False, True],
      [False, True, True, False, False, True, False, False, True, False,
       True, True, False, False, True],
      [False, False, True, True, False, False, True, False, False, True,
       True, False, True, True, False, False, True],

      # Measure 1 - Chord Index 4
      [False, False, True, True, False, False, False, True, False, False,
       True, True, False, False, True, True, True, False, True],
      [False, False, True, True, False, False, False, True, False, False,
       True, True, False, False, True, True, True, False, False, True],
    ]

    score = vs.Score("test_score.xml", 4, True)
    active_voices = vs.ActiveVoices(
      div_limit=0, 
      lookback_inc=1, lookback_proxs=(20,), allow_overlap=True
    )

    for i, chord in enumerate(score[:6]):
      active_voices.filter(chord.beat_onset)
      active_voices.update(chord)

      with self.subTest(
        test="Measure-%d Chord-%d" % (chord.measure_index, chord.mc_index)
      ):
        voice_names = [v.blocked for v in active_voices]

        self.assertEqual(voice_names, expected_voice_names[i])


  def test_03_crossers_update_t3(self):
    expected_voice_names = [
      # Measure 0 - Chord Index 0
      [(), ()],
      [(1,1), (), (1,0), ()],
      [(), (1, 1), (), (1, 0), (), ()],
      [(3, 1), (), (3, 0), (1, 1), (), (1, 0), (), ()] 
    ]

    score = vs.Score("test_score3.xml", 4, True)
    active_voices = vs.ActiveVoices(
     div_limit=0, 
      lookback_inc=1, lookback_proxs=(20,), allow_overlap=True
    )

    for i, chord in enumerate(score):
      active_voices.filter(chord.beat_onset)
      active_voices.update(chord)

      with self.subTest(
        test="Measure-%d Chord-%d" % (chord.measure_index, chord.mc_index)
      ):
        voice_names = [
          () if len(v.crossers) == 0 else 
          (v.crossers[0].note.chord_index, v.crossers[0].note.index) 
          for v in active_voices
        ]

        self.assertEqual(voice_names, expected_voice_names[i])

  def test_04_div_count_update_t4(self):
    expected_voice_names = [
      # Measure 0 - Chord Index 0
      [0, 0, 0],
      [1, 0, 2, 0, 1],
      [1, 1, 0, 3, 1, 0, 2]
    ]

    score = vs.Score("test_score4.xml", 4, True)
    active_voices = vs.ActiveVoices(
      div_limit=0, 
      lookback_inc=1, lookback_proxs=(20,), allow_overlap=True
    )

    for i, chord in enumerate(score):
      active_voices.filter(chord.beat_onset)
      active_voices.update(chord)

      with self.subTest(
        test="Measure-%d Chord-%d" % (chord.measure_index, chord.mc_index)
      ):
        voice_names = [v.div_count for v in active_voices]

        self.assertEqual(voice_names, expected_voice_names[i])

  def test_05_index_update_t4(self):
    expected_voice_names = [
      # Measure 0 - Chord Index 0
      [0, 0, 0],
      [1, 0, 1, 0, 1],
      [2, 1, 0, 2, 1, 0, 2]
    ]

    score = vs.Score("test_score4.xml", 4, True)
    active_voices = vs.ActiveVoices(
      div_limit=0, 
      lookback_inc=1, lookback_proxs=(20,), allow_overlap=True
    )

    for i, chord in enumerate(score):
      active_voices.filter(chord.beat_onset)
      active_voices.update(chord)

      with self.subTest(
        test="Measure-%d Chord-%d" % (chord.measure_index, chord.mc_index)
      ):
        voice_names = [v.position for v in active_voices]

        self.assertEqual(voice_names, expected_voice_names[i])

  def test_06_length_update_t4(self):
    expected_voice_names = [
      # Measure 0 - Chord Index 0
      [1, 1, 1],
      [1, 2, 1, 2, 1],
      [1, 2, 3, 1, 2, 2, 1]
    ]

    score = vs.Score("test_score4.xml", 4, True)
    active_voices = vs.ActiveVoices(
      div_limit=0, 
      lookback_inc=1, lookback_proxs=(20,), allow_overlap=True
    )

    for i, chord in enumerate(score):
      active_voices.filter(chord.beat_onset)
      active_voices.update(chord)

      with self.subTest(
        test="Measure-%d Chord-%d" % (chord.measure_index, chord.mc_index)
      ):
        voice_names = [v.length for v in active_voices]

        self.assertEqual(voice_names, expected_voice_names[i])

  def test_07_note_count_update_t4(self):
    expected_voice_names = [
      # Measure 0 - Chord Index 0
      [1, 1, 1],
      [1, 3, 1, 3, 1],
      [1, 3, 6, 1, 3, 2, 1]
    ]

    score = vs.Score("test_score4.xml", 4, True)
    active_voices = vs.ActiveVoices(
      div_limit=0, 
      lookback_inc=1, lookback_proxs=(20,), allow_overlap=True
    )

    for i, chord in enumerate(score):
      active_voices.filter(chord.beat_onset)
      active_voices.update(chord)

      with self.subTest(
        test="Measure-%d Chord-%d" % (chord.measure_index, chord.mc_index)
      ):
        voice_names = [v.note_count for v in active_voices]

        self.assertEqual(voice_names, expected_voice_names[i])

  def test_08_avg_pitch_space_update_t4(self):
    expected_voice_names = [
      # Measure 0 - Chord Index 0
      [81, 72, 57],
      [81, 79, 72, 65.33333333333333, 57],
      [81, 79, 74, 72, 65.33333333333333, 57, 57]
    ]

    score = vs.Score("test_score4.xml", 4, True)
    active_voices = vs.ActiveVoices(
      div_limit=0, 
      lookback_inc=1, lookback_proxs=(20,), allow_overlap=True
    )

    for i, chord in enumerate(score):
      active_voices.filter(chord.beat_onset)
      active_voices.update(chord)

      with self.subTest(
        test="Measure-%d Chord-%d" % (chord.measure_index, chord.mc_index)
      ):
        voice_names = [v.avg_pitch_space for v in active_voices]

        self.assertEqual(voice_names, expected_voice_names[i])

  def test_09_std_pitch_space_update_t4(self):
    expected_voice_names = [
      # Measure 0 - Chord Index 0
      [0, 0, 0],
      [0, 5.0990195135927845, 0, 6.236095644623236, 0],
      [0, 5.0990195135927845, 9.763879010584539, 0, 6.236095644623236, 0, 0]
    ]

    score = vs.Score("test_score4.xml", 4, True)
    active_voices = vs.ActiveVoices(
      div_limit=0, 
      lookback_inc=1, lookback_proxs=(20,), allow_overlap=True
    )

    for i, chord in enumerate(score):
      active_voices.filter(chord.beat_onset)
      active_voices.update(chord)

      with self.subTest(
        test="Measure-%d Chord-%d" % (chord.measure_index, chord.mc_index)
      ):
        voice_names = [v.std_pitch_space for v in active_voices]

        self.assertEqual(voice_names, expected_voice_names[i])

  def test_10_max_pitch_space_update_t4(self):
    expected_voice_names = [
      # Measure 0 - Chord Index 0
      [81, 72, 57],
      [81, 84, 72, 72, 57],
      [81, 84, 84, 72, 72, 57, 57]
    ]

    score = vs.Score("test_score4.xml", 4, True)
    active_voices = vs.ActiveVoices(
      div_limit=0, 
      lookback_inc=1, lookback_proxs=(20,), allow_overlap=True
    )

    for i, chord in enumerate(score):
      active_voices.filter(chord.beat_onset)
      active_voices.update(chord)

      with self.subTest(
        test="Measure-%d Chord-%d" % (chord.measure_index, chord.mc_index)
      ):
        voice_names = [v.max_pitch_space for v in active_voices]

        self.assertEqual(voice_names, expected_voice_names[i])

  def test_11_min_pitch_space_update_t4(self):
    expected_voice_names = [
      # Measure 0 - Chord Index 0
      [81, 72, 57],
      [81, 72, 72, 57, 57],
      [81, 72, 57, 72, 57, 57, 57]
    ]

    score = vs.Score("test_score4.xml", 4, True)
    active_voices = vs.ActiveVoices(
      div_limit=0, 
      lookback_inc=1, lookback_proxs=(20,), allow_overlap=True
    )

    for i, chord in enumerate(score):
      active_voices.filter(chord.beat_onset)
      active_voices.update(chord)

      with self.subTest(
        test="Measure-%d Chord-%d" % (chord.measure_index, chord.mc_index)
      ):
        voice_names = [v.min_pitch_space for v in active_voices]

        self.assertEqual(voice_names, expected_voice_names[i])

  def test_12_allow_overlap_subset_t4(self):
    score = vs.Score("test_score4.xml", 4, True)
    active_voices = vs.ActiveVoices(
      div_limit=0, 
      lookback_inc=1, lookback_proxs=(30,), allow_overlap=False
    )
    active_voices.voiceid_type = "test"

    for chord in score[:-1]:
      active_voices.filter(chord.beat_onset)
      active_voices.update(chord)

    active_subset = active_voices.subset(score[-1])
    voice_names = [
      (v.note.chord_index, v.note.index) for v in active_subset
    ]

    self.assertEqual(voice_names, [(1,0), (0,1), (1,1)])

  def test_13_div_limit_subset_t4(self):
    score = vs.Score("test_score4.xml", 4, True)
    active_voices = vs.ActiveVoices(
      div_limit=2, 
      lookback_inc=1, lookback_proxs=(30,), allow_overlap=True
    )
    active_voices.voiceid_type = "test"

    for chord in score[:-1]:
      active_voices.filter(chord.beat_onset)
      active_voices.update(chord)

    active_subset = active_voices.subset(score[-1])
    voice_names = [
      (v.note.chord_index, v.note.index) for v in active_subset
    ]

    self.assertEqual(voice_names, [(1,0), (1,1), (0,2)])

  def test_14_lookback_prox2_subset_t4(self):
    score = vs.Score("test_score4.xml", 4, True)
    active_voices = vs.ActiveVoices(
      div_limit=0, 
      lookback_inc=0.5, lookback_proxs=(2,), allow_overlap=True
    )
    active_voices.voiceid_type = "test"

    for chord in score[:-1]:
      active_voices.filter(chord.beat_onset)
      active_voices.update(chord)

    active_subset = active_voices.subset(score[-1])
    voice_names = [
      (v.note.chord_index, v.note.index) for v in active_subset
    ]

    self.assertEqual(voice_names, [(1,0), (1,1), (0,2)])

    voice_proxs = [v.lookback_prox for v in active_subset]
    self.assertEqual(voice_proxs, [120, 120, 2])

  def test_15_lookback_prox20_15_10_5_subset_t4(self):
    score = vs.Score("test_score4.xml", 4, True)
    active_voices = vs.ActiveVoices(
      div_limit=0, 
      lookback_inc=0.5, lookback_proxs=(20,15,10,5), allow_overlap=True
    )

    for chord in score[:-1]:
      active_voices.filter(chord.beat_onset)
      active_voices.update(chord)

    active_subset = active_voices.subset(score[-1])
    voice_names = [
      (v.note.chord_index, v.note.index) for v in active_subset
    ]

    self.assertEqual(voice_names, [(1,0), (0,1), (1,1), (0,2)])

    voice_proxs = [v.lookback_prox for v in active_subset]
    self.assertEqual(voice_proxs, [120, 15, 120, 20])

  def test_16_position_update_t2(self):
    expected_voice_names = [
      [0, 0, 0],
      [1, 0, 1, 0],
      [2, 0, 1, 0, 2, 0],
      [3, 0, 0, 1, 2, 0, 1, 0, 3, 0],
      [4, 1, 0, 0, 2, 3, 1, 0, 2, 0, 1, 4, 0],
      [5, 1, 0, 0, 2, 4, 2, 0, 1, 3, 0, 1, 5, 0]
    ]

    score = vs.Score("test_score2.xml", 4, True)
    active_voices = vs.ActiveVoices(
      div_limit=0, 
      lookback_inc=1, lookback_proxs=(20,), allow_overlap=True
    )

    chord_index = 0
    for i, chord in enumerate(score):
      active_voices.filter(chord.beat_onset)
      active_voices.update(chord)

      with self.subTest(
        test="Measure-%d Chord-%d" % (chord.measure_index, chord_index)
      ):
        voice_names = [v.position for v in active_voices]

        self.assertEqual(voice_names, expected_voice_names[i])

      if (
        i + 1 < len(score) and
        score[i+1].measure_index != chord.measure_index
      ):
        chord_index = 0
      else:
        chord_index += 1

  def test_17_div_notes_update_t4(self):
    expected_voice_names = [
      # Measure 0 - Chord Index 0
      [[], [], []],
      [[], [(0,1)], [], [(0,1)], []],
      [[], [(0, 1)], [(0, 2), (0, 1)], [], [(0, 1)], [(0, 2)], []]
    ]

    score = vs.Score("test_score4.xml", 4, True)
    active_voices = vs.ActiveVoices(
      div_limit=0, 
      lookback_inc=1, lookback_proxs=(20,), allow_overlap=True
    )

    for i, chord in enumerate(score):
      active_voices.filter(chord.beat_onset)
      active_voices.update(chord)

      with self.subTest(
        test="Measure-%d Chord-%d" % (chord.measure_index, chord.mc_index)
      ):
        voice_names = [
          [(n.chord_index, n.index) for n in v.div_notes]
          for v in active_voices 
        ]
        self.assertEqual(voice_names, expected_voice_names[i])

  def test_18_conv_notes_update_t4(self):
    expected_voice_names = [
      # Measure 0 - Chord Index 0
      [[], [], []],
      [[], [(0, 0), (0, 1)], [], [(0, 1), (0, 2)], []],
      [[], [(0, 0), (0, 1)], [(1, 0), (0, 1), (1, 1)], [], [(0, 1), (0, 2)], [], []]
    ]

    score = vs.Score("test_score4.xml", 4, True)
    active_voices = vs.ActiveVoices(
      div_limit=0, 
      lookback_inc=1, lookback_proxs=(20,), allow_overlap=True
    )

    for i, chord in enumerate(score):
      active_voices.filter(chord.beat_onset)
      active_voices.update(chord)

      with self.subTest(
        test="Measure-%d Chord-%d" % (chord.measure_index, chord.mc_index)
      ):
        voice_names = [
          [(n.chord_index, n.index) for n in v.conv_notes]
          for v in active_voices 
        ]
        self.assertEqual(voice_names, expected_voice_names[i])

  def test_19_true_voices_in_subset_t4(self):
    score = vs.Score("test_score5.xml", 4, True)
    active_voices = vs.ActiveVoices(
      div_limit=2, 
      lookback_inc=1, lookback_proxs=(2,), allow_overlap=False
    )

    for chord in score[:-1]:
      active_voices.filter(chord.beat_onset)
      active_voices.update(chord)

    active_subset = active_voices.subset(score[-1])
    voice_names = [
      (v.note.chord_index, v.note.index) for v in active_subset
    ]

    self.assertEqual(voice_names, [(1, 0), (1, 1), (0, 1), (0, 2), (0, 3)])

  # def test_03_voice_eq(self):
  #   pass
  #
  # def test_03_crosser_filter(self):
  #   pass
  #

if __name__ == "__main__":
  unittest.main()
