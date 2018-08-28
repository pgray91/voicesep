import unittest
import numpy as np
import voicesep as vs

class TestEvaluator(unittest.TestCase):

  def setUp(self):
    self.score1 = vs.Score("test_score1.xml", 4, True)
    self.score2 = vs.Score("test_score2.xml", 4, True)


    self.active_voices = vs.ActiveVoices(
      div_limit=1, 
      lookback_inc=0, lookback_proxs=(20,), allow_overlap=False
    )
    vs.envelope.separate(self.score1, self.active_voices)
    vs.envelope.separate(self.score2, self.active_voices)

    self.evaluator1 = vs.Evaluator(
      "test_results", 'w', "", 
      "envelope", many_only=False
    )
    self.evaluator1.update(self.score1)
    self.evaluator1.update(self.score2)

  def test_00_envelope_predicted_count(self):
    predicted_count = self.evaluator1.score_results[0].predicted_count
    self.assertEqual(predicted_count, 5)

  def test_01_envelope_true_count(self):
    true_count = self.evaluator1.score_results[0].true_count
    self.assertEqual(true_count, 6)

  def test_02_envelope_intersect_count(self):
    intersect_count = self.evaluator1.score_results[0].intersect_count
    self.assertEqual(intersect_count, 4)

  def test_03_envelope_precision(self):
    precision = self.evaluator1.score_results[0].precision
    self.assertEqual(precision, 0.8)

  def test_04_envelope_recall(self):
    recall = self.evaluator1.score_results[0].recall
    self.assertEqual(recall, 4 / 6)

  def test_05_envelope_jaccard_index(self):
    jaccard_index = self.evaluator1.score_results[0].jaccard_index
    self.assertEqual(jaccard_index, 4 / 7)

  def test_06_envelope_F1(self):
    F1 = self.evaluator1.score_results[0].F1
    self.assertEqual(F1, 2 * (4 / 11))

  def test_07_write(self):
    self.evaluator1.total()

  def test_08_envelope_predicted_count_MO(self):
    self.evaluator1 = vs.Evaluator(
      "test_results", 'w', "", 
      "envelope", many_only=True
    )
    self.evaluator1.update(self.score1)
    self.evaluator1.update(self.score2)

    predicted_count = self.evaluator1.score_results[0].predicted_count
    self.assertEqual(predicted_count, 3)

  def test_09_envelope_true_count_MO(self):
    self.evaluator1 = vs.Evaluator(
      "test_results", 'w', "", 
      "envelope", many_only=True
    )
    self.evaluator1.update(self.score1)
    self.evaluator1.update(self.score2)

    true_count = self.evaluator1.score_results[0].true_count
    self.assertEqual(true_count, 4)

  def test_10_envelope_intersect_count_MO(self):
    self.evaluator1 = vs.Evaluator(
      "test_results", 'w', "", 
      "envelope", many_only=True
    )
    self.evaluator1.update(self.score1)
    self.evaluator1.update(self.score2)

    intersect_count = self.evaluator1.score_results[0].intersect_count
    self.assertEqual(intersect_count, 2)

  def test_11_envelope_precision_MO(self):
    self.evaluator1 = vs.Evaluator(
      "test_results", 'w', "", 
      "envelope", many_only=True
    )
    self.evaluator1.update(self.score1)
    self.evaluator1.update(self.score2)

    precision = self.evaluator1.score_results[0].precision
    self.assertEqual(precision, 2 / 3)

  def test_12_envelope_recall_MO(self):
    self.evaluator1 = vs.Evaluator(
      "test_results", 'w', "", 
      "envelope", many_only=True
    )
    self.evaluator1.update(self.score1)
    self.evaluator1.update(self.score2)

    recall = self.evaluator1.score_results[0].recall
    self.assertEqual(recall, 2 / 4)

  def test_13_envelope_jaccard_index_MO(self):
    self.evaluator1 = vs.Evaluator(
      "test_results", 'w', "", 
      "envelope", many_only=True
    )
    self.evaluator1.update(self.score1)
    self.evaluator1.update(self.score2)

    jaccard_index = self.evaluator1.score_results[0].jaccard_index
    self.assertEqual(jaccard_index, 2 / 5)

  def test_14_envelope_F1_MO(self):
    self.evaluator1 = vs.Evaluator(
      "test_results", 'w', "", 
      "envelope", many_only=True
    )
    self.evaluator1.update(self.score1)
    self.evaluator1.update(self.score2)

    F1 = self.evaluator1.score_results[0].F1
    self.assertEqual(F1, 2 * (2 / 7))


if __name__ == "__main__":
  unittest.main()
