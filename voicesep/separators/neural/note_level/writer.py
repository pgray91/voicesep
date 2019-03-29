import numpy as np
import theano

from voicesep.separators.neural.network.features import Features
from voicesep.separators.separator import Separator


class Writer(Separator):

    def __init__(self, score, group):

        super().__init__(score)

        self.length = 0
        self.feature_count = Features.count(Features.Level.PAIR)

        self.features_dataset = group.create_dataset(
            name="input0",
            shape=(0, self.feature_count),
            maxshape=(None, self.feature_count),
            dtype=theano.config.floatX
        )

        self.labels_dataset = group.create_dataset(
            name="input1",
            shape=(0, 1),
            maxshape=(None, 1),
            dtype=np.int16
        )

    def run(self, chord, active_voices, assignment):

        features = Features(chord, active_voices)

        data = features.level(Features.Level.PAIR)

        self.length += len(data)
        self.features_dataset.resize((self.length, self.feature_count))
        self.labels_dataset.resize((self.length, 1))

        data_slice = slice(self.length - len(data), self.length)

        self.features_dataset[data_slice] = np.array(
            data, dtype=theano.config.floatX
        )

        active_count = len(active_voices) + 1
        for i, (note, voice)  in enumerate(zip(chord, assignment)):

            j = -1
            for j, active_voice in enumerate(active_voices):
                self.labels_dataset[data_slice.start + i * active_count + j] = [
                    active_voice in voice.left
                ]

            self.labels_dataset[data_slice.start + i * active_count + j + 1] = [
                len(voice.left) == 0
            ]
