import logging

logger = logging.getLogger(__name__)

class Voice(Note):

    def __init__(self, note):

        # super

        self.note = note

        self.left = []
        self.right = []

    # Set up get property for note

    def __str__(self):

        return "Voice({})".format(self.note)

def pair(left_voice, right_voice):

    left_voice.right.append(right_voice)
    right_voice.left.append(left_voice)
