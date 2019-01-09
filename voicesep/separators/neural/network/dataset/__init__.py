import h5py
import logging
import numpy as np
import random
import theano

from voicesep.active_voices import ActiveVoices
from voicesep.separators.neural.features import Features

logger = logging.getLogger(__name__)


class Dataset:

    def __init__(self, name):

        self.fp = h5py.File("{}.hdf5".format(path), "w+")
        self.length = 0

    def __del__(self):

        self.fp.close()

    def sort(self, corpus):

        random.shuffle(self.groups)

    def write(self, score, beat_horizon):

        group = self.fp.create_group(score.name)

        separators = [
            ("true", one_to_many)
            ("neural.dataset.writer", x)
        ]
        separate(score, separators, beat_horizon)


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
