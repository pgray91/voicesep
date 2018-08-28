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

  statistics = vs.Statistics(
    results_file, header, "true"
  )

  for score in scores:
    print(score.name)
    statistics.update(score, active_voices)

  statistics.total()
  statistics.close()

