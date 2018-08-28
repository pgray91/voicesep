import unittest
import numpy as np
import voicesep as vs

class TestAssignmentsGenerator(unittest.TestCase):

  def setUp(self):
    self.score = vs.Score(
      "test_score.xml", beat_horizon=4, is_one_to_many=True
    )

  def test_00_all_assignments_C0D0(self):
    expected_assignments = [
      [[(0,0)], [(0,1)]],
      [[], []],
      [[], [(1,0)]],
      [[], [(0,0)]],
      [[], [(0,1)]],
      [[], [(1,0), (0,0)]],
      [[], [(1,0), (0,1)]],
      [[], [(0,0), (0,1)]],
      [[], [(1,0), (0,0), (0,1)]],
      [[(1,0)], []],
      [[(1,0)], [(1,0)]],
      [[(1,0)], [(0,0)]],
      [[(1,0)], [(0,1)]],
      [[(1,0)], [(1,0), (0,0)]],
      [[(1,0)], [(1,0), (0,1)]],
      [[(1,0)], [(0,0), (0,1)]],
      [[(1,0)], [(1,0), (0,0), (0,1)]],
      [[(0,0)], []],
      [[(0,0)], [(1,0)]],
      [[(0,0)], [(0,0)]],
      [[(0,0)], [(1,0), (0,0)]],
      [[(0,0)], [(1,0), (0,1)]],
      [[(0,0)], [(0,0), (0,1)]],
      [[(0,0)], [(1,0), (0,0), (0,1)]],
      [[(0,1)], []],
      [[(0,1)], [(1,0)]],
      [[(0,1)], [(0,0)]],
      [[(0,1)], [(0,1)]],
      [[(0,1)], [(1,0), (0,0)]],
      [[(0,1)], [(1,0), (0,1)]],
      [[(0,1)], [(0,0), (0,1)]],
      [[(0,1)], [(1,0), (0,0), (0,1)]],
      [[(1,0), (0,0)], []],
      [[(1,0), (0,0)], [(1,0)]],
      [[(1,0), (0,0)], [(0,0)]],
      [[(1,0), (0,0)], [(0,1)]],
      [[(1,0), (0,0)], [(1,0), (0,0)]],
      [[(1,0), (0,0)], [(1,0), (0,1)]],
      [[(1,0), (0,0)], [(0,0), (0,1)]],
      [[(1,0), (0,0)], [(1,0), (0,0), (0,1)]],
      [[(1,0), (0,1)], []],
      [[(1,0), (0,1)], [(1,0)]],
      [[(1,0), (0,1)], [(0,0)]],
      [[(1,0), (0,1)], [(0,1)]],
      [[(1,0), (0,1)], [(1,0), (0,0)]],
      [[(1,0), (0,1)], [(1,0), (0,1)]],
      [[(1,0), (0,1)], [(0,0), (0,1)]],
      [[(1,0), (0,1)], [(1,0), (0,0), (0,1)]],
      [[(0,0), (0,1)], []],
      [[(0,0), (0,1)], [(1,0)]],
      [[(0,0), (0,1)], [(0,0)]],
      [[(0,0), (0,1)], [(0,1)]],
      [[(0,0), (0,1)], [(1,0), (0,0)]],
      [[(0,0), (0,1)], [(1,0), (0,1)]],
      [[(0,0), (0,1)], [(0,0), (0,1)]],
      [[(0,0), (0,1)], [(1,0), (0,0), (0,1)]],
      [[(1,0), (0,0), (0,1)], []],
      [[(1,0), (0,0), (0,1)], [(1,0)]],
      [[(1,0), (0,0), (0,1)], [(0,0)]],
      [[(1,0), (0,0), (0,1)], [(0,1)]],
      [[(1,0), (0,0), (0,1)], [(1,0), (0,0)]],
      [[(1,0), (0,0), (0,1)], [(1,0), (0,1)]],
      [[(1,0), (0,0), (0,1)], [(0,0), (0,1)]],
      [[(1,0), (0,0), (0,1)], [(1,0), (0,0), (0,1)]],
    ]

    active_voices = vs.ActiveVoices(
      div_limit=0, lookback_inc=1, lookback_proxs=(20,),
      allow_overlap=True
    )
    assignments_generator = vs.neural.chord_level.features.assignments_generator.AssignmentsGenerator(
      max_rows=64, assign_limit=0, random_limit=0,
      conv_limit=0, div_limit=0, pp_limit=0, 
      lookback=True, allow_cross=True
    )

    for chord in self.score[:2]:
      active_voices.update(chord)

    active_subset = active_voices.subset(self.score[2])

    assignments = next(
      assignments_generator(self.score[2], active_subset, active_voices, test_all=True)
    )

    self.assertEqual(len(assignments), 64)
    for i, assignment in enumerate(assignments):
      with self.subTest(test="Assignment-%d" % i):
        voice_names = [
          [
            (v.note.chord_index, v.note.index) for v in voices if v is not None
          ]
          for voices in assignment
        ]
        self.assertEqual(voice_names, expected_assignments[i])

  def test_01_all_assignments_C0D2(self):
    expected_assignments = [
      [[(0,0)], [(0,1)]],
      [[], []],
      [[], [(1,0)]],
      [[], [(0,0)]],
      [[], [(0,1)]],
      [[], [(1,0), (0,0)]],
      [[], [(1,0), (0,1)]],
      [[], [(0,0), (0,1)]],
      [[], [(1,0), (0,0), (0,1)]],
      [[(1,0)], []],
      [[(1,0)], [(1,0)]],
      [[(1,0)], [(0,0)]],
      [[(1,0)], [(0,1)]],
      [[(1,0)], [(1,0), (0,0)]],
      [[(1,0)], [(1,0), (0,1)]],
      [[(1,0)], [(0,0), (0,1)]],
      [[(1,0)], [(1,0), (0,0), (0,1)]],
      [[(0,0)], []],
      [[(0,0)], [(1,0)]],
      [[(0,0)], [(1,0), (0,1)]],
      [[(0,1)], []],
      [[(0,1)], [(1,0)]],
      [[(0,1)], [(0,0)]],
      [[(0,1)], [(0,1)]],
      [[(0,1)], [(1,0), (0,0)]],
      [[(0,1)], [(1,0), (0,1)]],
      [[(0,1)], [(0,0), (0,1)]],
      [[(0,1)], [(1,0), (0,0), (0,1)]],
      [[(1,0), (0,0)], []],
      [[(1,0), (0,0)], [(1,0)]],
      [[(1,0), (0,0)], [(0,1)]],
      [[(1,0), (0,0)], [(1,0), (0,1)]],
      [[(1,0), (0,1)], []],
      [[(1,0), (0,1)], [(1,0)]],
      [[(1,0), (0,1)], [(0,0)]],
      [[(1,0), (0,1)], [(0,1)]],
      [[(1,0), (0,1)], [(1,0), (0,0)]],
      [[(1,0), (0,1)], [(1,0), (0,1)]],
      [[(1,0), (0,1)], [(0,0), (0,1)]],
      [[(1,0), (0,1)], [(1,0), (0,0), (0,1)]],
      [[(0,0), (0,1)], []],
      [[(0,0), (0,1)], [(1,0)]],
      [[(0,0), (0,1)], [(0,1)]],
      [[(0,0), (0,1)], [(1,0), (0,1)]],
      [[(1,0), (0,0), (0,1)], []],
      [[(1,0), (0,0), (0,1)], [(1,0)]],
      [[(1,0), (0,0), (0,1)], [(0,1)]],
      [[(1,0), (0,0), (0,1)], [(1,0), (0,1)]],
    ]
    active_voices = vs.ActiveVoices(
      div_limit=2, lookback_inc=1, lookback_proxs=(20,),
      allow_overlap=True
    )
    assignments_generator = vs.neural.chord_level.features.assignments_generator.AssignmentsGenerator(
      max_rows=64, assign_limit=0, random_limit=0,
      conv_limit=0, div_limit=2, pp_limit=0, 
      lookback=True, allow_cross=True
    )

    for chord in self.score[:2]:
      active_voices.update(chord)

    active_subset = active_voices.subset(self.score[2])

    assignments = next(
      assignments_generator(self.score[2], active_subset, yield_true=True, test_all=True)
    )

    self.assertEqual(len(assignments), 48)
    for i, assignment in enumerate(assignments):
      with self.subTest(test="Assignment-%d" % i):
        voice_names = [
          [
            (v.note.chord_index, v.note.index) for v in voices if v is not None
          ]
          for voices in assignment
        ]
        self.assertEqual(voice_names, expected_assignments[i])

  def test_02_all_assignments_C1D2(self):
    expected_assignments = [
      [[(0,0)], [(0,1)]],
      [[], []],
      [[], [(1,0)]],
      [[], [(0,0)]],
      [[], [(0,1)]],
      [[(1,0)], []],
      [[(1,0)], [(1,0)]],
      [[(1,0)], [(0,0)]],
      [[(1,0)], [(0,1)]],
      [[(0,0)], []],
      [[(0,0)], [(1,0)]],
      [[(0,1)], []],
      [[(0,1)], [(1,0)]],
      [[(0,1)], [(0,0)]],
      [[(0,1)], [(0,1)]],
    ]

    active_voices = vs.ActiveVoices(
      div_limit=2, lookback_inc=1, lookback_proxs=(20,),
      allow_overlap=True
    )
    assignments_generator = vs.neural.chord_level.features.assignments_generator.AssignmentsGenerator(
      max_rows=64, assign_limit=0, random_limit=0,
      conv_limit=1, div_limit=2, pp_limit=0, 
      lookback=True, allow_cross=True
    )

    for chord in self.score[:2]:
      active_voices.update(chord)

    active_subset = active_voices.subset(self.score[2])

    assignments = next(
      assignments_generator(self.score[2], active_subset, yield_true=True, test_all=True)
    )

    self.assertEqual(len(assignments), 15)
    for i, assignment in enumerate(assignments):
      with self.subTest(test="Assignment-%d" % i):
        voice_names = [
          [
            (v.note.chord_index, v.note.index) for v in voices if v is not None
          ]
          for voices in assignment
        ]
        self.assertEqual(voice_names, expected_assignments[i])

  def test_03_all_assignments_C0D0PC(self):
    expected_assignments = [
      [[(0,0)], [(0,1)]],
      [[], []],
      [[], [(1,0)]],
      [[], [(0,0)]],
      [[], [(0,1)]],
      [[], [(1,0), (0,0)]],
      [[], [(1,0), (0,1)]],
      [[], [(0,0), (0,1)]],
      [[], [(1,0), (0,0), (0,1)]],
      [[(1,0)], []],
      [[(1,0)], [(1,0)]],
      [[(1,0)], [(0,0)]],
      [[(1,0)], [(0,1)]],
      [[(1,0)], [(1,0), (0,0)]],
      [[(1,0)], [(1,0), (0,1)]],
      [[(1,0)], [(0,0), (0,1)]],
      [[(1,0)], [(1,0), (0,0), (0,1)]],
      [[(0,0)], []],
      [[(0,0)], [(0,0)]],
      [[(0,0)], [(0,0), (0,1)]],
      [[(0,1)], []],
      [[(0,1)], [(0,1)]],
      [[(1,0), (0,0)], []],
      [[(1,0), (0,0)], [(0,0)]],
      [[(1,0), (0,0)], [(0,1)]],
      [[(1,0), (0,0)], [(0,0), (0,1)]],
      [[(1,0), (0,1)], []],
      [[(1,0), (0,1)], [(0,1)]],
      [[(0,0), (0,1)], []],
      [[(0,0), (0,1)], [(0,1)]],
      [[(1,0), (0,0), (0,1)], []],
      [[(1,0), (0,0), (0,1)], [(0,1)]],
    ]

    active_voices = vs.ActiveVoices(
      div_limit=0, lookback_inc=1, lookback_proxs=(20,),
      allow_overlap=True
    )
    assignments_generator = vs.neural.chord_level.features.assignments_generator.AssignmentsGenerator(
      max_rows=64, assign_limit=0, random_limit=0,
      conv_limit=0, div_limit=0, pp_limit=0, 
      lookback=True, allow_cross=False
    )

    for chord in self.score[:2]:
      active_voices.update(chord)

    active_subset = active_voices.subset(self.score[2])

    assignments = next(
      assignments_generator(self.score[2], active_subset, yield_true=True, test_all=True)
    )

    self.assertEqual(len(assignments), 32)
    for i, assignment in enumerate(assignments):
      with self.subTest(test="Assignment-%d" % i):
        voice_names = [
          [
            (v.note.chord_index, v.note.index) for v in voices if v is not None
          ]
          for voices in assignment
        ]
        self.assertEqual(voice_names, expected_assignments[i])

  def test_04_all_assignments_C0D2PC(self):
    expected_assignments = [
      [[(0,0)], [(0,1)]],
      [[], []],
      [[], [(1,0)]],
      [[], [(0,0)]],
      [[], [(0,1)]],
      [[], [(1,0), (0,0)]],
      [[], [(1,0), (0,1)]],
      [[], [(0,0), (0,1)]],
      [[], [(1,0), (0,0), (0,1)]],
      [[(1,0)], []],
      [[(1,0)], [(1,0)]],
      [[(1,0)], [(0,0)]],
      [[(1,0)], [(0,1)]],
      [[(1,0)], [(1,0), (0,0)]],
      [[(1,0)], [(1,0), (0,1)]],
      [[(1,0)], [(0,0), (0,1)]],
      [[(1,0)], [(1,0), (0,0), (0,1)]],
      [[(0,0)], []],
      [[(0,1)], []],
      [[(0,1)], [(0,1)]],
      [[(1,0), (0,0)], []],
      [[(1,0), (0,0)], [(0,1)]],
      [[(1,0), (0,1)], []],
      [[(1,0), (0,1)], [(0,1)]],
      [[(0,0), (0,1)], []],
      [[(0,0), (0,1)], [(0,1)]],
      [[(1,0), (0,0), (0,1)], []],
      [[(1,0), (0,0), (0,1)], [(0,1)]],
    ]

    active_voices = vs.ActiveVoices(
      div_limit=2, lookback_inc=1, lookback_proxs=(20,),
      allow_overlap=True
    )
    assignments_generator = vs.neural.chord_level.features.assignments_generator.AssignmentsGenerator(
      max_rows=64, assign_limit=0, random_limit=0,
      conv_limit=0, div_limit=2, pp_limit=0, 
      lookback=True, allow_cross=False
    )

    for chord in self.score[:2]:
      active_voices.update(chord)

    active_subset = active_voices.subset(self.score[2])

    assignments = next(
      assignments_generator(self.score[2], active_subset, yield_true=True, test_all=True)
    )

    self.assertEqual(len(assignments), 28)
    for i, assignment in enumerate(assignments):
      with self.subTest(test="Assignment-%d" % i):
        voice_names = [
          [
            (v.note.chord_index, v.note.index) for v in voices if v is not None
          ]
          for voices in assignment
        ]
        self.assertEqual(voice_names, expected_assignments[i])

  def test_05_all_assignments_C1D2PC(self):
    expected_assignments = [
      [[(0,0)], [(0,1)]],
      [[], []],
      [[], [(1,0)]],
      [[], [(0,0)]],
      [[], [(0,1)]],
      [[(1,0)], []],
      [[(1,0)], [(1,0)]],
      [[(1,0)], [(0,0)]],
      [[(1,0)], [(0,1)]],
      [[(0,0)], []],
      [[(0,1)], []],
      [[(0,1)], [(0,1)]],
    ]

    active_voices = vs.ActiveVoices(
      div_limit=2, lookback_inc=1, lookback_proxs=(20,),
      allow_overlap=True
    )
    assignments_generator = vs.neural.chord_level.features.assignments_generator.AssignmentsGenerator(
      max_rows=64, assign_limit=0, random_limit=0,
      conv_limit=1, div_limit=2, pp_limit=0, 
      lookback=True, allow_cross=False
    )

    for chord in self.score[:2]:
      active_voices.update(chord)

    active_subset = active_voices.subset(self.score[2])

    assignments = next(
      assignments_generator(self.score[2], active_subset, yield_true=True, test_all=True)
    )

    self.assertEqual(len(assignments), 12)
    for i, assignment in enumerate(assignments):
      with self.subTest(test="Assignment-%d" % i):
        voice_names = [
          [
            (v.note.chord_index, v.note.index) for v in voices if v is not None
          ]
          for voices in assignment
        ]
        self.assertEqual(voice_names, expected_assignments[i])

  def test_06_all_assignments_C1D1PC(self):
    expected_assignments = [
      [[(0,0)], [(0,1)]],
      [[], []],
      [[], [(1,0)]],
      [[], [(0,1)]],
      [[(1,0)], []],
      [[(1,0)], [(0,1)]],
      [[(0,1)], []],
    ]

    active_voices = vs.ActiveVoices(
      div_limit=1, lookback_inc=1, lookback_proxs=(20,),
      allow_overlap=True
    )

    assignments_generator = vs.neural.chord_level.features.assignments_generator.AssignmentsGenerator(
      max_rows=64, assign_limit=0, random_limit=0,
      conv_limit=1, div_limit=1, pp_limit=0, 
      lookback=True, allow_cross=False
    )

    for chord in self.score[:2]:
      active_voices.update(chord)

    active_subset = active_voices.subset(self.score[2])

    assignments = next(
      assignments_generator(self.score[2], active_subset, yield_true=True, test_all=True)
    )

    self.assertEqual(len(assignments), 7)
    for i, assignment in enumerate(assignments):
      with self.subTest(test="Assignment-%d" % i):
        voice_names = [
          [
            (v.note.chord_index, v.note.index) for v in voices if v is not None
          ]
          for voices in assignment
        ]
        self.assertEqual(voice_names, expected_assignments[i])

  def test_07_max_row_leftovers(self):
    active_voices = vs.ActiveVoices(
      div_limit=1, lookback_inc=1, lookback_proxs=(20,),
      allow_overlap=True
    )
    assignments_generator = vs.neural.chord_level.features.assignments_generator.AssignmentsGenerator(
      max_rows=4, assign_limit=0, random_limit=0,
      conv_limit=1, div_limit=1, pp_limit=0, 
      lookback=True, allow_cross=False
    )

    for chord in self.score[:2]:
      active_voices.update(chord)

    active_subset = active_voices.subset(self.score[2])

    ag = assignments_generator(self.score[2], active_subset, yield_true=True, test_all=True)

    assignments = next(ag)
    self.assertEqual(len(assignments), 4)

    assignments = next(ag)
    self.assertEqual(len(assignments), 3)

    with self.assertRaises(StopIteration):
      next(ag)

  def test_08_max_row_one_leftover(self):
    active_voices = vs.ActiveVoices(
      div_limit=1, lookback_inc=1, lookback_proxs=(20,),
      allow_overlap=True
    )
    assignments_generator = vs.neural.chord_level.features.assignments_generator.AssignmentsGenerator(
      max_rows=6, assign_limit=0, random_limit=0,
      conv_limit=1, div_limit=1, pp_limit=0, 
      lookback=True, allow_cross=False
    )

    for chord in self.score[:2]:
      active_voices.update(chord)

    active_subset = active_voices.subset(self.score[2])

    ag = assignments_generator(self.score[2], active_subset, yield_true=True, test_all=True)

    assignments = next(ag)
    self.assertEqual(len(assignments), 6)

    assignments = next(ag)
    self.assertEqual(len(assignments), 1)

    with self.assertRaises(StopIteration):
      next(ag)

  def test_09_max_row_no_leftovers(self):
    active_voices = vs.ActiveVoices(
      div_limit=1, lookback_inc=1, lookback_proxs=(20,),
      allow_overlap=True
    )
    assignments_generator = vs.neural.chord_level.features.assignments_generator.AssignmentsGenerator(
      max_rows=7, assign_limit=0, random_limit=0,
      conv_limit=1, div_limit=1, pp_limit=0, 
      lookback=True, allow_cross=False
    )

    for chord in self.score[:2]:
      active_voices.update(chord)

    active_subset = active_voices.subset(self.score[2])

    ag = assignments_generator(self.score[2], active_subset, yield_true=True, test_all=True)

    assignments = next(ag)
    self.assertEqual(len(assignments), 7)

    with self.assertRaises(StopIteration):
      next(ag)

  def test_10_random_assignments_C0D0(self):
    expected_assignments = [
      [[(0,0)], [(0,1)]],
      [[], []],
      [[], [(1,0)]],
      [[], [(0,0)]],
      [[], [(0,1)]],
      [[], [(1,0), (0,0)]],
      [[], [(1,0), (0,1)]],
      [[], [(0,0), (0,1)]],
      [[], [(1,0), (0,0), (0,1)]],
      [[(1,0)], []],
      [[(1,0)], [(1,0)]],
      [[(1,0)], [(0,0)]],
      [[(1,0)], [(0,1)]],
      [[(1,0)], [(1,0), (0,0)]],
      [[(1,0)], [(1,0), (0,1)]],
      [[(1,0)], [(0,0), (0,1)]],
      [[(1,0)], [(1,0), (0,0), (0,1)]],
      [[(0,0)], []],
      [[(0,0)], [(1,0)]],
      [[(0,0)], [(0,0)]],
      [[(0,0)], [(1,0), (0,0)]],
      [[(0,0)], [(1,0), (0,1)]],
      [[(0,0)], [(0,0), (0,1)]],
      [[(0,0)], [(1,0), (0,0), (0,1)]],
      [[(0,1)], []],
      [[(0,1)], [(1,0)]],
      [[(0,1)], [(0,0)]],
      [[(0,1)], [(0,1)]],
      [[(0,1)], [(1,0), (0,0)]],
      [[(0,1)], [(1,0), (0,1)]],
      [[(0,1)], [(0,0), (0,1)]],
      [[(0,1)], [(1,0), (0,0), (0,1)]],
      [[(1,0), (0,0)], []],
      [[(1,0), (0,0)], [(1,0)]],
      [[(1,0), (0,0)], [(0,0)]],
      [[(1,0), (0,0)], [(0,1)]],
      [[(1,0), (0,0)], [(1,0), (0,0)]],
      [[(1,0), (0,0)], [(1,0), (0,1)]],
      [[(1,0), (0,0)], [(0,0), (0,1)]],
      [[(1,0), (0,0)], [(1,0), (0,0), (0,1)]],
      [[(1,0), (0,1)], []],
      [[(1,0), (0,1)], [(1,0)]],
      [[(1,0), (0,1)], [(0,0)]],
      [[(1,0), (0,1)], [(0,1)]],
      [[(1,0), (0,1)], [(1,0), (0,0)]],
      [[(1,0), (0,1)], [(1,0), (0,1)]],
      [[(1,0), (0,1)], [(0,0), (0,1)]],
      [[(1,0), (0,1)], [(1,0), (0,0), (0,1)]],
      [[(0,0), (0,1)], []],
      [[(0,0), (0,1)], [(1,0)]],
      [[(0,0), (0,1)], [(0,0)]],
      [[(0,0), (0,1)], [(0,1)]],
      [[(0,0), (0,1)], [(1,0), (0,0)]],
      [[(0,0), (0,1)], [(1,0), (0,1)]],
      [[(0,0), (0,1)], [(0,0), (0,1)]],
      [[(0,0), (0,1)], [(1,0), (0,0), (0,1)]],
      [[(1,0), (0,0), (0,1)], []],
      [[(1,0), (0,0), (0,1)], [(1,0)]],
      [[(1,0), (0,0), (0,1)], [(0,0)]],
      [[(1,0), (0,0), (0,1)], [(0,1)]],
      [[(1,0), (0,0), (0,1)], [(1,0), (0,0)]],
      [[(1,0), (0,0), (0,1)], [(1,0), (0,1)]],
      [[(1,0), (0,0), (0,1)], [(0,0), (0,1)]],
      [[(1,0), (0,0), (0,1)], [(1,0), (0,0), (0,1)]],
    ]

    active_voices = vs.ActiveVoices(
      div_limit=0, lookback_inc=1, lookback_proxs=(20,),
      allow_overlap=True
    )
    assignments_generator = vs.neural.chord_level.features.assignments_generator.AssignmentsGenerator(
      max_rows=5000, assign_limit=4000, random_limit=1000,
      conv_limit=0, div_limit=0, pp_limit=0, 
      lookback=True, allow_cross=True
    )

    for chord in self.score[:2]:
      active_voices.update(chord)

    active_subset = active_voices.subset(self.score[2])

    for _ in range(50):
      assignments = next(
        assignments_generator(self.score[2], active_subset, yield_true=True, test_all=False)
      )

      unique_assignments = []
      for i, assignment in enumerate(assignments):
        with self.subTest(test="Assignment-%d" % i):
          voice_names = [
            [
              (v.note.chord_index, v.note.index) for v in voices if v is not None
            ]
            for voices in assignment
          ]
          self.assertEqual(voice_names in expected_assignments, True)

          unique_assignments.append(tuple(tuple(name) for name in voice_names))

      self.assertEqual(len(assignments), len(set(tuple(unique_assignments))))
      self.assertEqual(len(assignments), 64)

  def test_11_random_assignments_C0D2(self):
    expected_assignments = [
      [[(0,0)], [(0,1)]],
      [[], []],
      [[], [(1,0)]],
      [[], [(0,0)]],
      [[], [(0,1)]],
      [[], [(1,0), (0,0)]],
      [[], [(1,0), (0,1)]],
      [[], [(0,0), (0,1)]],
      [[], [(1,0), (0,0), (0,1)]],
      [[(1,0)], []],
      [[(1,0)], [(1,0)]],
      [[(1,0)], [(0,0)]],
      [[(1,0)], [(0,1)]],
      [[(1,0)], [(1,0), (0,0)]],
      [[(1,0)], [(1,0), (0,1)]],
      [[(1,0)], [(0,0), (0,1)]],
      [[(1,0)], [(1,0), (0,0), (0,1)]],
      [[(0,0)], []],
      [[(0,0)], [(1,0)]],
      [[(0,0)], [(1,0), (0,1)]],
      [[(0,1)], []],
      [[(0,1)], [(1,0)]],
      [[(0,1)], [(0,0)]],
      [[(0,1)], [(0,1)]],
      [[(0,1)], [(1,0), (0,0)]],
      [[(0,1)], [(1,0), (0,1)]],
      [[(0,1)], [(0,0), (0,1)]],
      [[(0,1)], [(1,0), (0,0), (0,1)]],
      [[(1,0), (0,0)], []],
      [[(1,0), (0,0)], [(1,0)]],
      [[(1,0), (0,0)], [(0,1)]],
      [[(1,0), (0,0)], [(1,0), (0,1)]],
      [[(1,0), (0,1)], []],
      [[(1,0), (0,1)], [(1,0)]],
      [[(1,0), (0,1)], [(0,0)]],
      [[(1,0), (0,1)], [(0,1)]],
      [[(1,0), (0,1)], [(1,0), (0,0)]],
      [[(1,0), (0,1)], [(1,0), (0,1)]],
      [[(1,0), (0,1)], [(0,0), (0,1)]],
      [[(1,0), (0,1)], [(1,0), (0,0), (0,1)]],
      [[(0,0), (0,1)], []],
      [[(0,0), (0,1)], [(1,0)]],
      [[(0,0), (0,1)], [(0,1)]],
      [[(0,0), (0,1)], [(1,0), (0,1)]],
      [[(1,0), (0,0), (0,1)], []],
      [[(1,0), (0,0), (0,1)], [(1,0)]],
      [[(1,0), (0,0), (0,1)], [(0,1)]],
      [[(1,0), (0,0), (0,1)], [(1,0), (0,1)]],
    ]

    active_voices = vs.ActiveVoices(
      div_limit=2, lookback_inc=1, lookback_proxs=(20,),
      allow_overlap=True
    )
    assignments_generator = vs.neural.chord_level.features.assignments_generator.AssignmentsGenerator(
      max_rows=64, assign_limit=64, random_limit=50,
      conv_limit=0, div_limit=2, pp_limit=0, 
      lookback=True, allow_cross=True
    )

    for chord in self.score[:2]:
      active_voices.update(chord)

    active_subset = active_voices.subset(self.score[2])

    for _ in range(50):
      assignments = next(
        assignments_generator(self.score[2], active_subset, yield_true=True, test_all=False)
      )

      unique_assignments = []
      for i, assignment in enumerate(assignments):
        with self.subTest(test="Assignment-%d" % i):
          voice_names = [
            [
              (v.note.chord_index, v.note.index) for v in voices if v is not None
            ]
            for voices in assignment
          ]
          self.assertEqual(voice_names in expected_assignments, True)

          unique_assignments.append(tuple(tuple(name) for name in voice_names))

      self.assertEqual(len(assignments), len(set(tuple(unique_assignments))))

  def test_12_random_assignments_C1D2(self):
    expected_assignments = [
      [[(0,0)], [(0,1)]],
      [[], []],
      [[], [(1,0)]],
      [[], [(0,0)]],
      [[], [(0,1)]],
      [[(1,0)], []],
      [[(1,0)], [(1,0)]],
      [[(1,0)], [(0,0)]],
      [[(1,0)], [(0,1)]],
      [[(0,0)], []],
      [[(0,0)], [(1,0)]],
      [[(0,1)], []],
      [[(0,1)], [(1,0)]],
      [[(0,1)], [(0,0)]],
      [[(0,1)], [(0,1)]],
    ]

    active_voices = vs.ActiveVoices(
      div_limit=2, lookback_inc=1, lookback_proxs=(20,),
      allow_overlap=True
    )
    assignments_generator = vs.neural.chord_level.features.assignments_generator.AssignmentsGenerator(
      max_rows=64, assign_limit=64, random_limit=50,
      conv_limit=1, div_limit=2, pp_limit=0, 
      lookback=True, allow_cross=True
    )

    for chord in self.score[:2]:
      active_voices.update(chord)

    active_subset = active_voices.subset(self.score[2])

    for _ in range(50):
      assignments = next(
        assignments_generator(self.score[2], active_subset, yield_true=True, test_all=False)
      )

      unique_assignments = []
      for i, assignment in enumerate(assignments):
        with self.subTest(test="Assignment-%d" % i):
          voice_names = [
            [
              (v.note.chord_index, v.note.index) for v in voices if v is not None
            ]
            for voices in assignment
          ]
          self.assertEqual(voice_names in expected_assignments, True)

          unique_assignments.append(tuple(tuple(name) for name in voice_names))

      self.assertEqual(len(assignments), len(set(tuple(unique_assignments))))

  def test_13_random_assignments_C0D0PC(self):
    expected_assignments = [
      [[(0,0)], [(0,1)]],
      [[], []],
      [[], [(1,0)]],
      [[], [(0,0)]],
      [[], [(0,1)]],
      [[], [(1,0), (0,0)]],
      [[], [(1,0), (0,1)]],
      [[], [(0,0), (0,1)]],
      [[], [(1,0), (0,0), (0,1)]],
      [[(1,0)], []],
      [[(1,0)], [(1,0)]],
      [[(1,0)], [(0,0)]],
      [[(1,0)], [(0,1)]],
      [[(1,0)], [(1,0), (0,0)]],
      [[(1,0)], [(1,0), (0,1)]],
      [[(1,0)], [(0,0), (0,1)]],
      [[(1,0)], [(1,0), (0,0), (0,1)]],
      [[(0,0)], []],
      [[(0,0)], [(0,0)]],
      [[(0,0)], [(0,0), (0,1)]],
      [[(0,1)], []],
      [[(0,1)], [(0,1)]],
      [[(1,0), (0,0)], []],
      [[(1,0), (0,0)], [(0,0)]],
      [[(1,0), (0,0)], [(0,1)]],
      [[(1,0), (0,0)], [(0,0), (0,1)]],
      [[(1,0), (0,1)], []],
      [[(1,0), (0,1)], [(0,1)]],
      [[(0,0), (0,1)], []],
      [[(0,0), (0,1)], [(0,1)]],
      [[(1,0), (0,0), (0,1)], []],
      [[(1,0), (0,0), (0,1)], [(0,1)]],
    ]

    active_voices = vs.ActiveVoices(
      div_limit=0, lookback_inc=1, lookback_proxs=(20,),
      allow_overlap=True
    )
    assignments_generator = vs.neural.chord_level.features.assignments_generator.AssignmentsGenerator(
      max_rows=64, assign_limit=64, random_limit=50,
      conv_limit=0, div_limit=0, pp_limit=0, 
      lookback=True, allow_cross=False
    )

    for chord in self.score[:2]:
      active_voices.update(chord)

    active_subset = active_voices.subset(self.score[2])

    for _ in range(50):
      assignments = next(
        assignments_generator(self.score[2], active_subset, yield_true=True, test_all=False)
      )

      unique_assignments = []
      for i, assignment in enumerate(assignments):
        with self.subTest(test="Assignment-%d" % i):
          voice_names = [
            [
              (v.note.chord_index, v.note.index) for v in voices if v is not None
            ]
            for voices in assignment
          ]
          self.assertEqual(voice_names in expected_assignments, True)

          unique_assignments.append(tuple(tuple(name) for name in voice_names))

      self.assertEqual(len(assignments), len(set(tuple(unique_assignments))))

  def test_14_random_assignments_C0D2PC(self):
    expected_assignments = [
      [[(0,0)], [(0,1)]],
      [[], []],
      [[], [(1,0)]],
      [[], [(0,0)]],
      [[], [(0,1)]],
      [[], [(1,0), (0,0)]],
      [[], [(1,0), (0,1)]],
      [[], [(0,0), (0,1)]],
      [[], [(1,0), (0,0), (0,1)]],
      [[(1,0)], []],
      [[(1,0)], [(1,0)]],
      [[(1,0)], [(0,0)]],
      [[(1,0)], [(0,1)]],
      [[(1,0)], [(1,0), (0,0)]],
      [[(1,0)], [(1,0), (0,1)]],
      [[(1,0)], [(0,0), (0,1)]],
      [[(1,0)], [(1,0), (0,0), (0,1)]],
      [[(0,0)], []],
      [[(0,1)], []],
      [[(0,1)], [(0,1)]],
      [[(1,0), (0,0)], []],
      [[(1,0), (0,0)], [(0,1)]],
      [[(1,0), (0,1)], []],
      [[(1,0), (0,1)], [(0,1)]],
      [[(0,0), (0,1)], []],
      [[(0,0), (0,1)], [(0,1)]],
      [[(1,0), (0,0), (0,1)], []],
      [[(1,0), (0,0), (0,1)], [(0,1)]],
    ]

    active_voices = vs.ActiveVoices(
      div_limit=2, lookback_inc=1, lookback_proxs=(20,),
      allow_overlap=True
    )
    assignments_generator = vs.neural.chord_level.features.assignments_generator.AssignmentsGenerator(
      max_rows=64, assign_limit=64, random_limit=50,
      conv_limit=0, div_limit=2, pp_limit=0, 
      lookback=True, allow_cross=False
    )

    for chord in self.score[:2]:
      active_voices.update(chord)

    active_subset = active_voices.subset(self.score[2])

    for _ in range(50):
      assignments = next(
        assignments_generator(self.score[2], active_subset, yield_true=True, test_all=False)
      )

      unique_assignments = []
      for i, assignment in enumerate(assignments):
        with self.subTest(test="Assignment-%d" % i):
          voice_names = [
            [
              (v.note.chord_index, v.note.index) for v in voices if v is not None
            ]
            for voices in assignment
          ]
          self.assertEqual(voice_names in expected_assignments, True)

          unique_assignments.append(tuple(tuple(name) for name in voice_names))

      self.assertEqual(len(assignments), len(set(tuple(unique_assignments))))

  def test_15_random_assignments_C1D2PC(self):
    expected_assignments = [
      [[(0,0)], [(0,1)]],
      [[], []],
      [[], [(1,0)]],
      [[], [(0,0)]],
      [[], [(0,1)]],
      [[(1,0)], []],
      [[(1,0)], [(1,0)]],
      [[(1,0)], [(0,0)]],
      [[(1,0)], [(0,1)]],
      [[(0,0)], []],
      [[(0,1)], []],
      [[(0,1)], [(0,1)]],
    ]

    active_voices = vs.ActiveVoices(
      div_limit=2, lookback_inc=1, lookback_proxs=(20,),
      allow_overlap=True
    )
    assignments_generator = vs.neural.chord_level.features.assignments_generator.AssignmentsGenerator(
      max_rows=64, assign_limit=64, random_limit=50,
      conv_limit=1, div_limit=2, pp_limit=0, 
      lookback=True, allow_cross=False
    )

    for chord in self.score[:2]:
      active_voices.update(chord)

    active_subset = active_voices.subset(self.score[2])

    for _ in range(50):
      assignments = next(
        assignments_generator(self.score[2], active_subset, yield_true=True, test_all=False)
      )

      unique_assignments = []
      for i, assignment in enumerate(assignments):
        with self.subTest(test="Assignment-%d" % i):
          voice_names = [
            [
              (v.note.chord_index, v.note.index) for v in voices if v is not None
            ]
            for voices in assignment
          ]
          self.assertEqual(voice_names in expected_assignments, True)

          unique_assignments.append(tuple(tuple(name) for name in voice_names))

      self.assertEqual(len(assignments), len(set(tuple(unique_assignments))))

  def test_16_random_assignments_C1D1PC(self):
    expected_assignments = [
      [[(0,0)], [(0,1)]],
      [[], []],
      [[], [(1,0)]],
      [[], [(0,1)]],
      [[(1,0)], []],
      [[(1,0)], [(0,1)]],
      [[(0,1)], []],
    ]

    active_voices = vs.ActiveVoices(
      div_limit=1, lookback_inc=1, lookback_proxs=(20,),
      allow_overlap=True
    )
    assignments_generator = vs.neural.chord_level.features.assignments_generator.AssignmentsGenerator(
      max_rows=64, assign_limit=64, random_limit=50,
      conv_limit=1, div_limit=1, pp_limit=0, 
      lookback=True, allow_cross=False
    )

    for chord in self.score[:2]:
      active_voices.update(chord)

    active_subset = active_voices.subset(self.score[2])

    for _ in range(50):
      assignments = next(
        assignments_generator(self.score[2], active_subset, yield_true=True, test_all=False)
      )

      unique_assignments = []
      for i, assignment in enumerate(assignments):
        with self.subTest(test="Assignment-%d" % i):
          voice_names = [
            [
              (v.note.chord_index, v.note.index) for v in voices if v is not None
            ]
            for voices in assignment
          ]
          self.assertEqual(voice_names in expected_assignments, True)

          unique_assignments.append(tuple(tuple(name) for name in voice_names))

      self.assertEqual(len(assignments), len(set(tuple(unique_assignments))))

  def test_17_empty_active_voices_all(self):
    active_voices = vs.ActiveVoices(
      div_limit=0, lookback_inc=1, lookback_proxs=(20,),
      allow_overlap=True
    )
    active_voices.voiceid_type = "test"

    assignments_generator = vs.neural.chord_level.features.assignments_generator.AssignmentsGenerator(
      max_rows=1000, assign_limit=0, random_limit=0,
      conv_limit=0, div_limit=0, pp_limit=0, 
      lookback=True, allow_cross=True
    )

    active_subset = active_voices.subset(self.score[0])

    self.assertEqual(
      [((None,), (None,))], 
      next(
        assignments_generator(self.score[0], active_subset, yield_true=False, test_all=True)
      )
    )

    active_voices.voiceid_type = "true"

    active_subset = active_voices.subset(self.score[0])

    ag = assignments_generator(self.score[0], active_subset, yield_true=True, test_all=True)
    self.assertEqual([((None,), (None,))], next(ag))

    with self.assertRaises(StopIteration):
      next(ag)

  def test_18_empty_active_voices_random(self):
    active_voices = vs.ActiveVoices(
      div_limit=0, lookback_inc=1, lookback_proxs=(20,),
      allow_overlap=True
    )
    active_voices.voiceid_type = "test"

    assignments_generator = vs.neural.chord_level.features.assignments_generator.AssignmentsGenerator(
      max_rows=1000, assign_limit=100, random_limit=10,
      conv_limit=0, div_limit=0, pp_limit=0, 
      lookback=True, allow_cross=True
    )

    active_subset = active_voices.subset(self.score[0])

    self.assertEqual(
      [((None,), (None,))], 
      next(
        assignments_generator(self.score[0], active_subset, yield_true=False, test_all=False)
      )
    )

    active_voices.voiceid_type = "true"

    active_subset = active_voices.subset(self.score[0])

    ag = assignments_generator(self.score[0], active_subset, yield_true=True, test_all=False)
    self.assertEqual([((None,), (None,))], next(ag))

    with self.assertRaises(StopIteration):
      next(ag)

  def test_19_true_generation_all(self):
    active_voices = vs.ActiveVoices(
      div_limit=0, lookback_inc=1, lookback_proxs=(20,),
      allow_overlap=True
    )

    assignments_generator = vs.neural.chord_level.features.assignments_generator.AssignmentsGenerator(
      max_rows=100, assign_limit=0, random_limit=0,
      conv_limit=0, div_limit=0, pp_limit=0, 
      lookback=True, allow_cross=True
    )

    for chord in self.score[5:7]:
      active_voices.update(chord)

    active_subset = active_voices.subset(self.score[7])

    ag = assignments_generator(self.score[7], active_subset, yield_true=True, test_all=True)

    assignments = next(ag)

    true_assignment = assignments[0]
    compare_assignment = [[], [(6,0), (5,1)], [(5,1), (5,2)]]
    breakdown = [
      [
        (v.note.chord_index, v.note.index) for v in voices if v is not None
      ]
      for voices in true_assignment
    ]
    self.assertEqual(compare_assignment, breakdown)

    for assignment in assignments[1:]:
      breakdown = [
        [
          (v.note.chord_index, v.note.index) for v in voices if v is not None
        ]
        for voices in assignment
      ]

      with self.subTest():
        self.assertNotEqual(compare_assignment, breakdown)

    for assignments in ag:
      for assignment in assignments:
        breakdown = [
          [
            (v.note.chord_index, v.note.index) for v in voices if v is not None
          ]
          for voices in assignment
        ]

        with self.subTest():
          self.assertNotEqual(compare_assignment, breakdown)

  def test_20_true_generation_random(self):
    active_voices = vs.ActiveVoices(
      div_limit=0, lookback_inc=1, lookback_proxs=(20,),
      allow_overlap=True
    )

    assignments_generator = vs.neural.chord_level.features.assignments_generator.AssignmentsGenerator(
      max_rows=10000, assign_limit=5000, random_limit=1000,
      conv_limit=0, div_limit=0, pp_limit=0, 
      lookback=True, allow_cross=True
    )

    for chord in self.score[5:7]:
      active_voices.update(chord)

    active_subset = active_voices.subset(self.score[7])

    ag = assignments_generator(self.score[7], active_subset, yield_true=True, test_all=False)

    assignments = next(ag)

    true_assignment = assignments[0]
    compare_assignment = [[], [(6,0), (5,1)], [(5,1), (5,2)]]
    breakdown = [
      [
        (v.note.chord_index, v.note.index) for v in voices if v is not None
      ]
      for voices in true_assignment
    ]
    self.assertEqual(compare_assignment, breakdown)

    for assignment in assignments[1:]:
      breakdown = [
        [
          (v.note.chord_index, v.note.index) for v in voices if v is not None
        ]
        for voices in assignment
      ]

      with self.subTest():
        self.assertNotEqual(compare_assignment, breakdown)

  def test_21_all_assignments_C1D1PC_PP2(self):
    expected_assignments = [
      [[(0,0)], [(0,1)]],
      [[], []],
      [[], [(0,1)]],
    ]

    active_voices = vs.ActiveVoices(
      div_limit=1, lookback_inc=1, lookback_proxs=(20,),
      allow_overlap=True
    )
    assignments_generator = vs.neural.chord_level.features.assignments_generator.AssignmentsGenerator(
      max_rows=64, assign_limit=0, random_limit=0,
      conv_limit=1, div_limit=1, pp_limit=2, 
      lookback=True, allow_cross=False
    )

    for chord in self.score[:2]:
      active_voices.update(chord)

    active_subset = active_voices.subset(self.score[2])

    assignments = next(
      assignments_generator(self.score[2], active_subset, yield_true=True, test_all=True)
    )

    self.assertEqual(len(assignments), 3)
    for i, assignment in enumerate(assignments):
      with self.subTest(test="Assignment-%d" % i):
        voice_names = [
          [
            (v.note.chord_index, v.note.index) for v in voices if v is not None
          ]
          for voices in assignment
        ]
        self.assertEqual(voice_names, expected_assignments[i])

  def test_22_all_assignments_C1D3PC_LB2(self):
    expected_assignments = [
      [[(0,0)], [(0,1)]],
      [[], []],
      [[], [(1,0)]],
      [[], [(0,1)]],
      [[(1,0)], []],
      [[(1,0)], [(1,0)]],
      [[(1,0)], [(0,1)]],
      [[(0,0)], []],
      [[(0,1)], []],
      [[(0,1)], [(0,1)]],
    ]

    active_voices = vs.ActiveVoices(
      div_limit=3, lookback_inc=1, lookback_proxs=(2,),
      allow_overlap=True
    )
    assignments_generator = vs.neural.chord_level.features.assignments_generator.AssignmentsGenerator(
      max_rows=64, assign_limit=0, random_limit=0,
      conv_limit=1, div_limit=3, pp_limit=0, 
      lookback=True, allow_cross=False
    )

    for chord in self.score[:2]:
      active_voices.update(chord)

    active_subset = active_voices.subset(self.score[2])

    assignments = next(
      assignments_generator(self.score[2], active_subset, yield_true=True, test_all=True)
    )

    self.assertEqual(len(assignments), 10)
    for i, assignment in enumerate(assignments):
      with self.subTest(test="Assignment-%d" % i):
        voice_names = [
          [
            (v.note.chord_index, v.note.index) for v in voices if v is not None
          ]
          for voices in assignment
        ]
        self.assertEqual(voice_names, expected_assignments[i])

  def test_23_random_assignments_C1D1PC_PP2(self):
    expected_assignments = [
      [[(0,0)], [(0,1)]],
      [[], []],
      [[], [(0,1)]],
    ]

    active_voices = vs.ActiveVoices(
      div_limit=1, lookback_inc=1, lookback_proxs=(20,),
      allow_overlap=True
    )
    assignments_generator = vs.neural.chord_level.features.assignments_generator.AssignmentsGenerator(
      max_rows=1000, assign_limit=1000, random_limit=500,
      conv_limit=1, div_limit=1, pp_limit=2, 
      lookback=True, allow_cross=False
    )

    for chord in self.score[:2]:
      active_voices.update(chord)

    active_subset = active_voices.subset(self.score[2])

    for _ in range(50):
      assignments = next(
        assignments_generator(self.score[2], active_subset, yield_true=True, test_all=False)
      )

      unique_assignments = []
      for i, assignment in enumerate(assignments):
        with self.subTest(test="Assignment-%d" % i):
          voice_names = [
            [
              (v.note.chord_index, v.note.index) for v in voices if v is not None
            ]
            for voices in assignment
          ]
          self.assertEqual(voice_names in expected_assignments, True)

          unique_assignments.append(tuple(tuple(name) for name in voice_names))

      self.assertEqual(len(assignments), len(set(tuple(unique_assignments))))
      self.assertEqual(len(assignments), 3)

  def test_24_random_assignments_C1D3PC_LB2(self):
    expected_assignments = [
      [[(0,0)], [(0,1)]],
      [[], []],
      [[], [(1,0)]],
      [[], [(0,1)]],
      [[(1,0)], []],
      [[(1,0)], [(1,0)]],
      [[(1,0)], [(0,1)]],
      [[(0,0)], []],
      [[(0,1)], []],
      [[(0,1)], [(0,1)]],
    ]

    active_voices = vs.ActiveVoices(
      div_limit=3, lookback_inc=1, lookback_proxs=(2,),
      allow_overlap=True
    )
    assignments_generator = vs.neural.chord_level.features.assignments_generator.AssignmentsGenerator(
      max_rows=1000, assign_limit=1000, random_limit=500,
      conv_limit=1, div_limit=3, pp_limit=0, 
      lookback=True, allow_cross=False
    )

    for chord in self.score[:2]:
      active_voices.update(chord)

    active_subset = active_voices.subset(self.score[2])

    for _ in range(50):
      assignments = next(
        assignments_generator(self.score[2], active_subset, yield_true=True, test_all=False)
      )

      unique_assignments = []
      for i, assignment in enumerate(assignments):
        with self.subTest(test="Assignment-%d" % i):
          voice_names = [
            [
              (v.note.chord_index, v.note.index) for v in voices if v is not None
            ]
            for voices in assignment
          ]
          self.assertEqual(voice_names in expected_assignments, True)

          unique_assignments.append(tuple(tuple(name) for name in voice_names))

      self.assertEqual(len(assignments), len(set(tuple(unique_assignments))))
      self.assertEqual(len(assignments), 10)

  def test_25_all_assignments_C0D0_POLY(self):
    expected_assignments = [
      [[(3, 0)], [(3, 1)]],
      [[], [(3, 1)]],
      [[(3, 1)], [(3, 1)]],
      [[(3, 0), (3, 1)], [(3, 1)]],
    ]

    score = vs.Score(
      "test_score2.xml", beat_horizon=4, is_one_to_many=True
    )

    active_voices = vs.ActiveVoices(
      div_limit=0, lookback_inc=1, lookback_proxs=(20,),
      allow_overlap=True
    )
    assignments_generator = vs.neural.chord_level.features.assignments_generator.AssignmentsGenerator(
      max_rows=64, assign_limit=0, random_limit=0,
      conv_limit=0, div_limit=0, pp_limit=0, 
      lookback=True, allow_cross=False
    )

    for chord in score[:5]:
      active_voices.update(chord)

    active_subset = active_voices.subset(score[5])

    assignments = next(
      assignments_generator(score[5], active_subset, active_voices, test_all=True)
    )

    self.assertEqual(len(assignments), 4)
    for i, assignment in enumerate(assignments):
      with self.subTest(test="Assignment-%d" % i):
        voice_names = [
          [
            (v.note.chord_index, v.note.index) for v in voices if v is not None
          ]
          for voices in assignment
        ]
        self.assertEqual(voice_names, expected_assignments[i])

  def test_26_random_assignments_C0D0_POLY(self):
    expected_assignments = [
      [[(3, 0)], [(3, 1)]],
      [[], [(3, 1)]],
      [[(3, 1)], [(3, 1)]],
      [[(3, 0), (3, 1)], [(3, 1)]],
    ]

    score = vs.Score(
      "test_score2.xml", beat_horizon=4, is_one_to_many=True
    )

    active_voices = vs.ActiveVoices(
      div_limit=0, lookback_inc=1, lookback_proxs=(20,),
      allow_overlap=True
    )
    assignments_generator = vs.neural.chord_level.features.assignments_generator.AssignmentsGenerator(
      max_rows=1000, assign_limit=1000, random_limit=500,
      conv_limit=0, div_limit=0, pp_limit=0, 
      lookback=True, allow_cross=False
    )

    for chord in score[:5]:
      active_voices.update(chord)

    active_subset = active_voices.subset(score[5])

    for _ in range(50):
      assignments = next(
        assignments_generator(score[5], active_subset, yield_true=True, test_all=False)
      )

      unique_assignments = []
      self.assertEqual(len(assignments), 4)
      for i, assignment in enumerate(assignments):
        with self.subTest(test="Assignment-%d" % i):
          voice_names = [
            [
              (v.note.chord_index, v.note.index) for v in voices if v is not None
            ]
            for voices in assignment
          ]
          self.assertEqual(voice_names in expected_assignments, True)

          unique_assignments.append(tuple(tuple(name) for name in voice_names))

      self.assertEqual(len(assignments), len(set(tuple(unique_assignments))))

if __name__ == "__main__":
  unittest.main()
