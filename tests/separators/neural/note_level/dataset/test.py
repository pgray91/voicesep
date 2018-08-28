import unittest
import numpy as np
import voicesep as vs

class TestDataset(unittest.TestCase):

  def setUp(self):
    self.score1 = vs.Score(
      "test_score1.xml", beat_horizon=4, is_one_to_many=True
    )
    self.score2 = vs.Score(
      "test_score2.xml", beat_horizon=4, is_one_to_many=True
    )
    self.features = vs.neural.note_level.Features()
    self.active_voices = vs.ActiveVoices(
      div_limit=0, lookback_inc=1, lookback_proxs=(20,),
      allow_overlap=True
    )


  def test_00_write(self):
    dataset = vs.neural.note_level.Dataset("test", "w")
    dataset.write(self.score1, self.active_voices, self.features)
    dataset.write(self.score2, self.active_voices, self.features)

    dataset.close()

  def test_01_write_feature_count(self):
    dataset = vs.neural.note_level.Dataset("test", "r")

    self.assertEqual(
      dataset.fp.attrs["feature_count"], self.features.COUNT
    )
    dataset.close()

  def test_02_write_score_names(self):
    dataset = vs.neural.note_level.Dataset("test", "r")

    score_names = list(sorted(dataset.fp.keys()))
    
    self.assertEqual(score_names, ["test_score1", "test_score2"])
    dataset.close()

  def test_03_write_dataset_names(self):
    dataset = vs.neural.note_level.Dataset("test", "r")

    for key in sorted(dataset.fp.keys()):
      with self.subTest(test="Score- %s" % key):
        dataset_names = list(sorted(dataset.fp[key].keys()))
        self.assertEqual(dataset_names, ["features", "labels"])

    dataset.close()

  def test_04_write_dataset_shapes(self):
    fc = self.features.COUNT
    expected_shapes = [
      (18,fc), (18,),
      (20,fc), (20,)
    ]

    dataset = vs.neural.note_level.Dataset("test", "r")

    i = 0
    for score_key in sorted(dataset.fp.keys()):
      for dataset_key in sorted(dataset.fp[score_key].keys()):
        with self.subTest(test="Score- %s, %s" % (score_key, dataset_key)):
          self.assertEqual(
            dataset.fp[score_key][dataset_key].shape, expected_shapes[i]
          )
        i += 1

    dataset.close()

  def test_05_write_dataset_values(self):
    expected_values = [
      0, (1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0),
      0, (1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0),
    ]

    dataset = vs.neural.note_level.Dataset("test", "r")

    i = 0
    for score_key in sorted(dataset.fp.keys()):
      for dataset_key in sorted(dataset.fp[score_key].keys()):
        with self.subTest(test="Score- %s, %s" % (score_key, dataset_key)):
          if dataset_key != "labels":
            self.assertEqual(
              dataset.fp[score_key][dataset_key][0,0], expected_values[i]
            )
          else:
            self.assertEqual(
              tuple(dataset.fp[score_key][dataset_key]), expected_values[i]
            )
        i += 1
    dataset.close()

  def test_06_read_dataset_shapes(self):
    fc = self.features.COUNT
    expected_shapes = [
      (38,fc), (38,),
    ]

    dataset = vs.neural.note_level.Dataset("test", "r")

    dataset.read([self.score1, self.score2])

    self.assertEqual(dataset.features.shape, expected_shapes[0])
    self.assertEqual(dataset.labels.shape, expected_shapes[1])

    dataset.close()

  def test_07_read_dataset_values(self):
    expected_values = [
      0, 
      (1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0,
       1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0
      ),
    ]

    dataset = vs.neural.note_level.Dataset("test", "r")

    dataset.read([self.score1, self.score2])

    self.assertEqual(dataset.features[0:1][0,0], expected_values[0])
    self.assertEqual(tuple(dataset.labels[:]), expected_values[1])

    dataset.close()

  def test_08_read_fp_equals_memmap(self):
    dataset = vs.neural.note_level.Dataset("test", "r")

    dataset.read([self.score1, self.score2])

    self.assertEqual(
      dataset.features[:18].tolist(), 
      dataset.fp["test_score1"]["features"][:].tolist()
    )
    self.assertEqual(
      dataset.features[18:38].tolist(), 
      dataset.fp["test_score2"]["features"][:].tolist()
    )

    self.assertEqual(
      dataset.labels[:18].tolist(), 
      dataset.fp["test_score1"]["labels"][:].tolist()
    )
    self.assertEqual(
      dataset.labels[18:38].tolist(), 
      dataset.fp["test_score2"]["labels"][:].tolist()
    )

    dataset.close()

  def test_09_read_memmap_reconstruction(self):
    dataset = vs.neural.note_level.Dataset("test", "r")

    dataset.read([self.score1, self.score2])
    reconstruct = np.empty((0, self.features.COUNT))
    for i in range(0,dataset.features.shape[0],10):
      reconstruct = np.concatenate((reconstruct, dataset.features[i:i+10]))

    self.assertEqual(
      reconstruct[:18].tolist(), 
      dataset.fp["test_score1"]["features"][:].tolist()
    )
    self.assertEqual(
      reconstruct[18:38].tolist(), 
      dataset.fp["test_score2"]["features"][:].tolist()
    )

    dataset.close()

if __name__ == "__main__":
  unittest.main()
