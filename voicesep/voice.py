import logging

logger = logging.getLogger(__name__)


class Voice:

    def __init__(self, note):

        self.note = note

        self.left = set()
        self.right = set()

        logger.debug("{} | initializing".format(self))

    def link(self, right_voice):

        self.right.add(right_voice)
        right_voice.left.add(self)

    def unlink(self, left_voice):

        self.left.remove(left_voice)
        left_voice.right.remove(self)

    def __eq__(self, other):

        return (
            isinstance(other, Voice) and
            self.note == other.note
        )

    def __hash__(self):

        return hash(self.note)

    def __str__(self):

        return "Voice({})".format(self.note)
