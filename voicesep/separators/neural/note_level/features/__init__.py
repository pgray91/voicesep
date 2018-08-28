import theano
import numpy as np

from voicesep.separators.neural.note_level.features.levels import (
  data
)

class Features:
  COUNT = features.COUNT

  def __init__(self, interval):
    self.data = np.empty(
      (const.MAX_ACTIVE_VOICES * const.MAX_CHORD, Features.COUNT),
      dtype=theano.config.floatX
    )
    self.labels = np.empty(
      (const.MAX_ACTIVE_VOICES * const.MAX_CHORD,),
      dtype=np.int16
    )

  def generate(self, chord, active_voices):
    row = 0
    for note in chord:
      voices_found = 0
      for voice in active_subset:
        self.labels[row] = 0
        if get_labels and voice.note in note.true_pairs.left:
          voices_found += 1
          self.labels[row] = 1

        self.data[row, :] = data.generate(note, chord, voice, self.interval)

        row += 1

      self.data[row, :] = 0
      self.data[row, 0] = 1
      self.labels[row] = voices_found == 0
      row += 1

      if active_voices.voiceid_type == "true":
        assert len(note.true_pairs.left) == voices_found, (
          "%d %d %s" % (note.mc_index, note.measure_index, str([n1.name for n1 in chord]))
        )
        
    return self.data[:row, :], self.labels[:row]
