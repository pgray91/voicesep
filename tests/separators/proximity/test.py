import unittest
import numpy as np
import voicesep as vs

class TestProximity(unittest.TestCase):

  def setUp(self):
    self.score = vs.Score("test_score.xml", 4, True)
    self.active_voices = vs.ActiveVoices(
      div_limit=1, 
      lookback_inc=0, lookback_proxs=(20,), allow_overlap=False
    )
    

  def test_00_proximity(self):
    expected_pairs = [
      (), (), (), (),
      (0,0),
      (1,0), (0,1), (0,2),
      (2,1), (),
      (3,0), (3,1), (0,3), 
      (2,0), (4,0), (2,2), (4,2), (),
      (5,0), (4,1),
      (6,0), 
      (7,0), ()
    ]

    vs.proximity.separate(self.score, self.active_voices)

    i = 0
    for chord in self.score:
      for note in chord:
        with self.subTest(test="Assignment-%d" % i):
          res = ()
          if len(note.proximity_pairs.left) > 0:
            lp = note.proximity_pairs.left[0]
            res = (lp.chord_index, lp.index)
          self.assertEqual(res, expected_pairs[i])
        i += 1

if __name__ == "__main__":
  unittest.main()
