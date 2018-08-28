class Evaluator:
  def __init__(
    self, results_file, write_mode, header, voiceid_type
  ):
    self.fp = open("%s.dat" % results_file, write_mode)
    self.fp.write("\n%s\n" % header)
    self.fp.write("Score, JI, Precision, Recall, F1, PC, TC, IC, Scenario\n")

    self.voiceid_type = voiceid_type
    self.results = {
        "all": [], "exclude_rests": [], 
        "joint_many": [], "true_joint_many": [], "predicted_joint_many": [],
        "joint_one": [], "true_joint_one": [], "predicted_joint_one": [],
        "many": [], "true_many": [], "predicted_many": [],
        "one": [], "true_one": [], "predicted_one": [],
    }

  def __del__(self):
    self.fp.close()

  def close(self):
    self.fp.close()

  @staticmethod
  def jaccard_index(predicted_count, true_count, intersect_count, name=""):
    precision = -1 if predicted_count == 0 else intersect_count / predicted_count
    recall = -1 if true_count == 0 else intersect_count / true_count

    jaccard_index = (
      -1 if predicted_count + true_count - intersect_count == 0 else
      intersect_count / (predicted_count + true_count - intersect_count)
    )
    F1 = (
      -1 if true_count + predicted_count == 0 else
      2 * intersect_count / (true_count + predicted_count)
    )

    return precision, recall, jaccard_index, F1

  def update(self, score):
    for scenario in self.results:
      self.results[scenario].append(
        ScoreResult(
          name = score.name, 
          predicted_count = 0, 
          true_count = 0, 
          intersect_count = 0
        )
      )

    for chord in score:
      for note in chord:
        true_pairs = note.true_pairs
        predicted_pairs = note.pairs(self.voiceid_type)

        # All
        score_result = self.results["all"][-1]
        true_left = true_pairs.left
        predicted_left = predicted_pairs.left

        score_result.true_count += len(true_left)
        score_result.predicted_count += len(predicted_left)
        score_result.intersect_count += len(set(true_left) & set(predicted_left))

        # Exclude Rests
        score_result = self.results["exclude_rests"][-1]
        true_left = [
          pair for pair in true_pairs.left 
          if note.beat_onset <= pair.beat_offset
        ]
        predicted_left = [
          pair for pair in predicted_pairs.left 
          if note.beat_onset <= pair.beat_offset
        ]

        score_result.true_count += len(true_left)
        score_result.predicted_count += len(predicted_left)
        score_result.intersect_count += len(set(true_left) & set(predicted_left))

        # Joint Many
        score_result = self.results["joint_many"][-1]
        for n in chord:
          tp = n.true_pairs
          pp = n.pairs(self.voiceid_type)

          if len(tp.left) > 1 or len(pp.left) > 1:
            true_left = true_pairs.left
            predicted_left = predicted_pairs.left
            break

          if len(tp.left) == 1 and len(tp.left[0].true_pairs.right) > 1:
            true_left = true_pairs.left
            predicted_left = predicted_pairs.left
            break

          if len(pp.left) == 1 and len(pp.left[0].pairs(self.voiceid_type).right) > 1:
            true_left = true_pairs.left
            predicted_left = predicted_pairs.left
            break
        else:
          true_left = []
          predicted_left = []

        score_result.true_count += len(true_left)
        score_result.predicted_count += len(predicted_left)
        score_result.intersect_count += len(set(true_left) & set(predicted_left))

        # True Joint Many
        score_result = self.results["true_joint_many"][-1]
        for n in chord:
          tp = n.true_pairs

          if len(tp.left) > 1:
            true_left = true_pairs.left
            predicted_left = predicted_pairs.left
            break

          if len(tp.left) == 1 and len(tp.left[0].true_pairs.right) > 1:
            true_left = true_pairs.left
            predicted_left = predicted_pairs.left
            break

        else:
          true_left = []
          predicted_left = []

        score_result.true_count += len(true_left)
        score_result.predicted_count += len(predicted_left)
        score_result.intersect_count += len(set(true_left) & set(predicted_left))

        # Predicted Joint Many
        score_result = self.results["predicted_joint_many"][-1]
        for n in chord:
          pp = n.pairs(self.voiceid_type)

          if len(pp.left) > 1:
            true_left = true_pairs.left
            predicted_left = predicted_pairs.left
            break

          if len(pp.left) == 1 and len(pp.left[0].pairs(self.voiceid_type).right) > 1:
            true_left = true_pairs.left
            predicted_left = predicted_pairs.left
            break

        else:
          true_left = []
          predicted_left = []

        score_result.true_count += len(true_left)
        score_result.predicted_count += len(predicted_left)
        score_result.intersect_count += len(set(true_left) & set(predicted_left))

        # Joint One
        score_result = self.results["joint_one"][-1]

        true_many_found = False
        for n in chord:
          tp = n.true_pairs

          if len(tp.left) == 0:
            continue

          if len(tp.left) == 1 and len(tp.left[0].true_pairs.right) == 1:
            continue

          true_many_found = True
          break

        predicted_many_found = False
        for n in chord:
          pp = n.pairs(self.voiceid_type)

          if len(pp.left) == 0:
            continue

          if len(pp.left) == 1 and len(pp.left[0].pairs(self.voiceid_type).right) == 1:
            continue

          predicted_many_found = True
          break

        if not true_many_found or not predicted_many_found:
          true_left = true_pairs.left
          predicted_left = predicted_pairs.left

        else:
          true_left = []
          predicted_left = []

        score_result.true_count += len(true_left)
        score_result.predicted_count += len(predicted_left)
        score_result.intersect_count += len(set(true_left) & set(predicted_left))

        # True Joint One
        score_result = self.results["true_joint_one"][-1]

        if not true_many_found:
          true_left = true_pairs.left
          predicted_left = predicted_pairs.left

        else:
          true_left = []
          predicted_left = []

        score_result.true_count += len(true_left)
        score_result.predicted_count += len(predicted_left)
        score_result.intersect_count += len(set(true_left) & set(predicted_left))

        # Predicted Joint One
        score_result = self.results["predicted_joint_one"][-1]

        if not predicted_many_found:
          true_left = true_pairs.left
          predicted_left = predicted_pairs.left

        else:
          true_left = []
          predicted_left = []

        score_result.true_count += len(true_left)
        score_result.predicted_count += len(predicted_left)
        score_result.intersect_count += len(set(true_left) & set(predicted_left))

        # Many
        score_result = self.results["many"][-1]
        if len(true_pairs.left) > 1 or len(predicted_pairs.left) > 1:
          true_left = true_pairs.left
          predicted_left = predicted_pairs.left

        elif (
          len(true_pairs.left) == 1 and
          len(true_pairs.left[0].true_pairs.right) > 1
        ):
          true_left = true_pairs.left
          predicted_left = predicted_pairs.left

        elif (
          len(predicted_pairs.left) == 1 and
          len(predicted_pairs.left[0].pairs(self.voiceid_type).right) > 1
        ):
          true_left = true_pairs.left
          predicted_left = predicted_pairs.left
       
        else:
          true_left = []
          predicted_left = []

        score_result.true_count += len(true_left)
        score_result.predicted_count += len(predicted_left)
        score_result.intersect_count += len(set(true_left) & set(predicted_left))

        # True Many
        score_result = self.results["true_many"][-1]
        if len(true_pairs.left) > 1:
          true_left = true_pairs.left
          predicted_left = predicted_pairs.left

        elif (
          len(true_pairs.left) == 1 and
          len(true_pairs.left[0].true_pairs.right) > 1
        ):
          true_left = true_pairs.left
          predicted_left = predicted_pairs.left
       
        else:
          true_left = []
          predicted_left = []

        score_result.true_count += len(true_left)
        score_result.predicted_count += len(predicted_left)
        score_result.intersect_count += len(set(true_left) & set(predicted_left))

        # Predicted Many
        score_result = self.results["predicted_many"][-1]
        if len(predicted_pairs.left) > 1:
          true_left = true_pairs.left
          predicted_left = predicted_pairs.left

        elif (
          len(predicted_pairs.left) == 1 and
          len(predicted_pairs.left[0].pairs(self.voiceid_type).right) > 1
        ):
          true_left = true_pairs.left
          predicted_left = predicted_pairs.left
       
        else:
          true_left = []
          predicted_left = []

        score_result.true_count += len(true_left)
        score_result.predicted_count += len(predicted_left)
        score_result.intersect_count += len(set(true_left) & set(predicted_left))

        # One
        score_result = self.results["one"][-1]
        if len(true_pairs.left) == 0 or len(predicted_pairs.left) == 0:
          true_left = true_pairs.left
          predicted_left = predicted_pairs.left

        elif (
          len(true_pairs.left) == 1 and
          len(true_pairs.left[0].true_pairs.right) == 1
        ):
          true_left = true_pairs.left
          predicted_left = predicted_pairs.left

        elif (
          len(predicted_pairs.left) == 1 and
          len(predicted_pairs.left[0].pairs(self.voiceid_type).right) == 1
        ):
          true_left = true_pairs.left
          predicted_left = predicted_pairs.left

        else:
          true_left = []
          predicted_left = []

        score_result.true_count += len(true_left)
        score_result.predicted_count += len(predicted_left)
        score_result.intersect_count += len(set(true_left) & set(predicted_left))

        # True One
        score_result = self.results["true_one"][-1]
        if len(true_pairs.left) == 0:
          true_left = true_pairs.left
          predicted_left = predicted_pairs.left

        elif (
          len(true_pairs.left) == 1 and
          len(true_pairs.left[0].true_pairs.right) == 1
        ):
          true_left = true_pairs.left
          predicted_left = predicted_pairs.left

        else:
          true_left = []
          predicted_left = []

        score_result.true_count += len(true_left)
        score_result.predicted_count += len(predicted_left)
        score_result.intersect_count += len(set(true_left) & set(predicted_left))

        # Predicted One
        score_result = self.results["predicted_one"][-1]
        if len(predicted_pairs.left) == 0:
          true_left = true_pairs.left
          predicted_left = predicted_pairs.left

        elif (
          len(predicted_pairs.left) == 1 and
          len(predicted_pairs.left[0].pairs(self.voiceid_type).right) == 1
        ):
          true_left = true_pairs.left
          predicted_left = predicted_pairs.left

        else:
          true_left = []
          predicted_left = []

        score_result.true_count += len(true_left)
        score_result.predicted_count += len(predicted_left)
        score_result.intersect_count += len(set(true_left) & set(predicted_left))

  def total(self):
    for scenario in self.results:
      for score_result in self.results[scenario]:
        precision, recall, jaccard_index, F1 = Evaluator.jaccard_index(
          **vars(score_result)
        )
        self.fp.write(
          "%s, %f, %f, %f, %f, %d, %d, %d, %s\n" % (
            score_result.name,
            jaccard_index, precision, recall, F1,
            score_result.predicted_count, score_result.true_count,
            score_result.intersect_count, scenario
          )
        )

      tot_predicted_count = sum(
        sr.predicted_count for sr in self.results[scenario]
      )
      tot_true_count = sum(
        sr.true_count for sr in self.results[scenario]
      )
      tot_intersect_count = sum(
        sr.intersect_count for sr in self.results[scenario]
      )

      tot_precision, tot_recall, tot_jaccard_index, tot_F1 = (
        Evaluator.jaccard_index(
          tot_predicted_count, tot_true_count, tot_intersect_count
        )
      )

      self.fp.write("\nJI, Precision, Recall, F1, PC, TC, IC, Scenario\n")
      self.fp.write(
        "%f, %f, %f, %f, %d, %d, %d, %s\n\n" % (
          tot_jaccard_index, tot_precision, tot_recall, tot_F1,
          tot_predicted_count, tot_true_count, tot_intersect_count,
          scenario
        )
      )

class ScoreResult():
  def __init__(self, **kwargs):
    for key, value in kwargs.items():
      setattr(self, key, value)
