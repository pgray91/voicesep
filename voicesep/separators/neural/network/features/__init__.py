import logging

from voicesep.separators.neural.network.features import constants
from voicesep.separators.neural.network.features import finder

from voicesep.separators.neural.network.features import chord_level
from voicesep.separators.neural.network.features import convergence_level
from voicesep.separators.neural.network.features import divergence_level
from voicesep.separators.neural.network.features import note_level
from voicesep.separators.neural.network.features import pair_level
from voicesep.separators.neural.network.features import voice_level

from voicesep.separators.neural.network.features.feature import Feature

logger = logging.getLogger(__name__)


class Features:

    class Level:

        ASSIGNMENT = "assignment_level",
        CHORD = "chord_level",
        CONVERGENCE = "convergence_level",
        DIVERGENCE = "divergence_level",
        NOTE = "note_level",
        PAIR = "pair_level",
        VOICE = "voice_level"

    def __init__(self, chord, active_voices):

        self.chord = chord
        self.active_voices = active_voices

        self.voices = list(active_voices) + [None]

        self.chord_datum = finder.generate(chord_level, chord)

        self.note_data = [
            finder.generate(
                note_level,
                note
            )
            for note in chord
        ]

        self.voice_data = [
            finder.generate(
                voice_level,
                voice,
                active_voices
            )
            for voice in voices
        ]

        self.pair_data = [
            finder.generate(
                pair_level,
                note,
                voice,
                active_voices
            )
        ]

        logger.debug("initializing")

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
            convergence_data = finder.generate(
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

        return finder.generate(assignment_level, assignment)

    @staticmethod
    def count(levels=None):

        levels = levels or Features.LEVELS

        return sum(finder.count(level) for level in levels)

    @staticmethod
    def pad(data, count):

        for _ in range(count):
            data.append(data[-1])


__all__ = [
    "constants",
    "finder",

    "chord_level",
    "convergence_level",
    "divergence_level",
    "note_level",
    "pair_level",
    "voice_level",

    "Feature"
]
