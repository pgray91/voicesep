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

        active_voices.insert(assignment)

        assignments.append(assignment)

    return assignments
