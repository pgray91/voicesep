from voicesep.separators.neural.network.features import constants
from voicesep.separators.neural.network.features.feature import Feature


class ActiveVoicesPosition(Feature):

    def generate(voice, active_voices):

        return [active_voices.index(voice) == i for i in ActiveVoicesPosition.range()]

    def range():

        return range(constants.MAX_ACTIVE_VOICES)


class AveragePitchRange(Feature):

    def generate(voice, active_voices):

        pitch = 0
        count = 0
        direction = "left"
        horizon = voice.note.onset - active_voices.beat_horizon
        for left_voice in iterate(voice, direction, horizon):
            pitch += voice.note.pitch
            count += 1

        return [
            lower <= pitch / count < lower + constants.INTERVAL
            for lower in AveragePitchRange.range()
        ]

    def range():

        return range(constants.MIN_PITCH, constants.MAX_PITCH, constants.INTERVAL)


class Blocked(Feature):

    def generate(voice, active_voices):

        return [active_voices.blocked(voice.note)]


class ChordPosition(Feature):

    def generate(voice, active_voices):

        return [voice.note.index == i for i in ChordPosition.range()]

    def range():

        return range(constants.MAX_CHORD_LENGTH)


class Divergence(Feature):

    def generate(voice, active_voices):

        return [len(voice.right) == i for i in Divergence.range()]

    def range():

        return range(constants.MAX_DIVERGENCE)


class DurationRange(Feature):

    def generate(voice, active_voices):

        return [
            lower <= voice.note.duration < lower + constants.INTERVAL
            for lower in DurationRange.range()
        ]

    def range():

        return range(0, constants.MAX_DURATION, constants.INTERVAL)


class NoteCount(Feature):

    def generate(voice, active_voices):

        direction = "left"
        horizon = voice.note.onset - active_voices.beat_horizon
        count = sum(1 for _ in iterate(voice, direction, horizon))

        return [count == i for i in NoteCount.range()]

    def range():

        return range(constants.MAX_NOTE_COUNT)


class PitchRange(Feature):

    def generate(voice, active_voices):

        return [
            lower <= voice.note.pitch < lower + constants.INTERVAL
            for lower in PitchRange.range()
        ]

    def range():

        return range(constants.MIN_PITCH, constants.MAX_PITCH, constants.INTERVAL)


def iterate(voice, direction, horizon):

    stack = [voice]
    while stack:
        voice = stack.pop()
        yield voice

        for next_voice in getattr(voice, direction):
            if (
                direction == "left" and next_voice.note.onset > horizon or
                direction == "right" and next_voice.note.onset < horizon
            ):
                stack.append(next_voice)
