import logging
import music21 as m21

logger = logging.getLogger(__name__)


class Note:

    def __init__(self, name, octave, location, **kwargs):

        self.name = name
        self.octave = octave
        self.location = location

        self.pitch = int(m21.pitch.Pitch(f"{name}{octave}").ps)

        for key, value in kwargs.items():
            setattr(self, key, value)

        logger.debug(f"{self} | initializing")

    def __eq__(self, note):

        return (
            isinstance(note, Note) and
            self.name == note.name and
            self.octave == note.octave and
            self.location == note.location
        )

    def __hash__(self):

        return hash((self.name, self.octave, self.location))

    def __lt__(self, note):

        return self.pitch < note.pitch

    def __str__(self):

        measure, chord = self.location
        return f"Note<M{measure},C{chord}>({self.name}{self.octave})"
