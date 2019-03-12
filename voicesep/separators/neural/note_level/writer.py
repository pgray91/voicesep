import numpy as np

from voicesep.separators.neural.network.features import Features


class Writer(Separator):

    def __init__(self, score, group):

        super().__init__(score)

        self.group = group
        self.length = 0

        self.feature_count = Features.count(Features.Level.PAIR)

        self.features_dataset = self.group.create_dataset(
            name="input0",
            shape=(0, self.feature_count),
            maxshape=(None, self.feature_count),
            dtype=theano.config.floatX
        )

        self.labels_dataset = self.group.create_dataset(
            name="input1",
            shape=(0, 1),
            maxshape=(None, 1),
            dtype=np.int16
        )

    def __del__(self):

        self.features_dataset.resize((self.length, self.feature_count))
        self.labels_dataset.resize((self.length, 1))

    def run(self, chord, active_voices, assignment):

        features = Features(chord, active_voices)

        data = features.level(Features.Level.PAIR)

        self.length += len(data)
        if self.features_dataset.len() <= self.length:
            self.features_dataset.resize((self.length * 2, self.features_count))
            self.labels_dataset.resize((self.length * 2, 1))

        self.features_dataset[self.length - len(data):self.length] = data

        labels_slice = self.labels_dataset[self.length - len(data):self.length]
        for i, note, voice  in enumerate(zip(chord, assignment)):
            for j, active_voice in enumerate(active_voices):
                labels_slice[i * len(active_voices) + j][0] = active_voice in voice.left

            labels_slice[i * len(active_voices) + j + 1][0] = len(voice.left) == 0
