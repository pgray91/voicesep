import logging

from voicesep.chord import Chord
from voicesep.note import Note

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

__all__ = ["Chord", "Note"]
