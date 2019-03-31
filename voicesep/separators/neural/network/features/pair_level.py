from voicesep.separators.neural.network.features import constants
from voicesep.separators.neural.network.features.feature import Feature


class PitchDistance(Feature):

    def generate(note, voice, active_voices):

        if not voice:
            return [constants.MAX_PITCH]

        return [abs(note.pitch - voice.note.pitch)]


class PitchDirection(Feature):

    
    def generate(note, voice, active_voices):

        if not voice:
            return [0] * len(list(PitchDirection.range()))

        return [
            note.pitch < voice.note.pitch,
            note.pitch == voice.note.pitch,
            note.pitch > voice.note.pitch
        ]

    def range():

        return [0, 1, 2]


class InterOnset(Feature):

    def generate(note, voice, active_voices):

        if not voice:
            return [constants.MAX_DURATION]

        return [abs(note.onset - voice.note.onset)]


class OnsetOffset(Feature):

    def generate(note, voice, active_voices):

        if not voice:
            return [constants.MAX_DURATION]

        return [max(note.onset - voice.note.offset, 0)]


class Overlap(Feature):

    def generate(note, voice, active_voices):

        if not voice:
            return [0] * len(list(Overlap.range()))

        return [
            note.onset > voice.note.offset,
            note.onset == voice.note.offset,
            note.onset < voice.note.offset
        ]

    def range():

        return [0, 1, 2]


class DurationDifference(Feature):

    def generate(note, voice, active_voices):

        if not voice:
            return [constants.MAX_DURATION]

        return [abs(note.duration - voice.note.duration)]
    

class PositionDifference(Feature):

    def generate(note, voice, active_voices):

        if not voice:
            return [constants.MAX_ACTIVE_VOICES]

        return [abs(note.index - active_voices.index(voice))]


class ChordPositionDifference(Feature):

    def generate(note, voice, active_voices):

        if not voice:
            return [constants.MAX_CHORD_LENGTH]

        return [abs(note.index - voice.note.index)]


class Cross(Feature):

    def generate(note, voice, active_voices):

        if not voice:
            return [False]

        return [active_voices.crossing(voice.note, note)]
