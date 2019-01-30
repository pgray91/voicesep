import numpy as np

from voicesep.separators.neural.note_level import features


class Writer(Separator):

    def __init__(self, score, group):

        super().__init__(score)

        self.group = group
        self.length = 0

        self.features_dataset = self.group.create_dataset(
            name="features",
            shape=(0, features.count()),
            maxshape=(None, features.count()),
            dtype=theano.config.floatX
        )

        self.labels_dataset = self.group.create_dataset(
            name="labels",
            shape=(0,),
            maxshape=(None,),
            dtype=np.int16
        )

    def __del__(self):

        self.features_dataset.resize((self.length, features.count()))
        self.labels_dataset.resize((self.length,))

    def run(self, chord, active_voices, assignment):

        features = Features(chord, active_voices)

        assignment_generator = assignments.generate(
            chord,
            active_voices,
            assignment,
            self.convergence_limit,
            self.divergence_limit,
        )

        pair_data = []
        for predicted_assignment in assignment_generator:

            pair_data.append(features.pair_data(predicted_assignment))

            data = features.generate(predicted_assignment)
            rank = network.predict(data)

            if rank > max_rank:
                max_rank = rank
                max_assignment = predicted_assignment

        for i, note, voices in enumerate(zip(chord, max_assignment)):
            if assignment[i]:
                continue

            assignment[i] = (note, voices)

        data = []
        for note in chord:
            for voice in active_voices:
                data.append(features.generate(note, chord, voice, active_voices))

            data.append(features.generate(note, chord, None, active_voices))

        self.length += len(data)
        if self.features_dataset.len() <= self.length:
            self.features_dataset.resize((self.length * 2, features.count()))
            self.labels_dataset.resize((self.length * 2,))

        self.features_dataset[self.length - len(data):self.length] = data

        labels_slice = self.labels_dataset[self.length - len(data):self.length]
        for i, note, voices  in enumerate(zip(chord, assignment)):
            for j, voice in enumerate(active_voices):
                labels_slice[i * len(active_voices) + j] = voice in voices.left

            labels_slice[i * len(active_voices) + j + 1] = len(voice.left) == 0
