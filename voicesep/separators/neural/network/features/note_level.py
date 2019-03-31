import numpy as np

from voicesep.separators.neural.network.features import constants
from voicesep.separators.neural.network.features.feature import Feature


class ChordPosition(Feature):

    def generate(note):

        return [note.index == i for i in ChordPosition.range()]

    def range():

        return list(range(constants.MAX_CHORD_LENGTH))


class DurationRange(Feature):

    def generate(note):

        lowers = DurationRange.range()
        uppers = lowers[1:] + [constants.MAX_DURATION]

        return [
            lower <= note.duration < upper
            for lower, upper in zip(lowers, uppers)
        ]

    def range():

        interval = constants.MAX_DURATION / constants.GRANULARITY

        return list(np.arange(0, constants.MAX_DURATION, interval))


class PitchRange(Feature):

    def generate(note):

        lowers = PitchRange.range()
        uppers = lowers[1:] + [constants.MAX_PITCH]

        return [
            lower <= note.pitch < upper
            for lower, upper in zip(lowers, uppers)
        ]

    def range():

        interval = (constants.MAX_PITCH - constants.MIN_PITCH) / constants.GRANULARITY

        return list(np.arange(constants.MIN_PITCH, constants.MAX_PITCH, interval))
