import logging

from voicesep.active_voices import ActiveVoices
from voicesep.assignments import Assignments

logger = logging.getLogger(__name__)


def separate(score):

    logger.info("{} | envelope separation".format(score.name))

    assignments = Assignments()
    active_voices = ActiveVoices()

    for chord in score:

        left_voices = [
            voice for voice in active_voices
            if voice.note.offset <= chord.onset and not voice.right
        ]

        right_voices = [Voice(note) for note in chord]

        for left_voice, right_voice in zip(left_voices, right_voices):
            left_voice.append(right_voice)

        assignments.append(right_voices)

        active_voices.insert(right_voices)

    return assignments
