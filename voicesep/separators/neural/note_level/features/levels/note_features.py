import voicesep.utils.constants as const
COUNT = 76

def create(note):
  data = [
    # Pitch
    note.pitch_space >= 80,
    note.pitch_space >= 75 and note.pitch_space < 80,
    note.pitch_space >= 70 and note.pitch_space < 75,
    note.pitch_space >= 65 and note.pitch_space < 70,
    note.pitch_space >= 60 and note.pitch_space < 65,
    note.pitch_space >= 55 and note.pitch_space < 60,
    note.pitch_space >= 50 and note.pitch_space < 55,
    note.pitch_space >= 45 and note.pitch_space < 50,
    note.pitch_space >= 40 and note.pitch_space < 45,
    note.pitch_space < 40,

    abs(note.pitch_space - note.note_above.pitch_space) / const.MAX_PITCH_DISTANCE if note.note_above else 1,
    abs(note.pitch_space - note.note_below.pitch_space) / const.MAX_PITCH_DISTANCE if note.note_below else 1,

    # Temporal
    note.beat_duration >= 4,
    note.beat_duration >= 3 and note.beat_duration < 4,
    note.beat_duration >= 2 and note.beat_duration < 3,
    note.beat_duration >= 1.75 and note.beat_duration < 2,
    note.beat_duration >= 1.5 and note.beat_duration < 1.75,
    note.beat_duration >= 1.25 and note.beat_duration < 1.5,
    note.beat_duration >= 1 and note.beat_duration < 1.25,
    note.beat_duration >= 0.875 and note.beat_duration < 1,
    note.beat_duration >= 0.75 and note.beat_duration < 0.875,
    note.beat_duration >= 0.625 and note.beat_duration < 0.75,
    note.beat_duration >= 0.5 and note.beat_duration < 0.625,
    note.beat_duration >= 0.375 and note.beat_duration < 0.5,
    note.beat_duration >= 0.25 and note.beat_duration < 0.375,
    note.beat_duration >= 0.125 and note.beat_duration < 0.25,
    note.beat_duration < 0.125,

    abs(float(note.beat_duration - note.note_above.beat_duration)) / const.MAX_BEAT_DUR_DISTANCE if note.note_above else 1,
    note.beat_duration > note.note_above.beat_duration if note.note_above else 0,
    note.beat_duration < note.note_above.beat_duration if note.note_above else 0,
    note.beat_duration == note.note_above.beat_duration if note.note_above else 0,

    abs(float(note.beat_duration - note.note_below.beat_duration)) / const.MAX_BEAT_DUR_DISTANCE if note.note_below else 1,
    note.beat_duration > note.note_below.beat_duration if note.note_below else 0,
    note.beat_duration < note.note_below.beat_duration if note.note_below else 0,
    note.beat_duration == note.note_below.beat_duration if note.note_below else 0,

    # Positional
    note.index == 0,
    note.index == 1,
    note.index == 2,
    note.index == 3,
    note.index == 4,
    note.index == 5,
    note.index == 6,
    note.index == 7,

    note.chord_length == 1,
    note.chord_length == 2,
    note.chord_length == 3,
    note.chord_length == 4,
    note.chord_length == 5,
    note.chord_length == 6,
    note.chord_length == 7,
    note.chord_length == 8,

    # Tonal
    note.degree == 1,
    note.degree == 2,
    note.degree == 3,
    note.degree == 4,
    note.degree == 5,
    note.degree == 6,
    note.degree == 7,

    note.chord_step == 1,
    note.chord_step == 2,
    note.chord_step == 3,
    note.chord_step == 4,
    note.chord_step == 5,
    note.chord_step == 6,
    note.chord_step == 7,

    # Metrical
    note.beat_strength == 1,
    note.beat_strength >= 0.9 and note.beat_strength < 1,
    note.beat_strength >= 0.8 and note.beat_strength < 0.9,
    note.beat_strength >= 0.7 and note.beat_strength < 0.8,
    note.beat_strength >= 0.6 and note.beat_strength < 0.7,
    note.beat_strength >= 0.5 and note.beat_strength < 0.6,
    note.beat_strength >= 0.4 and note.beat_strength < 0.5,
    note.beat_strength >= 0.3 and note.beat_strength < 0.4,
    note.beat_strength >= 0.2 and note.beat_strength < 0.3,
    note.beat_strength >= 0.1 and note.beat_strength < 0.2,
    note.beat_strength < 0.1,
  ]

  assert len(data) == COUNT, len(data)
  return data
