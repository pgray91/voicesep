import functools
import logging

from voicesep.separators import neural

from voicesep.separators.annotation import Annotation
from voicesep.separators.envelope import Envelope
from voicesep.separators.pseudo_polyphony import PseudoPolyphony
from voicesep.separators.separator import Separator

from voicesep.active_voices import ActiveVoices
from voicesep.voice import Voice

logger = logging.getLogger(__name__)


def separate(score, waterfall, beat_horizon):

    logger.debug(f"{score.name} | separation")

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

        logger.debug(f"{chord} | {len(active_voices)} active voices")

        assignment = [None] * len(chord)
        for separator in separators:
            separator.run(chord, active_voices, assignment)

        for i in range(len(assignment)):
            if assignment[i] is None:
                assignment[i] = Voice(chord[i])

        active_voices.insert(assignment)

        assignments.append(assignment)

    return assignments


__all__ = [
    "neural",

    "Annotation",
    "Envelope",
    "PseudoPolyphony",
    "Separator"
]
