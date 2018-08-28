#cython: language_level=3
import cython
import voicesep.utils.constants as const

cdef int COUNT = 111
cdef int PAD = 8

@cython.boundscheck(False)
@cython.wraparound(False)
cdef create(float[:,::1] div_data, float[:,::1] all_voice_data, chord, tuple assignment):
  cdef int div_data_len = len(div_data)
  assert div_data_len == PAD, div_data_len
  assert len(div_data[0, :]) == COUNT + len(all_voice_data[0, :])

  cdef int div_count = 0
  cdef int i, j = 0

  voice_seen = {}
  for i, voices in enumerate(assignment):
    for voice in voices:
      if voice is None:
        continue

      if voice in voice_seen:
        voice_seen[voice].append(chord[i])
        continue

      voice_seen[voice] = [chord[i]]
      for right_voice in voice.right:
        if right_voice.beat_onset >= chord.beat_onset:
          continue

        voice_seen[voice].append(right_voice.note)

  for voice, notes in voice_seen.items():
    if len(notes) == 1:
      continue

    notes.sort(key=lambda n : n.pitch_space)

    avg_div_pitch = sum(note.pitch_space for note in notes) / len(notes)

    avg_pitch_dist = sum(
      abs(voice.pitch_space - note.pitch_space) 
      for note in notes
    ) / len(notes)

    max_pitch_dist = max(
      abs(voice.pitch_space - note.pitch_space) 
      for note in notes
    )

    avg_beat_dist = sum(
      max(0, float(note.beat_onset - voice.beat_offset))
      for note in notes
    ) / len(notes)

    max_beat_dist = max(
      max(0, float(note.beat_onset - voice.beat_offset))
      for note in notes
    )

    div_notes_above = sum(
      note.pitch_space > voice.pitch_space for note in notes
    )
    div_notes_below = sum(
      note.pitch_space < voice.pitch_space for note in notes
    )
    div_notes_equal = sum(
      note.pitch_space == voice.pitch_space for note in notes
    )

    conv_notes = voice.conv_notes

    j = 0

    div_data[div_count, j] = 0; j += 1

    # Pitch
    div_data[div_count, j] = abs(avg_div_pitch - voice.pitch_space) / const.MAX_PITCH_DISTANCE; j += 1
    div_data[div_count, j] = avg_div_pitch > voice.pitch_space; j += 1
    div_data[div_count, j] = avg_div_pitch < voice.pitch_space; j += 1
    div_data[div_count, j] = avg_div_pitch == voice.pitch_space; j += 1

    div_data[div_count, j] = avg_pitch_dist / const.MAX_PITCH_DISTANCE; j += 1
    div_data[div_count, j] = max_pitch_dist / const.MAX_PITCH_DISTANCE; j += 1

    div_data[div_count, j] = abs(notes[0].pitch_space - voice.pitch_space) / const.MAX_PITCH_DISTANCE; j += 1
    div_data[div_count, j] = notes[0].pitch_space > voice.pitch_space; j += 1
    div_data[div_count, j] = notes[0].pitch_space < voice.pitch_space; j += 1
    div_data[div_count, j] = notes[0].pitch_space == voice.pitch_space; j += 1

    div_data[div_count, j] = abs(notes[len(notes)-1].pitch_space - voice.pitch_space) / const.MAX_PITCH_DISTANCE; j += 1
    div_data[div_count, j] = notes[len(notes)-1].pitch_space > voice.pitch_space; j += 1
    div_data[div_count, j] = notes[len(notes)-1].pitch_space < voice.pitch_space; j += 1
    div_data[div_count, j] = notes[len(notes)-1].pitch_space == voice.pitch_space; j += 1

    div_data[div_count, j] = abs(notes[0].pitch_space - notes[len(notes)-1].pitch_space) / const.MAX_PITCH_DISTANCE; j += 1

    # above
    div_data[div_count, j] = abs(notes[0].pitch_space - notes[1].pitch_space) / const.MAX_PITCH_DISTANCE; j += 1

    div_data[div_count, j] = abs(notes[1].pitch_space - voice.pitch_space) / const.MAX_PITCH_DISTANCE; j += 1
    div_data[div_count, j] = notes[1].pitch_space > voice.pitch_space; j += 1
    div_data[div_count, j] = notes[1].pitch_space < voice.pitch_space; j += 1
    div_data[div_count, j] = notes[1].pitch_space == voice.pitch_space; j += 1

    div_data[div_count, j] = abs(notes[0].pitch_space - conv_notes[0].pitch_space) / const.MAX_PITCH_DISTANCE if len(conv_notes) > 1 else 1; j += 1
    div_data[div_count, j] = notes[0].pitch_space > conv_notes[0].pitch_space if len(conv_notes) > 1 else 0; j += 1
    div_data[div_count, j] = notes[0].pitch_space < conv_notes[0].pitch_space if len(conv_notes) > 1 else 0; j += 1
    div_data[div_count, j] = notes[0].pitch_space == conv_notes[0].pitch_space if len(conv_notes) > 1 else 0; j += 1

    div_data[div_count, j] = abs(notes[0].pitch_space - conv_notes[len(conv_notes)-1].pitch_space) / const.MAX_PITCH_DISTANCE if len(conv_notes) > 1 else 1; j += 1
    div_data[div_count, j] = notes[0].pitch_space > conv_notes[len(conv_notes)-1].pitch_space if len(conv_notes) > 1 else 0; j += 1
    div_data[div_count, j] = notes[0].pitch_space < conv_notes[len(conv_notes)-1].pitch_space if len(conv_notes) > 1 else 0; j += 1
    div_data[div_count, j] = notes[0].pitch_space == conv_notes[len(conv_notes)-1].pitch_space if len(conv_notes) > 1 else 0; j += 1

    div_data[div_count, j] = abs(notes[1].pitch_space - conv_notes[0].pitch_space) / const.MAX_PITCH_DISTANCE if len(conv_notes) > 1 else 1; j += 1
    div_data[div_count, j] = notes[1].pitch_space > conv_notes[0].pitch_space if len(conv_notes) > 1 else 0; j += 1
    div_data[div_count, j] = notes[1].pitch_space < conv_notes[0].pitch_space if len(conv_notes) > 1 else 0; j += 1
    div_data[div_count, j] = notes[1].pitch_space == conv_notes[0].pitch_space if len(conv_notes) > 1 else 0; j += 1

    div_data[div_count, j] = abs(notes[1].pitch_space - conv_notes[len(conv_notes)-1].pitch_space) / const.MAX_PITCH_DISTANCE if len(conv_notes) > 1 else 1; j += 1
    div_data[div_count, j] = notes[1].pitch_space > conv_notes[len(conv_notes)-1].pitch_space if len(conv_notes) > 1 else 0; j += 1
    div_data[div_count, j] = notes[1].pitch_space < conv_notes[len(conv_notes)-1].pitch_space if len(conv_notes) > 1 else 0; j += 1
    div_data[div_count, j] = notes[1].pitch_space == conv_notes[len(conv_notes)-1].pitch_space if len(conv_notes) > 1 else 0; j += 1

    # below
    div_data[div_count, j] = abs(notes[len(notes)-2].pitch_space - notes[len(notes)-1].pitch_space) / const.MAX_PITCH_DISTANCE; j += 1

    div_data[div_count, j] = abs(notes[len(notes)-2].pitch_space - voice.pitch_space) / const.MAX_PITCH_DISTANCE; j += 1
    div_data[div_count, j] = notes[len(notes)-2].pitch_space > voice.pitch_space; j += 1
    div_data[div_count, j] = notes[len(notes)-2].pitch_space < voice.pitch_space; j += 1
    div_data[div_count, j] = notes[len(notes)-2].pitch_space == voice.pitch_space; j += 1

    div_data[div_count, j] = abs(notes[len(notes)-2].pitch_space - conv_notes[0].pitch_space) / const.MAX_PITCH_DISTANCE if len(conv_notes) > 1 else 1; j += 1
    div_data[div_count, j] = notes[len(notes)-2].pitch_space > conv_notes[0].pitch_space if len(conv_notes) > 1 else 0; j += 1
    div_data[div_count, j] = notes[len(notes)-2].pitch_space < conv_notes[0].pitch_space if len(conv_notes) > 1 else 0; j += 1
    div_data[div_count, j] = notes[len(notes)-2].pitch_space == conv_notes[0].pitch_space if len(conv_notes) > 1 else 0; j += 1

    div_data[div_count, j] = abs(notes[len(notes)-2].pitch_space - conv_notes[len(conv_notes)-1].pitch_space) / const.MAX_PITCH_DISTANCE if len(conv_notes) > 1 else 1; j += 1
    div_data[div_count, j] = notes[len(notes)-2].pitch_space > conv_notes[len(conv_notes)-1].pitch_space if len(conv_notes) > 1 else 0; j += 1
    div_data[div_count, j] = notes[len(notes)-2].pitch_space < conv_notes[len(conv_notes)-1].pitch_space if len(conv_notes) > 1 else 0; j += 1
    div_data[div_count, j] = notes[len(notes)-2].pitch_space == conv_notes[len(conv_notes)-1].pitch_space if len(conv_notes) > 1 else 0; j += 1

    div_data[div_count, j] = abs(notes[len(notes)-1].pitch_space - conv_notes[0].pitch_space) / const.MAX_PITCH_DISTANCE if len(conv_notes) > 1 else 1; j += 1
    div_data[div_count, j] = notes[len(notes)-1].pitch_space > conv_notes[0].pitch_space if len(conv_notes) > 1 else 0; j += 1
    div_data[div_count, j] = notes[len(notes)-1].pitch_space < conv_notes[0].pitch_space if len(conv_notes) > 1 else 0; j += 1
    div_data[div_count, j] = notes[len(notes)-1].pitch_space == conv_notes[0].pitch_space if len(conv_notes) > 1 else 0; j += 1

    div_data[div_count, j] = abs(notes[len(notes)-1].pitch_space - conv_notes[len(conv_notes)-1].pitch_space) / const.MAX_PITCH_DISTANCE if len(conv_notes) > 1 else 1; j += 1
    div_data[div_count, j] = notes[len(notes)-1].pitch_space > conv_notes[len(conv_notes)-1].pitch_space if len(conv_notes) > 1 else 0; j += 1
    div_data[div_count, j] = notes[len(notes)-1].pitch_space < conv_notes[len(conv_notes)-1].pitch_space if len(conv_notes) > 1 else 0; j += 1
    div_data[div_count, j] = notes[len(notes)-1].pitch_space == conv_notes[len(conv_notes)-1].pitch_space if len(conv_notes) > 1 else 0; j += 1

    # conv
    div_data[div_count, j] = abs(conv_notes[0].pitch_space - conv_notes[len(conv_notes) - 1].pitch_space) / const.MAX_PITCH_DISTANCE if len(conv_notes) > 1 else 1; j += 1

    # Temporal

    div_data[div_count, j] = avg_beat_dist / const.MAX_BEAT_ONSET_OFFSET; j += 1
    div_data[div_count, j] = max_beat_dist / const.MAX_BEAT_ONSET_OFFSET; j += 1

    div_data[div_count, j] = max(0, float(notes[0].beat_onset - voice.beat_offset)) / const.MAX_BEAT_ONSET_OFFSET; j += 1
    div_data[div_count, j] = voice.beat_offset > notes[0].beat_onset; j += 1
    div_data[div_count, j] = voice.beat_offset < notes[0].beat_onset; j += 1
    div_data[div_count, j] = voice.beat_offset == notes[0].beat_onset; j += 1

    div_data[div_count, j] = max(0, float(notes[len(notes)-1].beat_onset - voice.beat_offset)) / const.MAX_BEAT_ONSET_OFFSET; j += 1
    div_data[div_count, j] = voice.beat_offset > notes[len(notes)-1].beat_onset; j += 1
    div_data[div_count, j] = voice.beat_offset < notes[len(notes)-1].beat_onset; j += 1
    div_data[div_count, j] = voice.beat_offset == notes[len(notes)-1].beat_onset; j += 1

    # above
    div_data[div_count, j] = abs(notes[0].beat_duration - notes[1].beat_duration) / const.MAX_BEAT_DUR_DISTANCE; j += 1

    div_data[div_count, j] = max(0, float(notes[1].beat_onset - voice.beat_offset)) / const.MAX_BEAT_ONSET_OFFSET; j += 1
    div_data[div_count, j] = notes[1].beat_offset > voice.beat_onset; j += 1
    div_data[div_count, j] = notes[1].beat_offset < voice.beat_onset; j += 1
    div_data[div_count, j] = notes[1].beat_offset == voice.beat_onset; j += 1

    div_data[div_count, j] = notes[0].beat_onset > notes[1].beat_onset; j += 1
    div_data[div_count, j] = notes[0].beat_onset < notes[1].beat_onset; j += 1
    div_data[div_count, j] = notes[0].beat_onset == notes[1].beat_onset; j += 1

    # below
    div_data[div_count, j] = abs(notes[len(notes)-2].beat_duration - notes[len(notes)-1].beat_duration) / const.MAX_BEAT_DUR_DISTANCE; j += 1

    div_data[div_count, j] = max(0, float(notes[len(notes)-2].beat_onset - voice.beat_offset)) / const.MAX_BEAT_ONSET_OFFSET; j += 1
    div_data[div_count, j] = notes[len(notes)-2].beat_offset > voice.beat_onset; j += 1
    div_data[div_count, j] = notes[len(notes)-2].beat_offset < voice.beat_onset; j += 1
    div_data[div_count, j] = notes[len(notes)-2].beat_offset == voice.beat_onset; j += 1

    div_data[div_count, j] = notes[len(notes)-2].beat_onset > notes[len(notes)-1].beat_onset; j += 1
    div_data[div_count, j] = notes[len(notes)-2].beat_onset < notes[len(notes)-1].beat_onset; j += 1
    div_data[div_count, j] = notes[len(notes)-2].beat_onset == notes[len(notes)-1].beat_onset; j += 1

    # Positional
    div_data[div_count, j] = abs(notes[0].index - notes[1].index) / const.MAX_INDEX_DISTANCE if notes[0].beat_onset == notes[1].beat_onset else 1; j += 1
    div_data[div_count, j] = notes[0].index == notes[1].index - 1 if notes[0].beat_onset == notes[1].beat_onset else 0; j += 1
    div_data[div_count, j] = notes[0].index == notes[1].index - 2 if notes[0].beat_onset == notes[1].beat_onset else 0; j += 1
    div_data[div_count, j] = notes[0].index < notes[1].index - 2 if notes[0].beat_onset == notes[1].beat_onset else 0; j += 1

    div_data[div_count, j] = abs(notes[len(notes)-2].index - notes[len(notes)-1].index) / const.MAX_INDEX_DISTANCE if notes[len(notes)-2].beat_onset == notes[len(notes)-1].beat_onset else 1; j += 1
    div_data[div_count, j] = notes[len(notes)-2].index == notes[len(notes)-1].index - 1 if notes[len(notes)-2].beat_onset == notes[len(notes)-1].beat_onset else 0; j += 1
    div_data[div_count, j] = notes[len(notes)-2].index == notes[len(notes)-1].index - 2 if notes[len(notes)-2].beat_onset == notes[len(notes)-1].beat_onset else 0; j += 1
    div_data[div_count, j] = notes[len(notes)-2].index < notes[len(notes)-1].index - 2 if notes[len(notes)-2].beat_onset == notes[len(notes)-1].beat_onset else 0; j += 1

    div_data[div_count, j] = len(notes) == 2; j += 1
    div_data[div_count, j] = len(notes) == 3; j += 1
    div_data[div_count, j] = len(notes) == 4; j += 1
    div_data[div_count, j] = len(notes) == 5; j += 1

    div_data[div_count, j] = div_notes_above == 0; j += 1
    div_data[div_count, j] = div_notes_above == 1; j += 1
    div_data[div_count, j] = div_notes_above == 2; j += 1
    div_data[div_count, j] = div_notes_above == 3; j += 1

    div_data[div_count, j] = div_notes_below == 0; j += 1
    div_data[div_count, j] = div_notes_below == 1; j += 1
    div_data[div_count, j] = div_notes_below == 2; j += 1
    div_data[div_count, j] = div_notes_below == 3; j += 1

    div_data[div_count, j] = div_notes_equal == 0; j += 1
    div_data[div_count, j] = div_notes_equal == 1; j += 1
    div_data[div_count, j] = div_notes_equal == 2; j += 1
    div_data[div_count, j] = div_notes_equal == 3; j += 1

    div_data[div_count, j] = all(
      notes[i].chord_index == notes[i+1].chord_index
      for i in range(len(notes) - 1)
    ); j += 1

    div_data[div_count, j] = len(conv_notes) > 1; j += 1

    # Voice features
    div_data[div_count, j:] = all_voice_data[<int> voice.subset_index, :]

    div_count += 1

  if div_count > 0:
    assert div_count <= PAD, div_count
    assert j == COUNT, j

    for i in range(div_count, PAD):
      div_data[i, :] = div_data[i - 1, :]

  else:
    div_data[...] = 0
    for i in range(PAD):
      div_data[i, 0] = 1
