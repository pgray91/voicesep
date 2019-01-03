import h5py
import logging
import numpy as np
import random
import theano
import time

from voicesep.active_voices import ActiveVoices
from voicesep.separators.neural.note_level import features

logger = logging.getLogger(__name__)


class Dataset:

    def __init__(self, path):

        stamp = int(time.time())
        self.fp = h5py.File("{}/{}.{}.hdf5".format(path, "note_level", stamp), "w+")
        self.length = 0

    def __del__(self):

        self.fp.close()

    def shuffle(self):

        random.shuffle(self.groups)

    def write(self, score, assignments, beat_horizon):

        group = self.fp.create_group(score.name)

        features_dataset = group.create_dataset(
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

        active_voices = ActiveVoices()

        length = 0
        for chord, assignment in zip(score, assignments):
            active_voices.filter(beat_horizon)

            data = []
            for note in chord:
                for voice in active_voices:
                    data.append(features.generate(note, chord, voice))

                data.append(features.generate(note, chord, None))

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

    def __getitem__(self, index):

        if isinstance(slice, index):
            start = index.start if index.start else 0
            stop = index.stop if index.stop else self.length

        else:
            start = index
            stop = index + 1

        if start >= stop:
            raise IndexError()

        if start >= self.length:
            raise IndexError()

        length = stop - start

        features = np.empty((length, features.count()), dtype=theano.config.floatX)
        labels = np.empty((length,), dtype=np.int16)

        get_start = 0
        current_start = 0
        for group in self.groups:
            current_stop = current_start + len(group["features"])

            if start >= current_stop:
                current_start = current_stop
                continue

            group_start = max(0, start - current_start)
            group_stop = min(current_stop - current_start, stop - current_start)

            get_stop = get_start + group_stop - group_start

            features[get_start:get_stop] = group["features"][group_start:group_stop]
            labels[get_start:get_stop] = group["labels"][group_start:group_stop]

            get_start = get_stop
            if get_start >= length:
                break

        return features, labels

    def __len__(self):
        
        return self.length
