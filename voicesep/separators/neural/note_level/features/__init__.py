import theano
import numpy as np

from voicesep.separators.neural.note_level.features.levels import (
  note_features, voice_features, pair_features
)

class Features:
  COUNT = 1 + note_features.COUNT + voice_features.COUNT + pair_features.COUNT
  MAX_ACTIVE_VOICES = 50
  MAX_CHORD = 10

  def __init__(self):
    self.data = np.empty(
      (Features.MAX_ACTIVE_VOICES * Features.MAX_CHORD, Features.COUNT),
      dtype=theano.config.floatX
    )
    self.labels = np.empty(
      (Features.MAX_ACTIVE_VOICES * Features.MAX_CHORD,),
      dtype=np.int16
    )

  def generate(self, chord, active_voices, get_labels=True):
    active_subset = active_voices.subset(chord)

    row = 0
    for note in chord:
      voices_found = 0
      for voice in active_subset:
        self.labels[row] = 0
        if get_labels and voice.note in note.true_pairs.left:
          voices_found += 1
          self.labels[row] = 1

        self.data[row, :] = (
          [0] + note_features.create(note) + 
          voice_features.create(voice) + 
          pair_features.create(note, voice, chord)
        )

        row += 1

      self.data[row, :] = 0
      self.data[row, 0] = 1
      self.labels[row] = voices_found == 0
      row += 1

      if active_voices.voiceid_type == "true":
        assert len(note.true_pairs.left) == voices_found, (
          "%d %d %s" % (note.mc_index, note.measure_index, str([n1.name for n1 in chord]))
        )
        

    # assert np.max(self.data[:row, :]) <= 1, (
    #   "%d %d %s" % (
    #     chord.mc_index, chord.measure_index, 
    #     np.unravel_index(np.argmax(self.data[:row, :]), self.data[:row, :].shape)
    #   )
    # )
    # assert np.min(self.data[:row, :]) >= 0, np.unravel_index(np.argmin(self.data[:row, :]), self.data[:row, :].shape)

    if get_labels:
      return self.data[:row, :], self.labels[:row]
    else:
      return self.data[:row, :], active_subset
