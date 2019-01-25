from voicesep.separators.neural.network.features import constants
from voicesep.separators.neural.network.features.feature import Feature


class ChordLength(Feature):

    def generate(chord, **kwargs):

        return [len(chord) == i for i in ChordLength.range()]

    def range():

        return range(constants.MAX_CHORD_LENGTH)
