import inspect
import logging
import sys

from voicesep.separators.neural.network.features.feature import Feature

from voicesep.separators.neural.network.features import constants
from voicesep.separators.neural.network.features import finder

from voicesep.separators.neural.network.features import chord_level
from voicesep.separators.neural.network.features import note_level
from voicesep.separators.neural.network.features import pair_level
from voicesep.separators.neural.network.features import voice_level

modules = inspect.getmembers(sys.modules[__name__], predicate=inspect.ismodule)
levels = [module for name, module in modules if name.endswith("level")]

def generate(self, note, chord, voice, active_voices):

    data = []
    for level in levels:
        data.extend(finder.generate(level, note, chord, voice, active_voices))

    return data

def count():

    return sum(finder.count(level) for level in levels)

__all__ = [
    "Feature",

    "constants",
    "finder",

    "chord_level",
    "note_level",
    "pair_level",
    "voice_level"
]
