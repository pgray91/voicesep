import voicesep as vs
from config import *

if __name__ == '__main__':
  active_voices = vs.ActiveVoices(
    div_limit, lookback_inc, lookback_proxs, allow_overlap
  )
  features = vs.neural.note_level.Features()
  dataset = vs.neural.note_level.Dataset(dataset_file, "w")

  for score_name, bh in zip(score_list, beat_horizons):
    print(score_name)

    score = vs.Score(
      "%s%s.xml" % (score_path, score_name), 
      bh, one_to_many
    )
    dataset.write(score, active_voices, features)

  dataset.close()
