import numpy as np

from voicesep.separators.neural.network.features import constants
from voicesep.separators.neural.network.features.feature import Feature


class AveragePitchRange(Feature):

    def generate(note, voices, active_voices, **kwargs):

        lowers = AveragePitchRange.range()
        uppers = lowers[1:] + [constants.MAX_PITCH]

        average = sum(note.pitch - voice.note.pitch for voice in voices) / len(voices)

        return [
            lower <= average < upper
            for lower, upper in zip(lowers, uppers)
        ]

    def range():

        interval = (constants.MAX_PITCH - constants.MIN_PITCH) / constants.GRANULARITY

        return list(np.arange(constants.MIN_PITCH, constants.MAX_PITCH, interval))
