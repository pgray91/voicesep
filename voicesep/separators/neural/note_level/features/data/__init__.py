import note_data
import chord_data
import voice_data
import pair_data

def generate(note, chord, voice, interval):
  data = [
      empty_data.generate(voice),
      *note_data.generate(note, interval),
      *chord_data.generate(chord),
      *voice_data.generate(voice),
      *pair_data.generate(note, voice)
  ]

  if data[0]:
    return [1, *([0] * (len(data) - 1))]

note = Note()
chord = Chord()
chord.append(note)
voice = Voice(note, [])

COUNT = len(generate(note, chord, voice))
