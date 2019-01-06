import logging

from voicesep.active_voices import ActiveVoices

logger = logging.getLogger(__name__)


def separate(score, separators, beat_horizon):

    logger.info("{} | separation".format(score.name))

    for separator, args in separators:
        separator = locals("voicesep.separators.{}".format(
            "".join(name.title() for name in separator.split("_"))
        )
        )(*args)

    assignments = []
    active_voices = ActiveVoices()

    for chord in score:
        active_voices.filter(chord.onset, beat_horizon)

        logger.info("{} | {} active voices".format(chord, len(active_voices)))

        assignment = [None] * len(chord)
        for separator in separators:
            separator.run(chord, active_voices, assignment)

        active_voices.insert(assignment)

        assignments.append(assignment)

    return assignments
