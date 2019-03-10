from voicesep.separators.neural.network.features import constants
from voicesep.separators.neural.network.features.feature import Feature


class ChordPosition(Feature):

    def generate(note):

        return [note.index == i for i in ChordPosition.range()]

    def range():

        return range(constants.MAX_CHORD_LENGTH)

class DurationRange(Feature):

    def generate(note):

        return [
            lower <= note.duration < lower + constants.INTERVAL
            for lower in DurationRange.range()
        ]

    def range():

        return range(0, constants.MAX_DURATION, constants.INTERVAL)

class PitchRange(Feature):

    def generate(note):

        return [
            lower <= note.pitch < lower + constants.INTERVAL
            for lower in PitchRange.range()
        ]

    def range():

        return range(constants.MIN_PITCH, constants.MAX_PITCH, constants.INTERVAL)
