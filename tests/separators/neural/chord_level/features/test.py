import unittest
import numpy as np
import voicesep as vs

class TestFeatures(unittest.TestCase):

  def setUp(self):
    self.score = vs.Score(
      "test_score.xml", beat_horizon=4, is_one_to_many=True
    )

  def test_00_all_data_len(self):
    active_voices = vs.ActiveVoices(
      div_limit=0, lookback_inc=1, lookback_proxs=(20,),
      allow_overlap=True
    )
    active_voices.voiceid_type = "test"

    features = vs.neural.chord_level.Features(
      max_rows=10, assign_limit=0, random_limit=0,
      conv_limit=0, div_limit=0, pp_limit=0, 
      lookback=True, allow_cross=True, batch_size=3
    )

    for chord in self.score[:2]:
      active_voices.update(chord)

    for i, _ in enumerate(features.generate(self.score, self.score[2], active_voices)):
      data = features.release()
      with self.subTest(test="Assignment-%d" % i):
        self.assertEqual(len(data), len(features.GROUP_COUNTS) + 1)

  def test_01_all_assignments_len(self):
    expected_sizes = [10, 10, 10, 10, 10, 10, 4]

    active_voices = vs.ActiveVoices(
      div_limit=0, lookback_inc=1, lookback_proxs=(20,),
      allow_overlap=True
    )
    active_voices.voiceid_type = "test"

    features = vs.neural.chord_level.Features(
      max_rows=10, assign_limit=0, random_limit=0,
      conv_limit=0, div_limit=0, pp_limit=0, 
      lookback=True, allow_cross=True, batch_size=3
    )

    for chord in self.score[:2]:
      active_voices.update(chord)

    for i, assignments in enumerate(features.generate(self.score, self.score[2], active_voices)):
      data = features.release()
      with self.subTest(test="Assignment-%d" % i):
        self.assertEqual(len(assignments), expected_sizes[i])

  def test_02_all_each_data_len(self):
    expected_sizes = [10, 10, 10, 10, 10, 10, 4]

    active_voices = vs.ActiveVoices(
      div_limit=0, lookback_inc=1, lookback_proxs=(20,),
      allow_overlap=True
    )
    active_voices.voiceid_type = "test"

    features = vs.neural.chord_level.Features(
      max_rows=10, assign_limit=0, random_limit=0,
      conv_limit=0, div_limit=0, pp_limit=0, 
      lookback=True, allow_cross=True, batch_size=3
    )

    for chord in self.score[:2]:
      active_voices.update(chord)

    pads = features.GROUP_PADS + [1]

    for i, assignments in enumerate(features.generate(self.score, self.score[2], active_voices)):
      data = features.release()
      with self.subTest(test="Assignment-%d" % i):
        for j, d in enumerate(data):
          self.assertEqual(len(d), expected_sizes[i] * pads[j])

  def test_03_random_data_len(self):
    active_voices = vs.ActiveVoices(
      div_limit=0, lookback_inc=1, lookback_proxs=(20,),
      allow_overlap=True
    )
    features = vs.neural.chord_level.Features(
      max_rows=100, assign_limit=64, random_limit=100,
      conv_limit=0, div_limit=0, pp_limit=0, 
      lookback=True, allow_cross=True, batch_size=3
    )

    for chord in self.score[:2]:
      active_voices.update(chord)

    for i, _ in enumerate(features.generate(self.score, self.score[2], active_voices)):
      continue

    data = features.release()
    self.assertEqual(len(data), len(features.GROUP_COUNTS) + 1)

  def test_04_random_assignments_len(self):
    expected_sizes = [64]

    active_voices = vs.ActiveVoices(
      div_limit=0, lookback_inc=1, lookback_proxs=(20,),
      allow_overlap=True
    )
    features = vs.neural.chord_level.Features(
      max_rows=100, assign_limit=64, random_limit=1000,
      conv_limit=0, div_limit=0, pp_limit=0, 
      lookback=True, allow_cross=True, batch_size=3,
    )

    for chord in self.score[:2]:
      active_voices.update(chord)

    for i, assignments in enumerate(features.generate(self.score, self.score[2], active_voices)):
      with self.subTest(test="Assignment-%d" % i):
        self.assertEqual(len(assignments), expected_sizes[i])

  def test_05_random_each_data_len(self):
    active_voices = vs.ActiveVoices(
      div_limit=0, lookback_inc=1, lookback_proxs=(20,),
      allow_overlap=True
    )
    features = vs.neural.chord_level.Features(
      max_rows=500, assign_limit=100, random_limit=300,
      conv_limit=0, div_limit=0, pp_limit=0, 
      lookback=True, allow_cross=True, batch_size=3
    )

    active_voices.update(self.score[0])
    for i, assignments in enumerate(features.generate(self.score, self.score[1], active_voices)):
      continue

    active_voices.update(self.score[1])
    for i, assignments in enumerate(features.generate(self.score, self.score[2], active_voices)):
      continue

    pads = features.GROUP_PADS + [1]
    data = features.release()
    for j, d in enumerate(data):
      self.assertEqual(len(d), 200 * pads[j])

  def test_06_all_data_scaled(self):
    active_voices = vs.ActiveVoices(
      div_limit=0, lookback_inc=1, lookback_proxs=(20,),
      allow_overlap=True
    )
    active_voices.voiceid_type = "test"

    features = vs.neural.chord_level.Features(
      max_rows=64, assign_limit=0, random_limit=0,
      conv_limit=0, div_limit=0, pp_limit=0, 
      lookback=True, allow_cross=True, batch_size=3
    )

    for chord in self.score[:2]:
      active_voices.update(chord)

    for i, _ in enumerate(features.generate(self.score, self.score[2], active_voices)):
      continue

    data = features.release()
    for j, d in enumerate(data):
      with self.subTest(test="Feature Set %d" % j):
        self.assertLessEqual(np.max(d), 1)
        self.assertGreaterEqual(np.min(d), 0)

if __name__ == "__main__":
  unittest.main()
