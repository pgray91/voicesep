import logging

from voicesep.separators.neural.features import finder

from voicesep.separators.neural.features import chord_level
from voicesep.separators.neural.features import note_level
from voicesep.separators.neural.features import pair_level
from voicesep.separators.neural.features import voice_level

levels = [
    module for name, module in inspect.getmembers(__name__, predicate=inspect.ismodule)
    if name.endswith(level)
]

def generate(self, note, chord, voice):

    data = []
    for level in levels:
        data.extend(finder.generate(level, note, chord, voice))

    return data

def count():

    return sum(finder.count(level) for level in levels)

__all__ = [
    "finder",

    "chord_level",
    "note_level",
    "pair_level",
    "voice_level",
]
