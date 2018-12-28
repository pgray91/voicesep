import theano
import numpy as np

from voicesep.separators.neural.note_level.features.levels import (
  data
)

class Features:
    COUNT = features.COUNT

    def __init__(self):

        self.data = np.empty(
            (const.MAX_ACTIVE_VOICES * const.MAX_CHORD, Features.COUNT),
            dtype=theano.config.floatX
        )

    def generate(self, chord, active_voices):

        row = 0
        for note in chord:
            for voice in active_voices:
                self.data[row, :] = data.generate(note, chord, voice)
                row += 1

            self.data[row, 1:] = 0
            self.data[row, 0] = 1
            row += 1
            
        return self.data[:row, :]
