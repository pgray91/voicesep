import logging

logger = logging.getLogger(__name__)

class Note:

    def __init__(self, name, octave, location, **kwargs):

        self.name = name
        self.octave = octave
        self.location = location

        for key, value in kwargs.items():
            setattr(self, key, value)

        logger.debug("{} | initializing note".format(self))

    def __str__(self):

        return "Note<M{},C{}>({}{})".format(
            *self.location, self.name, self.octave
        )
