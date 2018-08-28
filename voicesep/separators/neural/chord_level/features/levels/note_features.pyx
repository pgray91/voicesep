#cython: language_level=3
import cython
import voicesep.utils.constants as const

cdef int COUNT = 76

@cython.boundscheck(False)
@cython.wraparound(False)
cdef create(float[:,::1] all_note_data, chord, float beat_horizon):
  cdef int chord_len = len(chord)
  cdef int all_note_data_len = len(all_note_data)
  assert all_note_data_len == chord_len

  cdef int all_note_len = len(all_note_data[0, :])
  assert all_note_len == COUNT

  cdef int i, j

  for i, note in enumerate(chord):
    # assert note.chord_length < 8, note.chord_length
    # assert note.beat <= 5, note.beat
    # assert note.all_index[chord.index] < 9, note.all_index[chord.index]

    j = 0

    # Pitch
    all_note_data[i, j] = note.pitch_space >= 80; j += 1
    all_note_data[i, j] = note.pitch_space >= 75 and note.pitch_space < 80; j += 1
    all_note_data[i, j] = note.pitch_space >= 70 and note.pitch_space < 75; j += 1
    all_note_data[i, j] = note.pitch_space >= 65 and note.pitch_space < 70; j += 1
    all_note_data[i, j] = note.pitch_space >= 60 and note.pitch_space < 65; j += 1
    all_note_data[i, j] = note.pitch_space >= 55 and note.pitch_space < 60; j += 1
    all_note_data[i, j] = note.pitch_space >= 50 and note.pitch_space < 55; j += 1
    all_note_data[i, j] = note.pitch_space >= 45 and note.pitch_space < 50; j += 1
    all_note_data[i, j] = note.pitch_space >= 40 and note.pitch_space < 45; j += 1
    all_note_data[i, j] = note.pitch_space < 40; j += 1

    all_note_data[i, j] = abs(note.pitch_space - note.note_above.pitch_space) / const.MAX_PITCH_DISTANCE if note.note_above else 1; j += 1
    all_note_data[i, j] = abs(note.pitch_space - note.note_below.pitch_space) / const.MAX_PITCH_DISTANCE if note.note_below else 1; j += 1

    # Temporal
    all_note_data[i, j] = note.beat_duration >= 4; j += 1
    all_note_data[i, j] = note.beat_duration >= 3 and note.beat_duration < 4; j += 1
    all_note_data[i, j] = note.beat_duration >= 2 and note.beat_duration < 3; j += 1
    all_note_data[i, j] = note.beat_duration >= 1.75 and note.beat_duration < 2; j += 1
    all_note_data[i, j] = note.beat_duration >= 1.5 and note.beat_duration < 1.75; j += 1
    all_note_data[i, j] = note.beat_duration >= 1.25 and note.beat_duration < 1.5; j += 1
    all_note_data[i, j] = note.beat_duration >= 1 and note.beat_duration < 1.25; j += 1
    all_note_data[i, j] = note.beat_duration >= 0.875 and note.beat_duration < 1; j += 1
    all_note_data[i, j] = note.beat_duration >= 0.75 and note.beat_duration < 0.875; j += 1
    all_note_data[i, j] = note.beat_duration >= 0.625 and note.beat_duration < 0.75; j += 1
    all_note_data[i, j] = note.beat_duration >= 0.5 and note.beat_duration < 0.625; j += 1
    all_note_data[i, j] = note.beat_duration >= 0.375 and note.beat_duration < 0.5; j += 1
    all_note_data[i, j] = note.beat_duration >= 0.25 and note.beat_duration < 0.375; j += 1
    all_note_data[i, j] = note.beat_duration >= 0.125 and note.beat_duration < 0.25; j += 1
    all_note_data[i, j] = note.beat_duration < 0.125; j += 1

    all_note_data[i, j] = abs(float(note.beat_duration - note.note_above.beat_duration)) / const.MAX_BEAT_DUR_DISTANCE if note.note_above else 1; j += 1
    all_note_data[i, j] = note.beat_duration > note.note_above.beat_duration if note.note_above else 0; j += 1
    all_note_data[i, j] = note.beat_duration < note.note_above.beat_duration if note.note_above else 0; j += 1
    all_note_data[i, j] = note.beat_duration == note.note_above.beat_duration if note.note_above else 0; j += 1

    all_note_data[i, j] = abs(float(note.beat_duration - note.note_below.beat_duration)) / const.MAX_BEAT_DUR_DISTANCE if note.note_below else 1; j += 1
    all_note_data[i, j] = note.beat_duration > note.note_below.beat_duration if note.note_below else 0; j += 1
    all_note_data[i, j] = note.beat_duration < note.note_below.beat_duration if note.note_below else 0; j += 1
    all_note_data[i, j] = note.beat_duration == note.note_below.beat_duration if note.note_below else 0; j += 1

    # Positional
    all_note_data[i, j] = note.index == 0; j += 1
    all_note_data[i, j] = note.index == 1; j += 1
    all_note_data[i, j] = note.index == 2; j += 1
    all_note_data[i, j] = note.index == 3; j += 1
    all_note_data[i, j] = note.index == 4; j += 1
    all_note_data[i, j] = note.index == 5; j += 1
    all_note_data[i, j] = note.index == 6; j += 1
    all_note_data[i, j] = note.index == 7; j += 1

    all_note_data[i, j] = note.chord_length == 1; j += 1
    all_note_data[i, j] = note.chord_length == 2; j += 1
    all_note_data[i, j] = note.chord_length == 3; j += 1
    all_note_data[i, j] = note.chord_length == 4; j += 1
    all_note_data[i, j] = note.chord_length == 5; j += 1
    all_note_data[i, j] = note.chord_length == 6; j += 1
    all_note_data[i, j] = note.chord_length == 7; j += 1
    all_note_data[i, j] = note.chord_length == 8; j += 1

    # Tonal
    all_note_data[i, j] = note.degree == 1; j += 1
    all_note_data[i, j] = note.degree == 2; j += 1
    all_note_data[i, j] = note.degree == 3; j += 1
    all_note_data[i, j] = note.degree == 4; j += 1
    all_note_data[i, j] = note.degree == 5; j += 1
    all_note_data[i, j] = note.degree == 6; j += 1
    all_note_data[i, j] = note.degree == 7; j += 1

    all_note_data[i, j] = note.chord_step == 1; j += 1
    all_note_data[i, j] = note.chord_step == 2; j += 1
    all_note_data[i, j] = note.chord_step == 3; j += 1
    all_note_data[i, j] = note.chord_step == 4; j += 1
    all_note_data[i, j] = note.chord_step == 5; j += 1
    all_note_data[i, j] = note.chord_step == 6; j += 1
    all_note_data[i, j] = note.chord_step == 7; j += 1

    # Metrical
    all_note_data[i, j] = note.beat_strength == 1; j += 1
    all_note_data[i, j] = note.beat_strength >= 0.9 and note.beat_strength < 1; j += 1
    all_note_data[i, j] = note.beat_strength >= 0.8 and note.beat_strength < 0.9; j += 1
    all_note_data[i, j] = note.beat_strength >= 0.7 and note.beat_strength < 0.8; j += 1
    all_note_data[i, j] = note.beat_strength >= 0.6 and note.beat_strength < 0.7; j += 1
    all_note_data[i, j] = note.beat_strength >= 0.5 and note.beat_strength < 0.6; j += 1
    all_note_data[i, j] = note.beat_strength >= 0.4 and note.beat_strength < 0.5; j += 1
    all_note_data[i, j] = note.beat_strength >= 0.3 and note.beat_strength < 0.4; j += 1
    all_note_data[i, j] = note.beat_strength >= 0.2 and note.beat_strength < 0.3; j += 1
    all_note_data[i, j] = note.beat_strength >= 0.1 and note.beat_strength < 0.2; j += 1
    all_note_data[i, j] = note.beat_strength < 0.1; j += 1

    # Pseudo Polyphony
    # repeat_count = 0
    # repeat_right = note.repeat_right
    # while repeat_right is not None:
    #   if repeat_right.beat_onset - repeat_right.repeat_left.beat_offset > 0:
    #     break
    #
    #   if repeat_right.beat_onset - repeat_right.repeat_left.beat_offset > beat_horizon:
    #     break
    #
    #   repeat_count += 1
    #   repeat_right = repeat_right.repeat_right
    #
    # repeat_left = note.repeat_left
    # while repeat_left is not None:
    #   if repeat_left.repeat_right.beat_onset - repeat_left.beat_offset > 0:
    #     break
    #
    #   if repeat_left.repeat_right.beat_onset - repeat_left.beat_offset > beat_horizon:
    #     break
    #
    #   repeat_count += 1
    #   repeat_left = repeat_left.repeat_left
    #
    # all_note_data[i, j] = repeat_count == 0; j += 1
    # all_note_data[i, j] = repeat_count == 1; j += 1
    # all_note_data[i, j] = repeat_count == 2; j += 1
    # all_note_data[i, j] = repeat_count == 3; j += 1
    # all_note_data[i, j] = repeat_count > 3; j += 1

    # EXTRA IDEAS
    # ------------
    # sec_duration

    # all_note_data[i, j] = note.all_length[chord.index] == 1; j += 1
    # all_note_data[i, j] = note.all_length[chord.index] == 2; j += 1
    # all_note_data[i, j] = note.all_length[chord.index] == 3; j += 1
    # all_note_data[i, j] = note.all_length[chord.index] == 4; j += 1
    # all_note_data[i, j] = note.all_length[chord.index] == 5; j += 1
    # all_note_data[i, j] = note.all_length[chord.index] == 6; j += 1
    # all_note_data[i, j] = note.all_length[chord.index] == 7; j += 1
    # all_note_data[i, j] = note.all_length[chord.index] > 8; j += 1

    # all_note_data[i, j] = note.all_index[chord.index] == 0; j += 1
    # all_note_data[i, j] = note.all_index[chord.index] == 1; j += 1
    # all_note_data[i, j] = note.all_index[chord.index] == 2; j += 1
    # all_note_data[i, j] = note.all_index[chord.index] == 3; j += 1
    # all_note_data[i, j] = note.all_index[chord.index] == 4; j += 1
    # all_note_data[i, j] = note.all_index[chord.index] == 5; j += 1
    # all_note_data[i, j] = note.all_index[chord.index] == 6; j += 1
    # all_note_data[i, j] = note.all_index[chord.index] == 7; j += 1
    # all_note_data[i, j] = note.all_index[chord.index] > 8; j += 1

  assert j == COUNT, j
