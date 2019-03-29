import functools
import importlib
import logging

from voicesep.active_voices import ActiveVoices
from voicesep.separators import *
from voicesep.voice import Voice

logger = logging.getLogger(__name__)


def separate(score, waterfall, beat_horizon):

    logger.debug("{} | separation".format(score.name))

    separators = []
    for request in waterfall:
        name, kwargs = next(iter(request.items()))

        path = name.split(".")
        Separator = functools.reduce(
            lambda a, b: getattr(a, b),
            [globals()[path[0]], *path[1:]]
        )

        separators.append(Separator(score, **kwargs))

    assignments = []
    active_voices = ActiveVoices(beat_horizon)

    for chord in score:
        active_voices.filter(chord.onset)

        logger.debug("{} | {} active voices".format(chord, len(active_voices)))

        assignment = [None] * len(chord)
        for separator in separators:
            separator.run(chord, active_voices, assignment)

        for i in range(len(assignment)):
            if assignment[i] is None:
                assignment[i] = Voice(chord[i])

        # right_voices = []
        # for note, left_voices in assignment:
        #     right_voices.append(Voice(note))
        #     for left_voice in left_voices:
        #         left_voice.link(right_voices[-1])

        # active_voices.insert(right_voices)

        active_voices.insert(assignment)

        assignments.append(assignment)

    return assignments
