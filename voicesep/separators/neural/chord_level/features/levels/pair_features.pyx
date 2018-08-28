#cython: language_level=3
import cython
import voicesep.utils.constants as const

cdef int COUNT = 203
cdef int PAD = 15
# Make sure your order of operations is correct (x - y) / 20

@cython.boundscheck(False)
@cython.wraparound(False)
cdef create(float[:,:,::1] all_pair_data, chord, list active_subset):
  cdef int chord_len = len(chord)
  cdef int len_all_pair_data_chord = len(all_pair_data)
  cdef int len_active_subset = len(active_subset)
  cdef int len_all_pair_data_subset = len(all_pair_data[0, :])
  cdef int len_all_pair_data_count = len(all_pair_data[0, 0, :])

  assert len_all_pair_data_chord == chord_len
  assert len_all_pair_data_subset == len_active_subset + 1
  assert len_all_pair_data_count == COUNT

  cdef int i, j, k = 0
  cdef int len_right = 0
  cdef int len_conv_notes = 0

  # Average, max, min,  inter-onset offset
  # Consecutive rest repeat count
  # Consecutive duration repeats

  for i, note in enumerate(chord):
    for j, voice in enumerate(active_subset):
      len_right = len(voice.right)
      len_conv_notes = len(voice.conv_notes)

      k = 0

      all_pair_data[i, j, k] = 0; k += 1

      all_pair_data[i, j, k] = abs(float(note.pitch_space - voice.note.pitch_space)) / const.MAX_PITCH_DISTANCE; k += 1
      all_pair_data[i, j, k] = note.pitch_space == voice.note.pitch_space; k += 1
      all_pair_data[i, j, k] = note.pitch_space > voice.note.pitch_space; k += 1
      all_pair_data[i, j, k] = note.pitch_space < voice.note.pitch_space; k += 1

      all_pair_data[i, j, k] = abs(float(note.pitch_space - voice.avg_pitch_space)) / const.MAX_PITCH_DISTANCE; k += 1
      all_pair_data[i, j, k] = note.pitch_space == voice.avg_pitch_space; k += 1
      all_pair_data[i, j, k] = note.pitch_space > voice.avg_pitch_space; k += 1
      all_pair_data[i, j, k] = note.pitch_space < voice.avg_pitch_space; k += 1

      all_pair_data[i, j, k] = abs(float(note.pitch_space - voice.max_pitch_space)) / const.MAX_PITCH_DISTANCE; k += 1
      all_pair_data[i, j, k] = note.pitch_space == voice.max_pitch_space; k += 1
      all_pair_data[i, j, k] = note.pitch_space > voice.max_pitch_space; k += 1
      all_pair_data[i, j, k] = note.pitch_space < voice.max_pitch_space; k += 1

      all_pair_data[i, j, k] = abs(float(note.pitch_space - voice.min_pitch_space)) / const.MAX_PITCH_DISTANCE; k += 1
      all_pair_data[i, j, k] = note.pitch_space == voice.min_pitch_space; k += 1
      all_pair_data[i, j, k] = note.pitch_space > voice.min_pitch_space; k += 1
      all_pair_data[i, j, k] = note.pitch_space < voice.min_pitch_space; k += 1

      all_pair_data[i, j, k] = abs(
        voice.std_pitch_space - 
        abs(note.pitch_space - voice.avg_pitch_space)
      ) / const.MAX_PITCH_DISTANCE; k += 1
      all_pair_data[i, j, k] = abs(note.pitch_space - voice.avg_pitch_space) < voice.std_pitch_space; k += 1

      all_pair_data[i, j, k] = 1 if note.note_above is None else abs(
        note.note_above.pitch_space - voice.note.pitch_space
      ) / const.MAX_PITCH_DISTANCE; k += 1

      all_pair_data[i, j, k] = 1 if note.note_below is None else abs(
        note.note_below.pitch_space - voice.note.pitch_space
      ) / const.MAX_PITCH_DISTANCE; k += 1

      # Note in voice
      all_pair_data[i, j, k] = 1 if voice.note.note_above is None else abs(
        voice.note.note_above.pitch_space - note.pitch_space
      ) / const.MAX_PITCH_DISTANCE; k += 1

      all_pair_data[i, j, k] = 1 if voice.note.note_below is None else abs(
        voice.note.note_below.pitch_space - note.pitch_space
      ) / const.MAX_PITCH_DISTANCE; k += 1

      # Last above and below
      all_pair_data[i, j, k] = 1 if voice.last_above is None else abs(
        voice.last_above.pitch_space - note.pitch_space
      ) / const.MAX_PITCH_DISTANCE; k += 1

      all_pair_data[i, j, k] = 1 if voice.last_below is None else abs(
        voice.last_below.pitch_space - note.pitch_space
      ) / const.MAX_PITCH_DISTANCE; k += 1

      # Subset above and below
      all_pair_data[i, j, k] = 1 if voice.voice_above is None else abs(
        voice.voice_above.pitch_space - note.pitch_space
      ) / const.MAX_PITCH_DISTANCE; k += 1

      all_pair_data[i, j, k] = 1 if voice.voice_below is None else abs(
        voice.voice_below.pitch_space - note.pitch_space
      ) / const.MAX_PITCH_DISTANCE; k += 1

      # Consecutive repeats
      all_pair_data[i, j, k] = note.pitch_space != voice.note.pitch_space; k += 1
      all_pair_data[i, j, k] = note.pitch_space == voice.note.pitch_space and voice.cons_repeat == 0; k += 1
      all_pair_data[i, j, k] = note.pitch_space == voice.note.pitch_space and voice.cons_repeat == 1; k += 1
      all_pair_data[i, j, k] = note.pitch_space == voice.note.pitch_space and voice.cons_repeat == 2; k += 1
      all_pair_data[i, j, k] = note.pitch_space == voice.note.pitch_space and voice.cons_repeat == 3; k += 1
      all_pair_data[i, j, k] = note.pitch_space == voice.note.pitch_space and voice.cons_repeat > 3; k += 1

      # Shared div note
      # Voice above and below
      voice_above_divs = [] if voice.voice_above is None else list(set(voice.voice_above.div_notes) & set(voice.div_notes))
      voice_above_divs.sort(key=lambda v : v.beat_onset)
      voice_above_div = None if len(voice_above_divs) == 0 else voice_above_divs[len(voice_above_divs)-1]
      all_pair_data[i, j, k] = voice_above_div is not None; k += 1
      all_pair_data[i, j, k] = 1 if voice_above_div is None else abs(voice_above_div.pitch_space - note.pitch_space) / const.MAX_PITCH_DISTANCE; k += 1
      all_pair_data[i, j, k] = 0 if voice_above_div is None else voice_above_div.pitch_space > note.pitch_space; k += 1
      all_pair_data[i, j, k] = 0 if voice_above_div is None else voice_above_div.pitch_space < note.pitch_space; k += 1
      all_pair_data[i, j, k] = 0 if voice_above_div is None else voice_above_div.pitch_space == note.pitch_space; k += 1

      voice_below_divs = [] if voice.voice_below is None else list(set(voice.voice_below.div_notes) & set(voice.div_notes))
      voice_below_divs.sort(key=lambda v : v.beat_onset)
      voice_below_div = None if len(voice_below_divs) == 0 else voice_below_divs[len(voice_below_divs)-1]
      all_pair_data[i, j, k] = voice_below_div is not None; k += 1
      all_pair_data[i, j, k] = 1 if voice_below_div is None else abs(voice_below_div.pitch_space - note.pitch_space) / const.MAX_PITCH_DISTANCE; k += 1
      all_pair_data[i, j, k] = 0 if voice_below_div is None else voice_below_div.pitch_space > note.pitch_space; k += 1
      all_pair_data[i, j, k] = 0 if voice_below_div is None else voice_below_div.pitch_space < note.pitch_space; k += 1
      all_pair_data[i, j, k] = 0 if voice_below_div is None else voice_below_div.pitch_space == note.pitch_space; k += 1

      # Last above and below
      last_above_divs = [] if voice.last_above is None else list(set(voice.last_above.div_notes) & set(voice.div_notes))
      last_above_divs.sort(key=lambda v : v.beat_onset)
      last_above_div = None if len(last_above_divs) == 0 else last_above_divs[len(last_above_divs)-1]
      all_pair_data[i, j, k] = last_above_div is not None; k += 1
      all_pair_data[i, j, k] = 1 if last_above_div is None else abs(last_above_div.pitch_space - note.pitch_space) / const.MAX_PITCH_DISTANCE; k += 1
      all_pair_data[i, j, k] = 0 if last_above_div is None else last_above_div.pitch_space > note.pitch_space; k += 1
      all_pair_data[i, j, k] = 0 if last_above_div is None else last_above_div.pitch_space < note.pitch_space; k += 1
      all_pair_data[i, j, k] = 0 if last_above_div is None else last_above_div.pitch_space == note.pitch_space; k += 1

      last_below_divs = [] if voice.last_below is None else list(set(voice.last_below.div_notes) & set(voice.div_notes))
      last_below_divs.sort(key=lambda v : v.beat_onset)
      last_below_div = None if len(last_below_divs) == 0 else last_below_divs[len(last_below_divs)-1]
      all_pair_data[i, j, k] = last_below_div is not None; k += 1
      all_pair_data[i, j, k] = 1 if last_below_div is None else abs(last_below_div.pitch_space - note.pitch_space) / const.MAX_PITCH_DISTANCE; k += 1
      all_pair_data[i, j, k] = 0 if last_below_div is None else last_below_div.pitch_space > note.pitch_space; k += 1
      all_pair_data[i, j, k] = 0 if last_below_div is None else last_below_div.pitch_space < note.pitch_space; k += 1
      all_pair_data[i, j, k] = 0 if last_below_div is None else last_below_div.pitch_space == note.pitch_space; k += 1

      # nv above and below
      nv_above_divs = [] if voice.nv_above is None else list(set(voice.nv_above.div_notes) & set(voice.div_notes))
      nv_above_divs.sort(key=lambda v : v.beat_onset)
      nv_above_div = None if len(nv_above_divs) == 0 else nv_above_divs[len(nv_above_divs)-1]
      all_pair_data[i, j, k] = nv_above_div is not None; k += 1
      all_pair_data[i, j, k] = 1 if nv_above_div is None else abs(nv_above_div.pitch_space - note.pitch_space) / const.MAX_PITCH_DISTANCE; k += 1
      all_pair_data[i, j, k] = 0 if nv_above_div is None else nv_above_div.pitch_space > note.pitch_space; k += 1
      all_pair_data[i, j, k] = 0 if nv_above_div is None else nv_above_div.pitch_space < note.pitch_space; k += 1
      all_pair_data[i, j, k] = 0 if nv_above_div is None else nv_above_div.pitch_space == note.pitch_space; k += 1

      nv_below_divs = [] if voice.nv_below is None else list(set(voice.nv_below.div_notes) & set(voice.div_notes))
      nv_below_divs.sort(key=lambda v : v.beat_onset)
      nv_below_div = None if len(nv_below_divs) == 0 else nv_below_divs[len(nv_below_divs)-1]
      all_pair_data[i, j, k] = nv_below_div is not None; k += 1
      all_pair_data[i, j, k] = 1 if nv_below_div is None else abs(nv_below_div.pitch_space - note.pitch_space) / const.MAX_PITCH_DISTANCE; k += 1
      all_pair_data[i, j, k] = 0 if nv_below_div is None else nv_below_div.pitch_space > note.pitch_space; k += 1
      all_pair_data[i, j, k] = 0 if nv_below_div is None else nv_below_div.pitch_space < note.pitch_space; k += 1
      all_pair_data[i, j, k] = 0 if nv_below_div is None else nv_below_div.pitch_space == note.pitch_space; k += 1

      # Conv notes
      all_pair_data[i, j, k] = len(voice.conv_notes) > 0; k += 1

      all_pair_data[i, j, k] = abs(voice.conv_notes[0].pitch_space - note.note_above.pitch_space) / const.MAX_PITCH_DISTANCE if len(voice.conv_notes) > 0 and note.note_above is not None else 1; k += 1
      all_pair_data[i, j, k] = voice.conv_notes[0].pitch_space > note.note_above.pitch_space if len(voice.conv_notes) > 0 and note.note_above is not None else 0; k += 1
      all_pair_data[i, j, k] = voice.conv_notes[0].pitch_space < note.note_above.pitch_space if len(voice.conv_notes) > 0 and note.note_above is not None else 0; k += 1
      all_pair_data[i, j, k] = voice.conv_notes[0].pitch_space == note.note_above.pitch_space if len(voice.conv_notes) > 0 and note.note_above is not None else 0; k += 1

      all_pair_data[i, j, k] = abs(voice.conv_notes[0].pitch_space - note.pitch_space) / const.MAX_PITCH_DISTANCE if len(voice.conv_notes) > 0 else 1; k += 1
      all_pair_data[i, j, k] = voice.conv_notes[0].pitch_space > note.pitch_space if len(voice.conv_notes) > 0 else 0; k += 1
      all_pair_data[i, j, k] = voice.conv_notes[0].pitch_space < note.pitch_space if len(voice.conv_notes) > 0 else 0; k += 1
      all_pair_data[i, j, k] = voice.conv_notes[0].pitch_space == note.pitch_space if len(voice.conv_notes) > 0 else 0; k += 1

      all_pair_data[i, j, k] = abs(voice.conv_notes[0].pitch_space - note.note_below.pitch_space) / const.MAX_PITCH_DISTANCE if len(voice.conv_notes) > 0 and note.note_below is not None else 1; k += 1
      all_pair_data[i, j, k] = voice.conv_notes[0].pitch_space > note.note_below.pitch_space if len(voice.conv_notes) > 0 and note.note_below is not None else 0; k += 1
      all_pair_data[i, j, k] = voice.conv_notes[0].pitch_space < note.note_below.pitch_space if len(voice.conv_notes) > 0 and note.note_below is not None else 0; k += 1
      all_pair_data[i, j, k] = voice.conv_notes[0].pitch_space == note.note_below.pitch_space if len(voice.conv_notes) > 0 and note.note_below is not None else 0; k += 1

      all_pair_data[i, j, k] = abs(voice.conv_notes[0].pitch_space - voice.right[0].pitch_space) / const.MAX_PITCH_DISTANCE if len(voice.conv_notes) > 0 and len(voice.right) > 0 else 1; k += 1
      all_pair_data[i, j, k] = voice.conv_notes[0].pitch_space > voice.right[0].pitch_space if len(voice.conv_notes) > 0 and len(voice.right) > 0 else 0; k += 1
      all_pair_data[i, j, k] = voice.conv_notes[0].pitch_space < voice.right[0].pitch_space if len(voice.conv_notes) > 0 and len(voice.right) > 0 else 0; k += 1
      all_pair_data[i, j, k] = voice.conv_notes[0].pitch_space == voice.right[0].pitch_space if len(voice.conv_notes) > 0 and len(voice.right) > 0 else 0; k += 1

      all_pair_data[i, j, k] = abs(voice.conv_notes[0].pitch_space - voice.right[len_right-1].pitch_space) / const.MAX_PITCH_DISTANCE if len(voice.conv_notes) > 0 and len(voice.right) > 0 else 1; k += 1
      all_pair_data[i, j, k] = voice.conv_notes[0].pitch_space > voice.right[len_right-1].pitch_space if len(voice.conv_notes) > 0 and len(voice.right) > 0 else 0; k += 1
      all_pair_data[i, j, k] = voice.conv_notes[0].pitch_space < voice.right[len_right-1].pitch_space if len(voice.conv_notes) > 0 and len(voice.right) > 0 else 0; k += 1
      all_pair_data[i, j, k] = voice.conv_notes[0].pitch_space == voice.right[len_right-1].pitch_space if len(voice.conv_notes) > 0 and len(voice.right) > 0 else 0; k += 1

      all_pair_data[i, j, k] = abs(voice.conv_notes[len_conv_notes-1].pitch_space - note.note_above.pitch_space) / const.MAX_PITCH_DISTANCE if len(voice.conv_notes) > 0 and note.note_above is not None else 1; k += 1
      all_pair_data[i, j, k] = voice.conv_notes[len_conv_notes-1].pitch_space > note.note_above.pitch_space if len(voice.conv_notes) > 0 and note.note_above is not None else 0; k += 1
      all_pair_data[i, j, k] = voice.conv_notes[len_conv_notes-1].pitch_space < note.note_above.pitch_space if len(voice.conv_notes) > 0 and note.note_above is not None else 0; k += 1
      all_pair_data[i, j, k] = voice.conv_notes[len_conv_notes-1].pitch_space == note.note_above.pitch_space if len(voice.conv_notes) > 0 and note.note_above is not None else 0; k += 1

      all_pair_data[i, j, k] = abs(voice.conv_notes[len_conv_notes-1].pitch_space - note.pitch_space) / const.MAX_PITCH_DISTANCE if len(voice.conv_notes) > 0 else 1; k += 1
      all_pair_data[i, j, k] = voice.conv_notes[len_conv_notes-1].pitch_space > note.pitch_space if len(voice.conv_notes) > 0 else 0; k += 1
      all_pair_data[i, j, k] = voice.conv_notes[len_conv_notes-1].pitch_space < note.pitch_space if len(voice.conv_notes) > 0 else 0; k += 1
      all_pair_data[i, j, k] = voice.conv_notes[len_conv_notes-1].pitch_space == note.pitch_space if len(voice.conv_notes) > 0 else 0; k += 1

      all_pair_data[i, j, k] = abs(voice.conv_notes[len_conv_notes-1].pitch_space - note.note_below.pitch_space) / const.MAX_PITCH_DISTANCE if len(voice.conv_notes) > 0 and note.note_below is not None else 1; k += 1
      all_pair_data[i, j, k] = voice.conv_notes[len_conv_notes-1].pitch_space > note.note_below.pitch_space if len(voice.conv_notes) > 0 and note.note_below is not None else 0; k += 1
      all_pair_data[i, j, k] = voice.conv_notes[len_conv_notes-1].pitch_space < note.note_below.pitch_space if len(voice.conv_notes) > 0 and note.note_below is not None else 0; k += 1
      all_pair_data[i, j, k] = voice.conv_notes[len_conv_notes-1].pitch_space == note.note_below.pitch_space if len(voice.conv_notes) > 0 and note.note_below is not None else 0; k += 1

      all_pair_data[i, j, k] = abs(voice.conv_notes[len_conv_notes-1].pitch_space - voice.right[0].pitch_space) / const.MAX_PITCH_DISTANCE if len(voice.conv_notes) > 0 and len(voice.right) > 0 else 1; k += 1
      all_pair_data[i, j, k] = voice.conv_notes[len_conv_notes-1].pitch_space > voice.right[0].pitch_space if len(voice.conv_notes) > 0 and len(voice.right) > 0 else 0; k += 1
      all_pair_data[i, j, k] = voice.conv_notes[len_conv_notes-1].pitch_space < voice.right[0].pitch_space if len(voice.conv_notes) > 0 and len(voice.right) > 0 else 0; k += 1
      all_pair_data[i, j, k] = voice.conv_notes[len_conv_notes-1].pitch_space == voice.right[0].pitch_space if len(voice.conv_notes) > 0 and len(voice.right) > 0 else 0; k += 1

      all_pair_data[i, j, k] = abs(voice.conv_notes[len_conv_notes-1].pitch_space - voice.right[len_right-1].pitch_space) / const.MAX_PITCH_DISTANCE if len(voice.conv_notes) > 0 and len(voice.right) > 0 else 1; k += 1
      all_pair_data[i, j, k] = voice.conv_notes[len_conv_notes-1].pitch_space > voice.right[len_right-1].pitch_space if len(voice.conv_notes) > 0 and len(voice.right) > 0 else 0; k += 1
      all_pair_data[i, j, k] = voice.conv_notes[len_conv_notes-1].pitch_space < voice.right[len_right-1].pitch_space if len(voice.conv_notes) > 0 and len(voice.right) > 0 else 0; k += 1
      all_pair_data[i, j, k] = voice.conv_notes[len_conv_notes-1].pitch_space == voice.right[len_right-1].pitch_space if len(voice.conv_notes) > 0 and len(voice.right) > 0 else 0; k += 1

      # Temporal
      all_pair_data[i, j, k] = float(note.beat_onset - voice.note.beat_onset) / const.MAX_BEAT_ONSET_DISTANCE; k += 1
      all_pair_data[i, j, k] = max(0, float(note.beat_onset - voice.beat_offset)) / const.MAX_BEAT_ONSET_DISTANCE; k += 1
      all_pair_data[i, j, k] = note.beat_onset == voice.note.beat_offset; k += 1
      all_pair_data[i, j, k] = note.beat_onset > voice.note.beat_offset; k += 1
      all_pair_data[i, j, k] = note.beat_onset < voice.note.beat_offset; k += 1

      all_pair_data[i, j, k] = float(note.beat_onset - voice.voice_above.note.beat_onset) / const.MAX_BEAT_ONSET_DISTANCE if voice.voice_above is not None else 1; k += 1
      all_pair_data[i, j, k] = max(0, float(note.beat_onset - voice.voice_above.beat_offset)) / const.MAX_BEAT_ONSET_OFFSET if voice.voice_above is not None else 1; k += 1
      all_pair_data[i, j, k] = note.beat_onset == voice.voice_above.note.beat_offset if voice.voice_above is not None else 0; k += 1
      all_pair_data[i, j, k] = note.beat_onset > voice.voice_above.note.beat_offset if voice.voice_above is not None else 0; k += 1
      all_pair_data[i, j, k] = note.beat_onset < voice.voice_above.note.beat_offset if voice.voice_above is not None else 0; k += 1

      all_pair_data[i, j, k] = float(note.beat_onset - voice.voice_below.note.beat_onset) / const.MAX_BEAT_ONSET_DISTANCE if voice.voice_below is not None else 1; k += 1
      all_pair_data[i, j, k] = max(0, float(note.beat_onset - voice.voice_below.beat_offset)) / const.MAX_BEAT_ONSET_OFFSET if voice.voice_below is not None else 1; k += 1
      all_pair_data[i, j, k] = note.beat_onset == voice.voice_below.note.beat_offset if voice.voice_below is not None else 0; k += 1
      all_pair_data[i, j, k] = note.beat_onset > voice.voice_below.note.beat_offset if voice.voice_below is not None else 0; k += 1
      all_pair_data[i, j, k] = note.beat_onset < voice.voice_below.note.beat_offset if voice.voice_below is not None else 0; k += 1

      all_pair_data[i, j, k] = float(note.beat_onset - voice.last_above.note.beat_onset) / const.MAX_BEAT_ONSET_DISTANCE if voice.last_above is not None else 1; k += 1
      all_pair_data[i, j, k] = max(0, float(note.beat_onset - voice.last_above.beat_offset)) / const.MAX_BEAT_ONSET_OFFSET if voice.last_above is not None else 1; k += 1
      all_pair_data[i, j, k] = note.beat_onset == voice.last_above.note.beat_offset if voice.last_above is not None else 0; k += 1
      all_pair_data[i, j, k] = note.beat_onset > voice.last_above.note.beat_offset if voice.last_above is not None else 0; k += 1
      all_pair_data[i, j, k] = note.beat_onset < voice.last_above.note.beat_offset if voice.last_above is not None else 0; k += 1

      all_pair_data[i, j, k] = float(note.beat_onset - voice.last_below.note.beat_onset) / const.MAX_BEAT_ONSET_DISTANCE if voice.last_below is not None else 1; k += 1
      all_pair_data[i, j, k] = max(0, float(note.beat_onset - voice.last_below.beat_offset)) / const.MAX_BEAT_ONSET_OFFSET if voice.last_below is not None else 1; k += 1
      all_pair_data[i, j, k] = note.beat_onset == voice.last_below.note.beat_offset if voice.last_below is not None else 0; k += 1
      all_pair_data[i, j, k] = note.beat_onset > voice.last_below.note.beat_offset if voice.last_below is not None else 0; k += 1
      all_pair_data[i, j, k] = note.beat_onset < voice.last_below.note.beat_offset if voice.last_below is not None else 0; k += 1

      all_pair_data[i, j, k] = abs(float(note.beat_duration - voice.note.beat_duration)) / const.MAX_BEAT_DUR_DISTANCE; k += 1
      all_pair_data[i, j, k] = note.beat_onset == voice.note.beat_duration; k += 1
      all_pair_data[i, j, k] = note.beat_onset > voice.note.beat_duration; k += 1
      all_pair_data[i, j, k] = note.beat_onset < voice.note.beat_duration; k += 1

      all_pair_data[i, j, k] = abs(float(note.beat_duration - voice.voice_above.note.beat_duration)) / const.MAX_BEAT_DUR_DISTANCE if voice.voice_above is not None else 1; k += 1
      all_pair_data[i, j, k] = note.beat_duration == voice.voice_above.note.beat_duration if voice.voice_above is not None else 0; k += 1
      all_pair_data[i, j, k] = note.beat_duration > voice.voice_above.note.beat_duration if voice.voice_above is not None else 0; k += 1
      all_pair_data[i, j, k] = note.beat_duration < voice.voice_above.note.beat_duration if voice.voice_above is not None else 0; k += 1

      all_pair_data[i, j, k] = abs(float(note.beat_duration - voice.voice_below.note.beat_duration)) / const.MAX_BEAT_DUR_DISTANCE if voice.voice_below is not None else 1; k += 1
      all_pair_data[i, j, k] = note.beat_duration == voice.voice_below.note.beat_duration if voice.voice_below is not None else 0; k += 1
      all_pair_data[i, j, k] = note.beat_duration > voice.voice_below.note.beat_duration if voice.voice_below is not None else 0; k += 1
      all_pair_data[i, j, k] = note.beat_duration < voice.voice_below.note.beat_duration if voice.voice_below is not None else 0; k += 1

      all_pair_data[i, j, k] = abs(float(note.beat_duration - voice.last_above.note.beat_duration)) / const.MAX_BEAT_DUR_DISTANCE if voice.last_above is not None else 1; k += 1
      all_pair_data[i, j, k] = note.beat_duration == voice.last_above.note.beat_duration if voice.last_above is not None else 0; k += 1
      all_pair_data[i, j, k] = note.beat_duration > voice.last_above.note.beat_duration if voice.last_above is not None else 0; k += 1
      all_pair_data[i, j, k] = note.beat_duration < voice.last_above.note.beat_duration if voice.last_above is not None else 0; k += 1

      all_pair_data[i, j, k] = abs(float(note.beat_duration - voice.last_below.note.beat_duration)) / const.MAX_BEAT_DUR_DISTANCE if voice.last_below is not None else 1; k += 1
      all_pair_data[i, j, k] = note.beat_duration == voice.last_below.note.beat_duration if voice.last_below is not None else 0; k += 1
      all_pair_data[i, j, k] = note.beat_duration > voice.last_below.note.beat_duration if voice.last_below is not None else 0; k += 1
      all_pair_data[i, j, k] = note.beat_duration < voice.last_below.note.beat_duration if voice.last_below is not None else 0; k += 1

      # Positional
      all_pair_data[i, j, k] = float(note.chord_index - voice.note.chord_index) / const.MAX_ONSET_DISTANCE; k += 1

      all_pair_data[i, j, k] = abs(float(note.index - voice.last_index)) / const.MAX_INDEX_DISTANCE; k += 1
      all_pair_data[i, j, k] = note.index == voice.last_index; k += 1
      all_pair_data[i, j, k] = note.index == voice.last_index + 1; k += 1
      all_pair_data[i, j, k] = note.index == voice.last_index - 1; k += 1
      all_pair_data[i, j, k] = note.index > voice.last_index + 1; k += 1
      all_pair_data[i, j, k] = note.index < voice.last_index - 1; k += 1

      all_pair_data[i, j, k] = abs(float(note.index - voice.subset_index)) / const.MAX_INDEX_DISTANCE; k += 1
      all_pair_data[i, j, k] = note.index == voice.subset_index; k += 1
      all_pair_data[i, j, k] = note.index == voice.subset_index + 1; k += 1
      all_pair_data[i, j, k] = note.index == voice.subset_index - 1; k += 1
      all_pair_data[i, j, k] = note.index > voice.subset_index + 1; k += 1
      all_pair_data[i, j, k] = note.index < voice.subset_index - 1; k += 1

      all_pair_data[i, j, k] = abs(float(note.index - voice.note.index)) / const.MAX_INDEX_DISTANCE; k += 1
      all_pair_data[i, j, k] = note.index == voice.note.index; k += 1
      all_pair_data[i, j, k] = note.index == voice.note.index + 1; k += 1
      all_pair_data[i, j, k] = note.index == voice.note.index - 1; k += 1
      all_pair_data[i, j, k] = note.index > voice.note.index + 1; k += 1
      all_pair_data[i, j, k] = note.index < voice.note.index - 1; k += 1

      all_pair_data[i, j, k] = abs(float(note.chord_length - voice.last_length)) / const.MAX_LENGTH_DISTANCE; k += 1
      all_pair_data[i, j, k] = note.chord_length == voice.last_length; k += 1
      all_pair_data[i, j, k] = note.chord_length == voice.last_length + 1; k += 1
      all_pair_data[i, j, k] = note.chord_length == voice.last_length - 1; k += 1
      all_pair_data[i, j, k] = note.chord_length > voice.last_length + 1; k += 1
      all_pair_data[i, j, k] = note.chord_length < voice.last_length - 1; k += 1

      all_pair_data[i, j, k] = abs(float(note.chord_length - voice.subset_length)) / const.MAX_LENGTH_DISTANCE; k += 1
      all_pair_data[i, j, k] = note.chord_length == voice.subset_length; k += 1
      all_pair_data[i, j, k] = note.chord_length == voice.subset_length + 1; k += 1
      all_pair_data[i, j, k] = note.chord_length == voice.subset_length - 1; k += 1
      all_pair_data[i, j, k] = note.chord_length > voice.subset_length + 1; k += 1
      all_pair_data[i, j, k] = note.chord_length < voice.subset_length - 1; k += 1

      all_pair_data[i, j, k] = abs(float(note.chord_length - voice.note.chord_length)) / const.MAX_LENGTH_DISTANCE; k += 1
      all_pair_data[i, j, k] = note.chord_length == voice.note.chord_length; k += 1
      all_pair_data[i, j, k] = note.chord_length == voice.note.chord_length + 1; k += 1
      all_pair_data[i, j, k] = note.chord_length == voice.note.chord_length - 1; k += 1
      all_pair_data[i, j, k] = note.chord_length > voice.note.chord_length + 1; k += 1
      all_pair_data[i, j, k] = note.chord_length < voice.note.chord_length - 1; k += 1

      all_pair_data[i, j, k] = abs(float(note.degree - voice.note.degree)) / const.MAX_DEGREE_DISTANCE; k += 1
      all_pair_data[i, j, k] = note.degree > voice.note.degree; k += 1
      all_pair_data[i, j, k] = note.degree < voice.note.degree; k += 1
      all_pair_data[i, j, k] = note.degree == voice.note.degree; k += 1

      all_pair_data[i, j, k] = abs(float(note.chord_step - voice.note.chord_step)) / const.MAX_DEGREE_DISTANCE; k += 1
      all_pair_data[i, j, k] = note.chord_step > voice.note.chord_step; k += 1
      all_pair_data[i, j, k] = note.chord_step < voice.note.chord_step; k += 1
      all_pair_data[i, j, k] = note.chord_step == voice.note.chord_step; k += 1

      all_pair_data[i, j, k] = abs(float(note.beat_strength - voice.note.beat_strength)); k += 1
      all_pair_data[i, j, k] = note.beat_strength > voice.note.beat_strength; k += 1
      all_pair_data[i, j, k] = note.beat_strength < voice.note.beat_strength; k += 1
      all_pair_data[i, j, k] = note.beat_strength == voice.note.beat_strength; k += 1

      # Pseudo-polyphony
      all_pair_data[i, j, k] = note.repeat_count <= 4 and voice.note.repeat_count <= 4; k += 1
      all_pair_data[i, j, k] = note.repeat_count <= 4 and voice.note.repeat_count > 4; k += 1

      all_pair_data[i, j, k] = note.repeat_count > 4 and voice.note.repeat_count <= 4; k += 1
      all_pair_data[i, j, k] = note.repeat_count > 4 and voice.note.repeat_count > 4 and note.repeat_behind is voice.note; k += 1
      all_pair_data[i, j, k] = note.repeat_count > 4 and voice.note.repeat_count > 4 and note.repeat_behind is not voice.note; k += 1
      # all_pair_data[i, j, k] = len(note.poly_pairs.left) > 0; k += 1
      # all_pair_data[i, j, k] = len(note.poly_pairs.left[0].poly_pairs.left) > 0 if len(note.poly_pairs.left) > 0 else False; k += 1
      #
      # # all_pair_data[i, j, k] = (note.poly_left.pitch_space > note.pitch_space) if note.poly_left is not None else False; k += 1
      # if len(note.poly_pairs.left) > 0:
      #   all_pair_data[i, j, k] = note.poly_pairs.left[0].pitch_space > note.pitch_space; k += 1
      #   all_pair_data[i, j, k] = note.poly_pairs.left[0].pitch_space < note.pitch_space; k += 1
      #   all_pair_data[i, j, k] = note.poly_pairs.left[0].pitch_space == note.pitch_space; k += 1
      # else:
      #   all_pair_data[i, j, k] = False; k += 1
      #   all_pair_data[i, j, k] = False; k += 1
      #   all_pair_data[i, j, k] = False; k += 1
      #
      # all_pair_data[i, j, k] = note.poly_left_count == 0; k += 1
      # all_pair_data[i, j, k] = note.poly_left_count == 1; k += 1
      # all_pair_data[i, j, k] = note.poly_left_count == 2; k += 1
      # all_pair_data[i, j, k] = note.poly_left_count == 3; k += 1
      # all_pair_data[i, j, k] = note.poly_left_count == 4; k += 1
      # all_pair_data[i, j, k] = note.poly_left_count == 5; k += 1
      # all_pair_data[i, j, k] = note.poly_left_count > 5; k += 1
      #
      # all_pair_data[i, j, k] = note.poly_right_count == 0; k += 1
      # all_pair_data[i, j, k] = note.poly_right_count == 1; k += 1
      # all_pair_data[i, j, k] = note.poly_right_count == 2; k += 1
      # all_pair_data[i, j, k] = note.poly_right_count == 3; k += 1
      # all_pair_data[i, j, k] = note.poly_right_count == 4; k += 1
      # all_pair_data[i, j, k] = note.poly_right_count == 5; k += 1
      # all_pair_data[i, j, k] = note.poly_right_count > 5; k += 1
      #
      # all_pair_data[i, j, k] = (note.poly_left_count + note.poly_right_count) == 5; k += 1
      # all_pair_data[i, j, k] = (note.poly_left_count + note.poly_right_count) == 6; k += 1
      # all_pair_data[i, j, k] = (note.poly_left_count + note.poly_right_count) == 7; k += 1
      # all_pair_data[i, j, k] = (note.poly_left_count + note.poly_right_count) == 8; k += 1
      # all_pair_data[i, j, k] = (note.poly_left_count + note.poly_right_count) > 8; k += 1
      #
      # all_pair_data[i, j, k] = note.poly_repeat_left == 0; k += 1
      # all_pair_data[i, j, k] = note.poly_repeat_left == 1; k += 1
      # all_pair_data[i, j, k] = note.poly_repeat_left == 2; k += 1
      # all_pair_data[i, j, k] = note.poly_repeat_left > 2; k += 1
      #
      # all_pair_data[i, j, k] = note.poly_repeat_right == 0; k += 1
      # all_pair_data[i, j, k] = note.poly_repeat_right == 1; k += 1
      # all_pair_data[i, j, k] = note.poly_repeat_right == 2; k += 1
      # all_pair_data[i, j, k] = note.poly_repeat_right > 2; k += 1
      #
      # all_pair_data[i, j, k] = (note.poly_repeat_left + note.poly_repeat_right) == 0; k += 1
      # all_pair_data[i, j, k] = (note.poly_repeat_left + note.poly_repeat_right) == 1; k += 1
      # all_pair_data[i, j, k] = (note.poly_repeat_left + note.poly_repeat_right) == 2; k += 1
      # all_pair_data[i, j, k] = (note.poly_repeat_left + note.poly_repeat_right) == 3; k += 1
      # all_pair_data[i, j, k] = (note.poly_repeat_left + note.poly_repeat_right) == 4; k += 1
      # all_pair_data[i, j, k] = (note.poly_repeat_left + note.poly_repeat_right) == 5; k += 1
      # all_pair_data[i, j, k] = (note.poly_repeat_left + note.poly_repeat_right) > 5; k += 1
      #
      # all_pair_data[i, j, k] = voice.note.poly_repeat_left == 0; k += 1
      # all_pair_data[i, j, k] = voice.note.poly_repeat_left == 1; k += 1
      # all_pair_data[i, j, k] = voice.note.poly_repeat_left == 2; k += 1
      # all_pair_data[i, j, k] = voice.note.poly_repeat_left > 2; k += 1
      #
      # all_pair_data[i, j, k] = voice.note.poly_repeat_right == 0; k += 1
      # all_pair_data[i, j, k] = voice.note.poly_repeat_right == 1; k += 1
      # all_pair_data[i, j, k] = voice.note.poly_repeat_right == 2; k += 1
      # all_pair_data[i, j, k] = voice.note.poly_repeat_right > 2; k += 1
      #
      # all_pair_data[i, j, k] = (voice.note.poly_repeat_left + voice.note.poly_repeat_right) == 0; k += 1
      # all_pair_data[i, j, k] = (voice.note.poly_repeat_left + voice.note.poly_repeat_right) == 1; k += 1
      # all_pair_data[i, j, k] = (voice.note.poly_repeat_left + voice.note.poly_repeat_right) == 2; k += 1
      # all_pair_data[i, j, k] = (voice.note.poly_repeat_left + voice.note.poly_repeat_right) == 3; k += 1
      # all_pair_data[i, j, k] = (voice.note.poly_repeat_left + voice.note.poly_repeat_right) == 4; k += 1
      # all_pair_data[i, j, k] = (voice.note.poly_repeat_left + voice.note.poly_repeat_right) == 5; k += 1
      # all_pair_data[i, j, k] = (voice.note.poly_repeat_left + voice.note.poly_repeat_right) > 5; k += 1
      #
      # all_pair_data[i, j, k] = note.zig_zag == 0; k += 1
      # all_pair_data[i, j, k] = note.zig_zag == 1; k += 1
      # all_pair_data[i, j, k] = note.zig_zag == 2; k += 1
      #
      # all_pair_data[i, j, k] = voice.note.zig_zag == 0; k += 1
      # all_pair_data[i, j, k] = voice.note.zig_zag == 1; k += 1
      # all_pair_data[i, j, k] = voice.note.zig_zag == 2; k += 1
      #
      # all_pair_data[i, j, k] = note.zig_zag == voice.note.zig_zag; k += 1
      #
      # all_pair_data[i, j, k] = voice.note is note.poly_pairs.left[0] if len(note.poly_pairs.left) > 0 else False; k += 1 
      # all_pair_data[i, j, k] = note.poly_pairs.left[0].poly_pairs.left[0] is voice.note if len(note.poly_pairs.left) > 0 and len(note.poly_pairs.left[0].poly_pairs.left) > 0 else False; k += 1


      # all_pair_data[i, j, k] = note.poly_right is not None; k += 1
      # all_pair_data[i, j, k] = voice.note is note.note_left; k += 1
      #
      # all_pair_data[i, j, k] = (
      #   0 if note.poly_right is None else 
      #   note.ql_duration == note.poly_right.ql_duration and 
      #   note.ql_duration == voice.note.ql_duration
      # ); k += 1
      #
      # all_pair_data[i, j, k] = (
      #   0 if voice.note.poly_right is None else 
      #   voice.note.ql_duration == voice.note.poly_right.ql_duration
      # ); k += 1
      #
      # all_pair_data[i, j, k] = (
      #   0 if note.poly_right is None else 
      #   note.pitch_space == note.poly_right.pitch_space and 
      #   note.pitch_space == voice.note.pitch_space
      # ); k += 1
      #
      # all_pair_data[i, j, k] = (
      #   0 if voice.note.poly_right is None else 
      #   voice.note.pitch_space == voice.note.poly_right.pitch_space
      # ); k += 1
      #
      # all_pair_data[i, j, k] = (
      #   1 if note.poly_right is None else
      #   abs(note.pitch_space - note.poly_right.pitch_space) / 50
      # ); k += 1
      #
      # all_pair_data[i, j, k] = (
      #   1 if voice.note.poly_right is None else 
      #   abs(voice.note.pitch_space - voice.note.poly_right.pitch_space) / 50
      # ); k += 1

    all_pair_data[i, len_active_subset, :] = 0
    all_pair_data[i, len_active_subset, 0] = 1

  if k > 0:
    assert k == COUNT, k
