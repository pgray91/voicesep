import h5py
import logging
import numpy as np
import random
import theano

logger = logging.getLogger(__name__)


class Dataset:

    class Writer:
        
        NOTE_LEVEL = "note_level"
        CHORD_LEVEL = "chord_level"

    def __init__(self, name, writer):

        self.fp = h5py.File("{}.hdf5".format(name), "w")
        self.writer = writer

    def __del__(self):

        self.fp.close()

    def sort(self, corpus):

        self.groups = sorted(
            self.groups,
            key=lambda group: corpus.index(os.path.basename(group.name))
        )

    def write(self, score, beat_horizon, one_to_many):

        group = self.fp.create_group(score.name)

        separators = [
            ("true", one_to_many),
            ("neural.{}.writer".format(self.writer), group)
        ]
        separate(score, separators, beat_horizon)

        self.groups.append(group)

    def __getitem__(self, index):

        if isinstance(slice, index):
            start = index.start if index.start else 0
            stop = index.stop if index.stop else self.length

        else:
            start = index
            stop = index + 1

        if start >= stop:
            raise IndexError("only forward indexing allowed")

        if start >= self.length:
            raise IndexError("start index exceeds length of dataset")

        length = stop - start

        inputs = {
            name: np.empty((length, *input_.shape()[1:]), dtype=input_.dtype)
            for name, input_ in self.groups[0].items()
        }

        get_start = 0
        current_start = 0
        for group in self.groups:
            current_stop = current_start + len(group["input0"])

            if start >= current_stop:
                current_start = current_stop
                continue

            group_start = max(0, start - current_start)
            group_stop = min(current_stop - current_start, stop - current_start)

            get_stop = get_start + group_stop - group_start

            for i in range(len(group)):
                name = "input{}".format(i)
                # flatten to 2d
                inputs[name] = group[name][group_start:group_stop]

            get_start = get_stop
            if get_start >= length:
                break

        return inputs
