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

    def __init__(self, chord, active_voices):

        self.chord = chord
        self.voices = list(active_voices) + [None]

        self.chord_datum = finder.generate(chord_level, chord)

        self.note_data = [
            finder.generate(note_level, note)
            for note in chord
        ]

        self.voice_data = [
            finder.generate(voice_level, voice, active_voices)
            for voice in self.voices
        ]

        self.pair_data = []
        for note in chord:
            for voice in self.voices:
                self.pair_data.append(
                    finder.generate(
                        pair_level,
                        note,
                        voice,
                        active_voices
                    )
                )

        logger.debug("initializing")

    def level(self, level):

        if level == pair_level:

            data = []
            for i in range(len(self.chord)):
                for j in range(len(self.voices)):
                    data.append(
                        self.chord_datum +
                        self.note_data[i] +
                        self.voice_data[j] +
                        self.pair_data[i * len(self.chord) + j]
                    )

            return data

        # if level == Features.Level.CONVERGENCE:
        #
        #     data = []
        #     for note, voices in assignment:
        #         convergence_data = finder.generate(
        #             convergence_level,
        #             note,
        #             voices,
        #             active_voices
        #         )
        #
        #         data.append(
        #             self.chord_datum +
        #             self.note_data[i] +
        #             convergence_data
        #         )
        #
        #     return data
        #
        # if level == Features.Level.DIVERGENCE:
        #
        #     data = []
        #     return data
        #
        # if level == Features.Level.ASSIGNMENT:
        #
        #     return finder.generate(assignment_level, assignment)

    @staticmethod
    def count(level):

        if level == pair_level:

            levels = [
                pair_level,
                note_level,
                voice_level,
                chord_level
            ]

        # elif level == convergence_level:
        #
        #     levels = [
        #         Features.Level.CONVERGENCE,
        #         Features.Level.NOTE,
        #         Features.Level.CHORD
        #     ]
        #
        # elif level == divergence_level:
        #
        #     levels = [
        #         Features.Level.DIVERGENCE,
        #         Features.Level.VOICE,
        #         Features.Level.CHORD
        #     ]
        #
        # elif level == Features.Level.ASSIGNMENT:
        #
        #     levels = [Features.Level.ASSIGNMENT]
        #
        else:
            
            levels = [level]

        return sum(finder.count(level) for level in levels)

    @staticmethod
    def pad(data, count):

        for _ in range(max(count - len(data), 0)):
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

    "Feature",
    "Features"
]
