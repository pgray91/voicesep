import logging

from voicesep.active_voices import ActiveVoices
from voicesep.assignments import Assignments

logger = logging.getLogger(__name__)


def separate(score):

    logger.info("{} | envelope separation".format(score.name))

    pairs = set()
    active_voices = ActiveVoices()

    for chord in score:

        left_voices = [
            voice for voice in active_voices
            if voice.note.offset <= chord.onset and not voice.right
        ]

        right_voices = [Voice(note) for note in chord]

        for left_voice, right_voice in zip(left_voices, right_voices):
            left_voice.link(right_voice)
            pairs.add((left_voice.note, right_voice.note))

        active_voices.insert(right_voices)

    return pairs
