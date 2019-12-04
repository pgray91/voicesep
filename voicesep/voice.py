import logging

logger = logging.getLogger(__name__)


class Voice:

    def __init__(self, note):

        self.note = note

        self.left = set()
        self.right = set()

        logger.debug(f"{self} | initializing")

    def link(self, right_voice):

        self.right.add(right_voice)
        right_voice.left.add(self)

    def __eq__(self, voice):

        return (
            isinstance(voice, Voice) and
            self.note == voice.note
        )

    def __hash__(self):

        return hash(self.note)

    def __lt__(self, voice):

        return self.note < voice.note

    def __str__(self):

        return f"Voice({self.note})"
