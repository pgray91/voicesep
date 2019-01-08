from voicesep.score import Score
from voicesep.separators.neural.features.feature import Feature


class ChordPosition(Feature):

    def generate(note, **kwargs):

        return [note.index == i for i in ChordPosition.range()]

    def range():

        return range(Score.MAX_CHORD_LENGTH)

class DurationRange(Feature):

    def generate(note, **kwargs):

        return [
            lower <= note.duration < upper
            for lower, upper in DurationRange.range()
        ]

    def range():

        return range(0, Score.MAX_DURATION, Feature.INTERVAL)

class PitchRange(Feature):

    def generate(note, **kwargs):

        return [
            lower <= note.pitch < upper
            for lower, upper in PitchRange.range()
        ]

    def range():

        return range(Score.MIN_PITCH, Score.MAX_PITCH, Feature.INTERVAL)
