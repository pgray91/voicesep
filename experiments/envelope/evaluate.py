from config import *
import voicesep as vs

if __name__ == '__main__':

  print("Reading Scores ...")
  scores =  [
    vs.Score(
      "%s%s.xml" % (score_path, score_name),
      bh, one_to_many
    )
    for score_name, bh in zip(score_list, beat_horizons)
  ]

  active_voices = vs.ActiveVoices(
    div_limit, lookback_inc, lookback_proxs, allow_overlap
  )

  evaluator = vs.Evaluator(results_file, write_mode, header, "envelope")

  for score in scores:
    print("  Testing: %s" % score.name)
    vs.envelope.separate(score, active_voices)

    evaluator.update(score)
    _, _, JI, F1 = vs.Evaluator.jaccard_index(
      **vars(evaluator.results["all"][-1])
    )
    print("    Score: %s, JI-%f, F1-%f" % (score.name, JI, F1))

    if score.name in write_score:
      print("      Writing %s" % score.name)
      score.write("%s%s.xml" % (pred_scores, score.name), "envelope")

  evaluator.total()
  evaluator.close()
