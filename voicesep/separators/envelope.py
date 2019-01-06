import logging

from voicesep.separators.separator import Separator

logger = logging.getLogger(__name__)


class Envelope(Separator):

    def __init__(self, score):

        super(score)

    def run(self, chord, active_voices, assignment):

        logger.info("{} separation".format(__name__))

        left_voices = [
            voice for voice in active_voices
            if voice.note.offset <= chord.onset and not voice.right
        ]

        right_voices = [Voice(note) for note in zip(chord, assignment)]

        for left_voice, right_voice in zip(left_voices, right_voices):
            left_voice.link(right_voice)
