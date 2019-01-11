import logging

logger = logging.getLogger(__name__)


class Note:

    def __init__(self, name, octave, location, **kwargs):

        self.name = name
        self.octave = octave
        self.location = location

        for key, value in kwargs.items():
            setattr(self, key, value)

        logger.debug("{} | initializing".format(self))

    def __eq__(self, other):

        return (
            isinstance(other, Note) and
            self.name == other.name and
            self.octave == other.octave and
            self.location == other.location
        )

    def __hash__(self):

        return hash((self.name, self.octave, self.location))

    def __str__(self):

        return "Note<M{},C{}>({}{})".format(
            *self.location, self.name, self.octave
        )
