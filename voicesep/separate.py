import importlib
import logging

from voicesep.active_voices import ActiveVoices
from voicesep.separators import *

logger = logging.getLogger(__name__)


def separate(score, waterfall, beat_horizon):

    logger.debug("{} | separation".format(score.name))

    separators = []
    for request in waterfall:
        name = next(iter(request))
        kwargs = request[name]

        Separator = globals()[name]
        separators.append(Separator(score, **kwargs))

    assignments = []
    active_voices = ActiveVoices(beat_horizon)

    for chord in score:
        active_voices.filter(chord.onset)

        logger.debug("{} | {} active voices".format(chord, len(active_voices)))

        assignment = [None] * len(chord)
        for separator in separators:
            separator.run(chord, active_voices, assignment)

        right_voices = []
        for note, left_voices in assignment:
            right_voices.append(Voice(note))
            for left_voice in voices:
                left_voice.link(right_voices[-1])

        active_voices.insert(right_voices)

        assignments.append(assignment)

    return assignments
