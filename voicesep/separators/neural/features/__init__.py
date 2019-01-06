import logging

from voicesep.chord import Chord
from voicesep.note import Note
from voicesep.voice import Voice
from voicesep.separators.neural.note_level.features import chord_data
from voicesep.separators.neural.note_level.features import note_data
from voicesep.separators.neural.note_level.features import pair_data
from voicesep.separators.neural.note_level.features import voice_data


def generate(self, note, chord, voice):

    return [
        *note_data.generate(note),
        *chord_data.generate(note),
        *voice_data.generate(note),
        *pair_data.generate(note),
    ]

def count():

    note = Note() 
    chord = Chord()
    voice = Voice()

    return len(generate(note, chord, voice))
