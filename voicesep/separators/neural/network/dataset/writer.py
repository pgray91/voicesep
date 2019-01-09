import numpy as np

from voicesep.separators.neural.note_level import features


class Writer(Separator):

    def __init__(self, score, group):

        super(score)

        self.group = group
        self.length = 0

        features_dataset = self.group.create_dataset(
            name="features",
            shape=(0, features.count()),
            maxshape=(None, features.count()),
            dtype=theano.config.floatX
        )

        labels_dataset = group.create_dataset(
            name="labels",
            shape=(0,),
            maxshape=(None,),
            dtype=np.int16
        )

    def __del__(self):
        pass


    def run(self, chord, active_voices, assignment):

        data = []
        for note in chord:
            for voice in active_voices:
                data.append(features.generate(note, chord, voice, active_voices))

            data.append(features.generate(note, chord, None, active_voices))

        length += len(data)
        if features_data.len() <= length:
            features_dataset.resize((length * 2, features.count()))
            labels_dataset.resize((length * 2,))

        features_dataset[length - len(data):length] = data

        labels_slice = labels_dataset[length - len(data):length]
        for i, note, voices  in enumerate(zip(chord, assignment)):
            for j, voice in enumerate(active_voices):
                labels_slice[i * len(active_voices) + j] = voice in voices.left

            labels_slice[i * len(active_voices) + j + 1] = len(voice.left) == 0

            active_voices.insert(assignment)

        self.groups.append(group)
        self.length += length
