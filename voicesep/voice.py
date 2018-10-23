import logging

logger = logging.getLogger(__name__)

class Voice(Note):

    def __init__(self, note):

        self.note = note

        self.left = set()
        self.right = set()

    def __str__(self):

        return "Voice({})".format(self.note)

    @staticmethod
    def connect(left_voice, right_voice):

        left_voice.right.insert(right_voice)
        right_voice.left.insert(left_voice)

        pair = (left_voice.note, right_voice.note)
        return pair
