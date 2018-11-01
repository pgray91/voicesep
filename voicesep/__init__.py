import logging

from voicesep.note import Note

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

__all__ = ["Note"]
