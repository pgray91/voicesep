#cython: language_level=3
import cython
import voicesep.utils.constants as const

# conv_data[conv_count, j] = any(voice.blocked for voice in voices); j += 1

cdef int COUNT = 155
cdef int PAD = 6

@cython.boundscheck(False)
@cython.wraparound(False)
cdef create(float[:,::1] conv_data, float[:,::1] all_note_data, chord, tuple assignment, float beat_horizon):
  cdef int conv_data_len = len(conv_data)
  assert conv_data_len == PAD, conv_data_len
  assert len(conv_data[0, :]) == COUNT + len(all_note_data[0, :])


  cdef int conv_count = 0
  cdef int i, j = 0

  for note, voices in zip(chord, assignment):
    if len(voices) == 1:
      continue

    avg_conv_pitch = sum(voice.pitch_space for voice in voices) / len(voices)

    avg_pitch_dist = sum(
      abs(voice.pitch_space - note.pitch_space) 
      for voice in voices
    ) / len(voices)

    max_pitch_dist = max(
      abs(voice.pitch_space - note.pitch_space) 
      for voice in voices
    )

    avg_beat_dist = sum(
      max(0, float(note.beat_onset - voice.beat_offset))
      for voice in voices
    ) / len(voices)

    max_beat_dist = max(
      max(0, float(note.beat_onset - voice.beat_offset))
      for voice in voices
    )

    conv_notes_above = sum(
      voice.pitch_space > note.pitch_space for voice in voices
    )
    conv_notes_below = sum(
      voice.pitch_space < note.pitch_space for voice in voices
    )
    conv_notes_equal = sum(
      voice.pitch_space == note.pitch_space for voice in voices
    )

    num_complete = sum(voice.position == 0 for voice in voices)
    num_partial = sum(voice.position > 0 for voice in voices)

    top_div_note = None
    if (
      voices[0] not in voices[1].all_right and 
      voices[1] not in voices[0].all_right
    ):
      top_div_notes = list(set(voices[0].div_notes) & set(voices[1].div_notes))
      top_div_notes.sort(key=lambda n : n.beat_onset)
      top_div_note = (
        None if len(top_div_notes) == 0 
        else top_div_notes[len(top_div_notes) - 1]
      )

    bottom_div_note = None
    if (
      voices[len(voices)-2] not in voices[len(voices)-1].all_right and 
      voices[len(voices)-2] not in voices[len(voices)-1].all_right
    ):
      bottom_div_notes = list(
        set(voices[len(voices)-2].div_notes) & 
        set(voices[len(voices)-1].div_notes)
      )
      bottom_div_notes.sort(key=lambda n : n.beat_onset)
      bottom_div_note = (
        None if len(bottom_div_notes) == 0 
        else bottom_div_notes[len(bottom_div_notes) - 1]
      )

    div_note = None
    for i, voice1 in enumerate(voices):
      for voice2 in voices[i+1:]:
        if voice1 in voice2.all_right or voice2 in voice1.all_right:
          break
      else:
        continue

      break
    else:
      div_notes = set(voices[0].div_notes)
      for voice in voices[1:]:
        div_notes &= set(voice.div_notes)

      div_notes = list(div_notes)
      div_notes.sort(key=lambda n : n.beat_onset)
      div_note = None if len(div_notes) == 0 else div_notes[len(div_notes) - 1]

    # assert div_note is None

    top_voices = []
    top_voice = voices[0]
    for _ in range(voices[0].length_bottom + 1):
      if top_voice is top_div_note:
        break

      top_voices.append(top_voice)
      if len(top_voice.left) == 0:
        break
      top_voice = top_voice.left[len(top_voice.left) - 1]
      if note.beat_onset - top_voice.beat_offset > beat_horizon:
        break

    bottom_voices = []
    bottom_voice = voices[1]
    for _ in range(voices[1].length_top + 1):
      if bottom_voice is top_div_note:
        break

      bottom_voices.append(bottom_voice)
      if len(bottom_voice.left) == 0:
        break
      bottom_voice = bottom_voice.left[0]
      if note.beat_onset - bottom_voice.beat_offset > beat_horizon:
        break

    top_beat_onsets = set(v.beat_onset for v in top_voices)
    bottom_beat_onsets = set(v.beat_onset for v in bottom_voices)

    shared_beat_onsets = list(top_beat_onsets & bottom_beat_onsets)

    top_voices = [v for v in top_voices if v.beat_onset in shared_beat_onsets]
    bottom_voices = [v for v in bottom_voices if v.beat_onset in shared_beat_onsets]

    assert len(top_voices) == len(bottom_voices)

    above_length = len(top_beat_onsets | bottom_beat_onsets)
    above_shared_count = len(top_voices)
    above_pitch_dis_avg = (
      sum(
        abs(top_v.pitch_space - bot_v.pitch_space)
        for top_v, bot_v in zip(top_voices, bottom_voices)
      ) + (
        const.MAX_PITCH_DISTANCE * (above_length - len(top_voices))
      )
    ) / above_length

    above_dur_dis_avg = (
      sum(
        abs(float(top_v.note.beat_duration - bot_v.note.beat_duration))
        for top_v, bot_v in zip(top_voices, bottom_voices)
      ) + (
        const.MAX_BEAT_DUR_DISTANCE * (above_length - len(top_voices))
      )
    ) / above_length

    above_index_dis_avg = (
      sum(
        abs(top_v.note.index - bot_v.note.index)
        for top_v, bot_v in zip(top_voices, bottom_voices)
      ) + (
        const.MAX_INDEX_DISTANCE * (above_length - len(top_voices))
      )
    ) / above_length

    # Below comparison
    top_voices = []
    top_voice = voices[len(voices)-2]
    for _ in range(voices[0].length_bottom + 1):
      if top_voice is top_div_note:
        break

      top_voices.append(top_voice)
      if len(top_voice.left) == 0:
        break
      top_voice = top_voice.left[len(top_voice.left) - 1]
      if note.beat_onset - top_voice.beat_offset > beat_horizon:
        break

    bottom_voices = []
    bottom_voice = voices[len(voices)-1]
    for _ in range(voices[len(voices)-1].length_top + 1):
      if bottom_voice is top_div_note:
        break

      bottom_voices.append(bottom_voice)
      if len(bottom_voice.left) == 0:
        break
      bottom_voice = bottom_voice.left[0]
      if note.beat_onset - bottom_voice.beat_offset > beat_horizon:
        break

    top_beat_onsets = set(v.beat_onset for v in top_voices)
    bottom_beat_onsets = set(v.beat_onset for v in bottom_voices)

    shared_beat_onsets = list(top_beat_onsets & bottom_beat_onsets)

    top_voices = [v for v in top_voices if v.beat_onset in shared_beat_onsets]
    bottom_voices = [v for v in bottom_voices if v.beat_onset in shared_beat_onsets]

    assert len(top_voices) == len(bottom_voices)

    below_length = len(top_beat_onsets | bottom_beat_onsets)
    below_shared_count = len(top_voices)
    below_pitch_dis_avg = (
      sum(
        abs(top_v.pitch_space - bot_v.pitch_space)
        for top_v, bot_v in zip(top_voices, bottom_voices)
      ) + (
        const.MAX_PITCH_DISTANCE * (below_length - len(top_voices)) 
      )
    ) / below_length

    below_dur_dis_avg = (
      sum(
        abs(float(top_v.note.beat_duration - bot_v.note.beat_duration))
        for top_v, bot_v in zip(top_voices, bottom_voices)
      ) + (
        const.MAX_BEAT_DUR_DISTANCE * (below_length - len(top_voices))
      )
    ) / below_length

    below_index_dis_avg = (
      sum(
        abs(top_v.note.index - bot_v.note.index)
        for top_v, bot_v in zip(top_voices, bottom_voices)
      ) + (
        const.MAX_INDEX_DISTANCE * (below_length - len(top_voices))
      )
    ) / below_length

    j = 0

    conv_data[conv_count, j] = 0; j += 1

    # Pitch
    conv_data[conv_count, j] = abs(avg_conv_pitch - note.pitch_space) / const.MAX_PITCH_DISTANCE; j += 1
    conv_data[conv_count, j] = avg_conv_pitch > note.pitch_space; j += 1
    conv_data[conv_count, j] = avg_conv_pitch < note.pitch_space; j += 1
    conv_data[conv_count, j] = avg_conv_pitch == note.pitch_space; j += 1

    conv_data[conv_count, j] = avg_pitch_dist / const.MAX_PITCH_DISTANCE; j += 1
    conv_data[conv_count, j] = max_pitch_dist / const.MAX_PITCH_DISTANCE; j += 1

    conv_data[conv_count, j] = abs(voices[0].pitch_space - note.pitch_space) / const.MAX_PITCH_DISTANCE; j += 1
    conv_data[conv_count, j] = voices[0].pitch_space > note.pitch_space; j += 1
    conv_data[conv_count, j] = voices[0].pitch_space < note.pitch_space; j += 1
    conv_data[conv_count, j] = voices[0].pitch_space == note.pitch_space; j += 1

    conv_data[conv_count, j] = abs(voices[len(voices)-1].pitch_space - note.pitch_space) / const.MAX_PITCH_DISTANCE; j += 1
    conv_data[conv_count, j] = voices[len(voices)-1].pitch_space > note.pitch_space; j += 1
    conv_data[conv_count, j] = voices[len(voices)-1].pitch_space < note.pitch_space; j += 1
    conv_data[conv_count, j] = voices[len(voices)-1].pitch_space == note.pitch_space; j += 1

    conv_data[conv_count, j] = abs(voices[0].pitch_space - voices[len(voices)-1].pitch_space) / const.MAX_PITCH_DISTANCE; j += 1

    # above
    conv_data[conv_count, j] = abs(voices[0].pitch_space - voices[1].pitch_space) / const.MAX_PITCH_DISTANCE; j += 1
    conv_data[conv_count, j] = above_pitch_dis_avg / const.MAX_PITCH_DISTANCE; j += 1

    conv_data[conv_count, j] = abs(note.pitch_space - voices[1].pitch_space) / const.MAX_PITCH_DISTANCE; j += 1
    conv_data[conv_count, j] = note.pitch_space > voices[1].pitch_space; j += 1
    conv_data[conv_count, j] = note.pitch_space < voices[1].pitch_space; j += 1
    conv_data[conv_count, j] = note.pitch_space == voices[1].pitch_space; j += 1

    conv_data[conv_count, j] = 1 if top_div_note is None else abs(
      note.pitch_space - top_div_note.pitch_space
    ) / const.MAX_PITCH_DISTANCE; j += 1

    # below
    conv_data[conv_count, j] = abs(voices[len(voices)-2].pitch_space - voices[len(voices)-1].pitch_space) / const.MAX_PITCH_DISTANCE; j += 1
    conv_data[conv_count, j] = below_pitch_dis_avg / const.MAX_PITCH_DISTANCE; j += 1

    conv_data[conv_count, j] = abs(note.pitch_space - voices[len(voices)-2].pitch_space) / const.MAX_PITCH_DISTANCE; j += 1
    conv_data[conv_count, j] = note.pitch_space > voices[len(voices)-2].pitch_space; j += 1
    conv_data[conv_count, j] = note.pitch_space < voices[len(voices)-2].pitch_space; j += 1
    conv_data[conv_count, j] = note.pitch_space == voices[len(voices)-2].pitch_space; j += 1

    conv_data[conv_count, j] = 1 if bottom_div_note is None else abs(
      note.pitch_space - bottom_div_note.pitch_space
    ) / const.MAX_PITCH_DISTANCE; j += 1
    
    # Div note
    conv_data[conv_count, j] = 1 if div_note is None else abs(
      note.pitch_space - div_note.pitch_space
    ) / const.MAX_PITCH_DISTANCE; j += 1

    # Temporal
    conv_data[conv_count, j] = avg_beat_dist / const.MAX_BEAT_ONSET_OFFSET; j += 1
    conv_data[conv_count, j] = max_beat_dist / const.MAX_BEAT_ONSET_OFFSET; j += 1

    conv_data[conv_count, j] = max(0, float(note.beat_onset - voices[0].beat_offset)) / const.MAX_BEAT_ONSET_OFFSET; j += 1
    conv_data[conv_count, j] = voices[0].beat_offset > note.beat_onset; j += 1
    conv_data[conv_count, j] = voices[0].beat_offset < note.beat_onset; j += 1
    conv_data[conv_count, j] = voices[0].beat_offset == note.beat_onset; j += 1

    conv_data[conv_count, j] = max(0, float(note.beat_onset - voices[len(voices)-1].beat_offset)) / const.MAX_BEAT_ONSET_OFFSET; j += 1
    conv_data[conv_count, j] = voices[len(voices)-1].beat_offset > note.beat_onset; j += 1
    conv_data[conv_count, j] = voices[len(voices)-1].beat_offset < note.beat_onset; j += 1
    conv_data[conv_count, j] = voices[len(voices)-1].beat_offset == note.beat_onset; j += 1

    # above
    conv_data[conv_count, j] = above_dur_dis_avg / const.MAX_BEAT_DUR_DISTANCE; j += 1

    conv_data[conv_count, j] = max(0, float(note.beat_onset - voices[1].beat_offset)) / const.MAX_BEAT_ONSET_OFFSET; j += 1
    conv_data[conv_count, j] = voices[1].beat_offset > note.beat_onset; j += 1
    conv_data[conv_count, j] = voices[1].beat_offset < note.beat_onset; j += 1
    conv_data[conv_count, j] = voices[1].beat_offset == note.beat_onset; j += 1

    conv_data[conv_count, j] = voices[0].beat_onset > voices[1].beat_onset; j += 1
    conv_data[conv_count, j] = voices[0].beat_onset < voices[1].beat_onset; j += 1
    conv_data[conv_count, j] = voices[0].beat_onset == voices[1].beat_onset; j += 1

    # below
    conv_data[conv_count, j] = below_dur_dis_avg / const.MAX_BEAT_DUR_DISTANCE; j += 1

    conv_data[conv_count, j] = max(0, float(note.beat_onset - voices[len(voices)-2].beat_offset)) / const.MAX_BEAT_ONSET_OFFSET; j += 1
    conv_data[conv_count, j] = voices[len(voices)-2].beat_offset > note.beat_onset; j += 1
    conv_data[conv_count, j] = voices[len(voices)-2].beat_offset < note.beat_onset; j += 1
    conv_data[conv_count, j] = voices[len(voices)-2].beat_offset == note.beat_onset; j += 1

    conv_data[conv_count, j] = voices[len(voices)-2].beat_onset > voices[len(voices)-1].beat_onset; j += 1
    conv_data[conv_count, j] = voices[len(voices)-2].beat_onset < voices[len(voices)-1].beat_onset; j += 1
    conv_data[conv_count, j] = voices[len(voices)-2].beat_onset == voices[len(voices)-1].beat_onset; j += 1

    # Positional

    # above
    conv_data[conv_count, j] = voices[0].position == 0; j += 1
    conv_data[conv_count, j] = voices[1].position == 0; j += 1

    conv_data[conv_count, j] = abs(voices[0].note.index - voices[1].note.index) / const.MAX_INDEX_DISTANCE if voices[0].beat_onset == voices[1].beat_onset else 1; j += 1
    conv_data[conv_count, j] = voices[0].note.index == voices[1].note.index - 1 if voices[0].beat_onset == voices[1].beat_onset else 0; j += 1
    conv_data[conv_count, j] = voices[0].note.index == voices[1].note.index - 2 if voices[0].beat_onset == voices[1].beat_onset else 0; j += 1
    conv_data[conv_count, j] = voices[0].note.index < voices[1].note.index - 2 if voices[0].beat_onset == voices[1].beat_onset else 0; j += 1

    conv_data[conv_count, j] = abs(voices[0].subset_index - voices[1].subset_index) / const.MAX_INDEX_DISTANCE; j += 1
    conv_data[conv_count, j] = voices[0].subset_index == voices[1].subset_index - 1; j += 1
    conv_data[conv_count, j] = voices[0].subset_index == voices[1].subset_index - 2; j += 1
    conv_data[conv_count, j] = voices[0].subset_index < voices[1].subset_index - 2; j += 1

    conv_data[conv_count, j] = above_index_dis_avg / const.MAX_INDEX_DISTANCE; j += 1
    conv_data[conv_count, j] = (above_length - above_shared_count) / const.MAX_LENGTH_DISTANCE; j += 1

    conv_data[conv_count, j] = above_length == 1; j += 1
    conv_data[conv_count, j] = above_length == 2; j += 1
    conv_data[conv_count, j] = above_length == 3; j += 1
    conv_data[conv_count, j] = above_length == 4; j += 1
    conv_data[conv_count, j] = above_length == 5; j += 1
    conv_data[conv_count, j] = above_length == 6; j += 1
    conv_data[conv_count, j] = above_length == 7; j += 1
    conv_data[conv_count, j] = above_length == 8; j += 1
    conv_data[conv_count, j] = above_length == 9; j += 1
    conv_data[conv_count, j] = above_length > 9; j += 1

    conv_data[conv_count, j] = above_shared_count == 0; j += 1
    conv_data[conv_count, j] = above_shared_count == 1; j += 1
    conv_data[conv_count, j] = above_shared_count == 2; j += 1
    conv_data[conv_count, j] = above_shared_count == 3; j += 1
    conv_data[conv_count, j] = above_shared_count == 4; j += 1
    conv_data[conv_count, j] = above_shared_count == 5; j += 1
    conv_data[conv_count, j] = above_shared_count == 6; j += 1
    conv_data[conv_count, j] = above_shared_count == 7; j += 1
    conv_data[conv_count, j] = above_shared_count == 8; j += 1
    conv_data[conv_count, j] = above_shared_count == 9; j += 1
    conv_data[conv_count, j] = above_shared_count > 9; j += 1

    # below
    conv_data[conv_count, j] = voices[len(voices)-2].position == 0; j += 1
    conv_data[conv_count, j] = voices[len(voices)-1].position == 0; j += 1

    conv_data[conv_count, j] = abs(voices[len(voices)-2].note.index - voices[len(voices)-1].note.index) / const.MAX_INDEX_DISTANCE if voices[len(voices)-2].beat_onset == voices[len(voices)-1].beat_onset else 1; j += 1
    conv_data[conv_count, j] = voices[len(voices)-2].note.index == voices[len(voices)-1].note.index - 1 if voices[len(voices)-2].beat_onset == voices[len(voices)-1].beat_onset else 0; j += 1
    conv_data[conv_count, j] = voices[len(voices)-2].note.index == voices[len(voices)-1].note.index - 2 if voices[len(voices)-2].beat_onset == voices[len(voices)-1].beat_onset else 0; j += 1
    conv_data[conv_count, j] = voices[len(voices)-2].note.index < voices[len(voices)-1].note.index - 2 if voices[len(voices)-2].beat_onset == voices[len(voices)-1].beat_onset else 0; j += 1

    conv_data[conv_count, j] = abs(voices[len(voices)-2].subset_index - voices[len(voices)-1].subset_index) / const.MAX_INDEX_DISTANCE; j += 1
    conv_data[conv_count, j] = voices[len(voices)-2].subset_index == voices[len(voices)-1].subset_index - 1; j += 1
    conv_data[conv_count, j] = voices[len(voices)-2].subset_index == voices[len(voices)-1].subset_index - 2; j += 1
    conv_data[conv_count, j] = voices[len(voices)-2].subset_index < voices[len(voices)-1].subset_index - 2; j += 1

    conv_data[conv_count, j] = below_index_dis_avg / const.MAX_INDEX_DISTANCE; j += 1
    conv_data[conv_count, j] = (below_length - below_shared_count) / const.MAX_LENGTH_DISTANCE; j += 1

    conv_data[conv_count, j] = below_length == 1; j += 1
    conv_data[conv_count, j] = below_length == 2; j += 1
    conv_data[conv_count, j] = below_length == 3; j += 1
    conv_data[conv_count, j] = below_length == 4; j += 1
    conv_data[conv_count, j] = below_length == 5; j += 1
    conv_data[conv_count, j] = below_length == 6; j += 1
    conv_data[conv_count, j] = below_length == 7; j += 1
    conv_data[conv_count, j] = below_length == 8; j += 1
    conv_data[conv_count, j] = below_length == 9; j += 1
    conv_data[conv_count, j] = below_length > 9; j += 1

    conv_data[conv_count, j] = below_shared_count == 0; j += 1
    conv_data[conv_count, j] = below_shared_count == 1; j += 1
    conv_data[conv_count, j] = below_shared_count == 2; j += 1
    conv_data[conv_count, j] = below_shared_count == 3; j += 1
    conv_data[conv_count, j] = below_shared_count == 4; j += 1
    conv_data[conv_count, j] = below_shared_count == 5; j += 1
    conv_data[conv_count, j] = below_shared_count == 6; j += 1
    conv_data[conv_count, j] = below_shared_count == 7; j += 1
    conv_data[conv_count, j] = below_shared_count == 8; j += 1
    conv_data[conv_count, j] = below_shared_count == 9; j += 1
    conv_data[conv_count, j] = below_shared_count > 9; j += 1

    conv_data[conv_count, j] = len(voices) == 2; j += 1
    conv_data[conv_count, j] = len(voices) == 3; j += 1
    conv_data[conv_count, j] = len(voices) == 4; j += 1
    conv_data[conv_count, j] = len(voices) == 5; j += 1

    conv_data[conv_count, j] = conv_notes_above == 0; j += 1
    conv_data[conv_count, j] = conv_notes_above == 1; j += 1
    conv_data[conv_count, j] = conv_notes_above == 2; j += 1
    conv_data[conv_count, j] = conv_notes_above == 3; j += 1

    conv_data[conv_count, j] = conv_notes_below == 0; j += 1
    conv_data[conv_count, j] = conv_notes_below == 1; j += 1
    conv_data[conv_count, j] = conv_notes_below == 2; j += 1
    conv_data[conv_count, j] = conv_notes_below == 3; j += 1

    conv_data[conv_count, j] = conv_notes_equal == 0; j += 1
    conv_data[conv_count, j] = conv_notes_equal == 1; j += 1
    conv_data[conv_count, j] = conv_notes_equal == 2; j += 1
    conv_data[conv_count, j] = conv_notes_equal == 3; j += 1

    conv_data[conv_count, j] = num_complete == 0; j += 1
    conv_data[conv_count, j] = num_complete == 1; j += 1
    conv_data[conv_count, j] = num_complete == 2; j += 1
    conv_data[conv_count, j] = num_complete == 3; j += 1
    conv_data[conv_count, j] = num_complete == 4; j += 1
    conv_data[conv_count, j] = num_complete == 5; j += 1

    conv_data[conv_count, j] = num_partial == 0; j += 1
    conv_data[conv_count, j] = num_partial == 1; j += 1
    conv_data[conv_count, j] = num_partial == 2; j += 1
    conv_data[conv_count, j] = num_partial == 3; j += 1
    conv_data[conv_count, j] = num_partial == 4; j += 1
    conv_data[conv_count, j] = num_partial == 5; j += 1
    
    conv_data[conv_count, j] = all(
      voices[i].note.chord_index == voices[i+1].note.chord_index
      for i in range(len(voices) - 1)
    ); j += 1

    conv_data[conv_count, j] = div_note is not None; j += 1
    conv_data[conv_count, j] = top_div_note is not None; j += 1
    conv_data[conv_count, j] = bottom_div_note is not None; j += 1

    # Note features
    conv_data[conv_count, j:] = all_note_data[<int> note.index, :]

    conv_count += 1

  if conv_count > 0:
    assert conv_count <= PAD, conv_count
    assert j == COUNT, j

    for i in range(conv_count, PAD):
      conv_data[i, :] = conv_data[i - 1, :]

  else:
    conv_data[...] = 0
    for i in range(PAD):
      conv_data[i, 0] = 1
