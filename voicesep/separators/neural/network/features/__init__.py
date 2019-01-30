from voicesep.separators.neural.network.features.feature import Feature

from voicesep.separators.neural.network.features import constants
from voicesep.separators.neural.network.features import finder

from voicesep.separators.neural.network.features import chord_level
from voicesep.separators.neural.network.features import note_level
from voicesep.separators.neural.network.features import pair_level
from voicesep.separators.neural.network.features import voice_level


class Features:

    def __init__(self, chord, active_voices):

        self.chord = chord
        self.active_voices = active_voices

        self.voices = list(active_voices) + [None]

        self.chord_datum = features.finder.generate(chord_level, chord)

        self.note_data = [
            features.finder.generate(
                note_level,
                note
            )
            for note in chord
        ]

        self.voice_data = [
            features.finder.generate(
                voice_level,
                voice,
                active_voices
            )
            for voice in voices
        ]

        self.pair_data = [
            features.finder.generate(
                pair_level,
                note,
                voice,
                active_voices
            )
        ]

    def pair_level(self, assignment):

        data = []
        for note, voices in assignment:
            for voice in voices:
                data.append(
                    self.chord_datum +
                    self.note_data[i] +
                    self.voice_data[i] +
                    self.pair_data[i]
                )

        return data

    def convergence_level(self, assignment):

        data = []
        for note, voices in assignment:
            convergence_data = features.finder.generate(
                convergence_level,
                note,
                voices,
                active_voices
            )

            data.append(
                self.chord_datum +
                self.note_data[i] +
                convergence_data
            )

        return data

    def divergence_level(self, assignment):

        data = []

    def assignment_level(self, assignment):

        return features.finder.generate(assignment_level, assignment)

    @staticmethod
    def count():

        return sum(features.finder.count(level) for level in levels)

    @staticmethod
    def pad(data, count):

        for _ in range(count):
            data.append(data[-1])


__all__ = [
    "Feature",

    "constants",
    "finder",

    "chord_level",
    "note_level",
    "pair_level",
    "voice_level"
]
