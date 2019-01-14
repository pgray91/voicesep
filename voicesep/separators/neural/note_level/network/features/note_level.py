from voicesep.separators.neural.network.features import constants
from voicesep.separators.neural.network.features.feature import Feature


class ChordPosition(Feature):

    def generate(note, **kwargs):

        return [note.index == i for i in ChordPosition.range()]

    def range():

        return range(constants.MAX_CHORD_LENGTH)

class DurationRange(Feature):

    def generate(note, **kwargs):

        return [
            lower <= note.duration < upper
            for lower, upper in DurationRange.range()
        ]

    def range():

        return range(0, constants.MAX_DURATION, constants.INTERVAL)

class PitchRange(Feature):

    def generate(note, **kwargs):

        return [
            lower <= note.pitch < upper
            for lower, upper in PitchRange.range()
        ]

    def range():

        return range(constants.MIN_PITCH, constants.MAX_PITCH, constants.INTERVAL)
