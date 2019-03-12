from voicesep.separators.neural.network.features import constants
from voicesep.separators.neural.network.features.feature import Feature


class ActiveVoicesPosition(Feature):

    def generate(voice, active_voices):

        if not voice:
            return [0] * len(list(ActiveVoicesPosition.range()))

        return [active_voices.index(voice) == i for i in ActiveVoicesPosition.range()]

    def range():

        return range(constants.MAX_ACTIVE_VOICES)


class AveragePitchRange(Feature):

    def generate(voice, active_voices):

        if not voice:
            return [0] * len(list(ActivePitchRange.range()))

        beat_horizon = active_voices.beat_horizon or constants.BEAT_HORIZON
        pitch = 0
        count = 0
        direction = "left"
        distance = voice.note.onset - beat_horizon
        for left_voice in iterate(voice, direction, distance):
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

        if not voice:
            return [0]

        return [active_voices.blocked(voice.note)]


class ChordPosition(Feature):

    def generate(voice, active_voices):

        if not voice:
            return [0] * len(list(ChordPosition.range()))

        return [voice.note.index == i for i in ChordPosition.range()]

    def range():

        return range(constants.MAX_CHORD_LENGTH)


class Divergence(Feature):

    def generate(voice, active_voices):

        if not voice:
            return [0] * len(list(Divergence.range()))

        return [len(voice.right) == i for i in Divergence.range()]

    def range():

        return range(constants.MAX_DIVERGENCE)


class DurationRange(Feature):

    def generate(voice, active_voices):

        if not voice:
            return [0] * len(list(DurationRange.range()))

        return [
            lower <= voice.note.duration < lower + constants.INTERVAL
            for lower in DurationRange.range()
        ]

    def range():

        return range(0, constants.MAX_DURATION, constants.INTERVAL)


class NoteCount(Feature):

    def generate(voice, active_voices):

        if not voice:
            return [0] * len(list(NoteCount.range()))

        beat_horizon = active_voices.beat_horizon or constants.BEAT_HORIZON
        direction = "left"
        distance = voice.note.onset - beat_horizon
        count = sum(1 for _ in iterate(voice, direction, distance))

        return [count == i for i in NoteCount.range()]

    def range():

        return range(constants.MAX_NOTE_COUNT)


class PitchRange(Feature):

    def generate(voice, active_voices):

        if not voice:
            return [0] * len(list(PitchRange.range()))

        return [
            lower <= voice.note.pitch < lower + constants.INTERVAL
            for lower in PitchRange.range()
        ]

    def range():

        return range(constants.MIN_PITCH, constants.MAX_PITCH, constants.INTERVAL)


class Empty(Feature):

    def generate(voice, active_voices):

        if not voice:
            return [1]

        return [0]


def iterate(voice, direction, distance):

    stack = [voice]
    while stack:
        voice = stack.pop()
        yield voice

        for next_voice in getattr(voice, direction):
            if (
                direction == "left" and next_voice.note.onset > distance or
                direction == "right" and next_voice.note.onset < distance
            ):
                stack.append(next_voice)
