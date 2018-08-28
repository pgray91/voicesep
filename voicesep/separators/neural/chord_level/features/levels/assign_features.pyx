#cython: language_level=3
import cython

cdef int COUNT = 46

@cython.boundscheck(False)
@cython.wraparound(False)
cdef create(
  float[::1] assign_data,
  chord, tuple assignment, int voice_count, int empty_count
):
  cdef int assign_data_len = len(assign_data)
  assert assign_data_len == COUNT

  cdef int i = 0, kk = 0

  cdef float avg_pitch_prox = sum (
    sum(
      abs(note.pitch_space - voice.pitch_space) if voice else 0
      for voice in voices
    )
    for note, voices in zip(chord, assignment)
  ) / voice_count

  # Consider passing in conv and div count as arguments
  conv_count = sum(len(voices) > 1 for voices in assignment)

  voice_seen = {}
  for kk, voices in enumerate(assignment):
    for voice in voices:
      if voice is None:
        continue

      if voice in voice_seen:
        voice_seen[voice].append(chord[kk])
        continue

      voice_seen[voice] = [chord[kk]]
      for right_voice in voice.right:
        if right_voice.beat_onset >= chord.beat_onset:
          continue

        voice_seen[voice].append(right_voice.note)

  div_count = sum(len(notes) for _, notes in voice_seen.items())

  active_indices = [voice.active_index for voices in assignment for voice in voices if voice]
  has_cross = any(active_indices[kk] > active_indices[kk + 1] for kk in range(len(active_indices)-1))

  assign_data[i] = has_cross; i += 1
  assign_data[i] = not has_cross; i += 1

  assign_data[i] = avg_pitch_prox / 50; i += 1

  assign_data[i] = voice_count - empty_count == len(chord); i += 1
  assign_data[i] = voice_count - empty_count == len(chord) + 1; i += 1
  assign_data[i] = voice_count - empty_count == len(chord) - 1; i += 1
  assign_data[i] = voice_count - empty_count > len(chord) + 1; i += 1
  assign_data[i] = voice_count - empty_count < len(chord) - 1; i += 1

  assign_data[i] = voice_count == 0; i += 1
  assign_data[i] = voice_count == 1; i += 1
  assign_data[i] = voice_count == 2; i += 1
  assign_data[i] = voice_count == 3; i += 1
  assign_data[i] = voice_count == 4; i += 1
  assign_data[i] = voice_count == 5; i += 1
  assign_data[i] = voice_count == 6; i += 1
  assign_data[i] = voice_count == 7; i += 1
  assign_data[i] = voice_count == 8; i += 1
  assign_data[i] = voice_count == 9; i += 1
  assign_data[i] = voice_count == 10; i += 1
  assign_data[i] = voice_count == 11; i += 1
  assign_data[i] = voice_count > 11; i += 1

  assign_data[i] = empty_count == 0; i += 1
  assign_data[i] = empty_count == 1; i += 1
  assign_data[i] = empty_count == 2; i += 1
  assign_data[i] = empty_count == 3; i += 1
  assign_data[i] = empty_count == 4; i += 1
  assign_data[i] = empty_count == 5; i += 1
  assign_data[i] = empty_count == 6; i += 1
  assign_data[i] = empty_count == 7; i += 1
  assign_data[i] = empty_count > 7; i += 1

  assign_data[i] = len(chord) == 1; i += 1
  assign_data[i] = len(chord) == 2; i += 1
  assign_data[i] = len(chord) == 3; i += 1
  assign_data[i] = len(chord) == 4; i += 1
  assign_data[i] = len(chord) == 5; i += 1
  assign_data[i] = len(chord) == 6; i += 1
  assign_data[i] = len(chord) == 7; i += 1
  assign_data[i] = len(chord) > 7; i += 1

  assign_data[i] = conv_count == 0; i += 1
  assign_data[i] = conv_count == 1; i += 1
  assign_data[i] = conv_count == 2; i += 1
  assign_data[i] = conv_count == 3; i += 1

  assign_data[i] = div_count == 0; i += 1
  assign_data[i] = div_count == 1; i += 1
  assign_data[i] = div_count == 2; i += 1
  assign_data[i] = div_count == 3; i += 1

  # assign_data[i] = chord.beat_strength >= 0 and note.beat_strength < 0.2; i += 1
  # assign_data[i] = note.beat_strength >= 0.2 and note.beat_strength < 0.4; i += 1
  # assign_data[i] = note.beat_strength >= 0.4 and note.beat_strength < 0.6; i += 1
  # assign_data[i] = note.beat_strength >= 0.6 and note.beat_strength < 0.8; i += 1
  # assign_data[i] = note.beat_strength >= 0.8 and note.beat_strength < 1; i += 1
  # assign_data[i] = note.beat_strength >= 1; i += 1
  # ADD IN BEAT
  # average pitch distances

  assert i == COUNT, i
