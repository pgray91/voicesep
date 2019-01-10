import importlib
import logging

from voicesep.active_voices import ActiveVoices

logger = logging.getLogger(__name__)


def separate(score, separator_configs, beat_horizon):

    logger.debug("{} | separation".format(score.name))

    for name, args in separator_configs:
        Separator = importlib.import_module("voicesep.separators.{}".format(name))
        separators.append(Separator(score, *args))

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
