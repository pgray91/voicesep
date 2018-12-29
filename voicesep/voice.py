import logging

logger = logging.getLogger(__name__)


class Voice:

    def __init__(self, note):

        self.note = note

        self.left = set()
        self.right = set()

        logger.debug("{} | initializing voice".format(self))

    def link(self, right_voice):

        self.right.add(right_voice)
        right_voice.left.add(self)

    def __str__(self):

        return "Voice({})".format(self.note)
