import logging

logger = logging.getLogger(__name__)


class Chord:

    def __init__(self, notes, **kwargs):

        self.notes = notes

        for key, value in kwargs.items():
            setattr(self, key, value)

        logger.debug("{} | initializing".format(self))

    def __len__(self):

        return len(self.notes)

    def __getitem__(self, index):

        return self.notes[index]

    def __iter__(self):

        return iter(self.notes)

    def __str__(self):

        return "Chord({})".format(", ".join(map(str, self.notes)))
