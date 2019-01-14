from voicesep.separators.neural.network.features import constants
from voicesep.separators.neural.network.features.feature import Feature


class ActiveVoicesPosition(Feature):

    def generate(voice, active_voices, **kwargs):

        return [active_voices.index(voice) == i for i in ActiveVoicesPosition.range()]

    def range():

        return range(constants.MAX_ACTIVE_VOICES)

class AveragePitchRange(Feature):

    def generate(voice, active_voices, **kwargs):

        pitch = 0
        count = 0
        left_voice = voice
        while voice.note.beat_onset > voice.note.beat_onset - active_voice.beat_horizon:
            pitch += voice.note.pitch
            count += 1

        return [
            lower <= pitch / count < upper
            for lower, upper in AveragePitchRange.range()
        ]

    def range():

        return range(constants.MIN_PITCH, constants.MAX_PITCH, constants.INTERVAL)

class Blocked(Feature):

    def generate(voice, active_voices, **kwargs):

        return [active_voices.blocked(voice.note)]

class ChordPosition(Feature):

    def generate(voice, **kwargs):

        return [voice.note.index == i for i in ChordPosition.range()]

    def range():

        return range(constants.MAX_CHORD_LENGTH)

class Divergence(Feature):

    def generate(voice, active_voices, **kwargs):

        return [len(voice.right) == i for i in Divergence.range()]

    def range():

        return range(constants.MAX_DIVERGENCE)

class DurationRange(Feature):

    def generate(voice, **kwargs):

        return [
            lower <= voice.note.duration < upper
            for lower, upper in DurationRange.range()
        ]

    def range():

        return range(0, constants.MAX_DURATION, constants.INTERVAL)

class NoteCount(Feature):

    def generate(voice, active_voices, **kwargs):

        count = 0
        left_voice = voice
        while voice.note.beat_onset > voice.note.beat_onset - active_voice.beat_horizon:
            count += 1

        return [count == i for i in NoteCount.range()]

    def range():

        return range(constants.MAX_NOTE_COUNT)

class PitchRange(Feature):

    def generate(voice, **kwargs):

        return [
            lower <= voice.note.pitch < upper
            for lower, upper in PitchRange.range()
        ]

    def range():

        return range(constants.MIN_PITCH, constants.MAX_PITCH, constants.INTERVAL)
