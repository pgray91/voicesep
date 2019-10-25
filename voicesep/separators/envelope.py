import logging

from voicesep.separators.separator import Separator
from voicesep.voice import Voice

logger = logging.getLogger(__name__)


class Envelope(Separator):

    def __init__(self, score):

        super().__init__(score)

        logger.debug(f"{__name__} | initialization")

    def run(self, chord, active_voices, assignment):

        logger.info(f"{__name__} separation")

        left_voices = [
            voice for voice in active_voices
            if voice.note.offset <= chord.onset and len(voice.right) == 0
        ]

        right_voices = [Voice(note) for note in chord]

        for left_voice, right_voice in zip(left_voices, right_voices):
            left_voice.link(right_voice)

        for i in range(len(assignment)):
            assignment[i] = right_voices[i]
