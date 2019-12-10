import h5py
import logging
import numpy as np
import os

import voicesep as vs


logger = logging.getLogger(__name__)


class Dataset:

    class Writer:

        NOTE_LEVEL = "note_level"
        CHORD_LEVEL = "chord_level"

    def __init__(self, name, writer):

        self.fp = h5py.File(f"{name}.hdf5", "a")
        self.writer = writer

        self.groups = list(self.fp.values())

    def __del__(self):

        self.fp.close()

    def sort(self, corpus):

        self.groups.sort(
            key=lambda group: corpus.index(os.path.basename(group.name))
        )

    def write(self, score, beat_horizon, one_to_many):

        group = self.fp.create_group(score.name)

        separators = [
            {"Annotation": {"one_to_many": one_to_many}},
            {f"neural.{self.writer}.Writer": {"group": group}}
        ]
        vs.separate(score, separators, beat_horizon)

        self.groups.append(group)

    def __len__(self):

        return sum(len(next(iter(group.values()))) for group in self.groups)

    def __getitem__(self, index):

        if isinstance(index, slice):
            start = index.start if index.start else 0
            stop = index.stop

        else:
            start = index
            stop = index + 1

        length = len(self)

        stop = min(stop, length) if stop else length

        if start >= stop:
            raise IndexError(f"start={start}, stop={stop}")

        chunk = stop - start

        inputs = {
            name: np.empty((chunk, *input_.shape[1:]), dtype=input_.dtype)
            for name, input_ in next(iter(self.groups)).items()
        }

        get_start = 0
        current_start = 0
        for group in self.groups:
            current_stop = current_start + len(next(iter(group.values())))

            if start < current_stop:
                group_start = max(0, start - current_start)
                group_stop = min(current_stop - current_start, stop - current_start)

                get_stop = get_start + group_stop - group_start

                for name in group:
                    inputs[name][get_start:get_stop] = group[name][group_start:group_stop]

                get_start = get_stop
                if get_start >= chunk:
                    break

            current_start = current_stop

        return tuple(inputs[name] for name in sorted(inputs))
