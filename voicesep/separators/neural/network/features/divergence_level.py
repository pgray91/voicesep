from voicesep.separators.neural.network.features import constants
from voicesep.separators.neural.network.features.feature import Feature


class AveragePitchRange(Feature):

    def generate(note, voices, active_voices, **kwargs):

        return [
            lower <= sum(note.pitch - voice.note.pitch for voice in voices) / len(voices) < upper
            for lower, upper in AveragePitchRange.range()
        ]

    def range():

        return range(constants.MIN_PITCH, constants.MAX_PITCH, constants.INTERVAL)
