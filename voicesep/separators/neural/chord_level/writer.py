import numpy as np

from voicesep.separators.neural.network import features
from voicesep.separators.neural.chord_level import assignments


class Writer(Separator):

    def __init__(
        self,
        score,
        group,
        convergence_limit,
        divergence_limit,
        assignment_limit,
        pair_depth,
        convergence_depth,
        divergence_depth
    ):

        super().__init__(score)

        self.group = group

        self.convergence_limit = convergence_limit
        self.divergence_limit = divergence_limit
        self.assignment_limit = assignment_limit
        self.pair_depth = pair_depth
        self.convergence_depth = convergence_depth
        self.divergence_depth = divergence_depth

        pair_count = features.count([features.Levels.CHORD, features.Levels.PAIR])
        convergence_count = features.count([features.Levels.CONVERGENCE])
        divergence_count = features.count([features.Levels.DIVERGENCE])
        assignment_count = features.count([features.Levels.ASSIGNMENT])

        self.pair_dataset = self.group.create_dataset(
            name="input0",
            shape=(0, pair_count),
            maxshape=(None, pair_count),
            dtype=theano.config.floatX
        )
        self.pair_length = 0

        self.convergence_dataset = self.group.create_dataset(
            name="input1",
            shape=(0, convergence_count),
            maxshape=(None, convergence_count),
            dtype=theano.config.floatX
        )
        self.convergence_length = 0

        self.divergence_dataset = self.group.create_dataset(
            name="input2",
            shape=(0, divergence_count),
            maxshape=(None, divergence_count),
            dtype=theano.config.floatX
        )
        self.divergence_length = 0

        self.assignment_dataset = self.group.create_dataset(
            name="input3",
            shape=(0, assignment_count),
            maxshape=(None, assignment_count),
            dtype=theano.config.floatX
        )
        self.assignment_length = 0

    def __del__(self):

        self.features_dataset.resize((self.length, features.count()))
        self.labels_dataset.resize((self.length,))

    def run(self, chord, active_voices, assignment):

        features = Features(chord, active_voices)

        assignment_generator = assignments.generate(
            chord,
            active_voices,
            None, # empty assignment
            self.convergence_limit,
            self.divergence_limit,
            self.assignment_limit
        )

        pair_data = []
        convergence_data = []
        divergence_data = []
        assignment_data = []
        for predicted_assignment in assignment_generator:

            pair_data.append(features.pair_data(predicted_assignment))
            Features.pad(pair_data[-1], self.pair_depth)

            convergence_data.append(features.convergence_data(predicted_assignment))
            Features.pad(convergence_data[-1], self.convergence_depth)

            divergence_data.extend(features.divergence_data(predicted_assignment))
            Features.pad(divergence_data[-1], self.divergence_depth)

            assignment_data.append(features.assignment_data(predicted_assignment))

        self.pair_length += len(pair_data)
        self.convergence_length += len(convergence_data)
        self.divergence_length += len(divergence_data)
        self.assignment_length += len(assignment_data)

        if self.features_dataset.len() <= self.length:
            self.features_dataset.resize((self.length * 2, features.count()))
            self.labels_dataset.resize((self.length * 2,))

        self.features_dataset[self.length - len(data):self.length] = data
