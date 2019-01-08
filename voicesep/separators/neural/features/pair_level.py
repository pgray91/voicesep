import voicesep.utils.constants as const
COUNT = 203

def create(note, voice, chord):
  len_conv_notes = len(voice.conv_notes)
  len_right = len(voice.right)

  voice_above_divs = [] if voice.voice_above is None else list(set(voice.voice_above.div_notes) & set(voice.div_notes))
  voice_above_divs.sort(key=lambda v : v.beat_onset)
  voice_above_div = None if len(voice_above_divs) == 0 else voice_above_divs[len(voice_above_divs)-1]

  voice_below_divs = [] if voice.voice_below is None else list(set(voice.voice_below.div_notes) & set(voice.div_notes))
  voice_below_divs.sort(key=lambda v : v.beat_onset)
  voice_below_div = None if len(voice_below_divs) == 0 else voice_below_divs[len(voice_below_divs)-1]

  last_above_divs = [] if voice.last_above is None else list(set(voice.last_above.div_notes) & set(voice.div_notes))
  last_above_divs.sort(key=lambda v : v.beat_onset)
  last_above_div = None if len(last_above_divs) == 0 else last_above_divs[len(last_above_divs)-1]

  last_below_divs = [] if voice.last_below is None else list(set(voice.last_below.div_notes) & set(voice.div_notes))
  last_below_divs.sort(key=lambda v : v.beat_onset)
  last_below_div = None if len(last_below_divs) == 0 else last_below_divs[len(last_below_divs)-1]

  nv_above_divs = [] if voice.nv_above is None else list(set(voice.nv_above.div_notes) & set(voice.div_notes))
  nv_above_divs.sort(key=lambda v : v.beat_onset)
  nv_above_div = None if len(nv_above_divs) == 0 else nv_above_divs[len(nv_above_divs)-1]

  nv_below_divs = [] if voice.nv_below is None else list(set(voice.nv_below.div_notes) & set(voice.div_notes))
  nv_below_divs.sort(key=lambda v : v.beat_onset)
  nv_below_div = None if len(nv_below_divs) == 0 else nv_below_divs[len(nv_below_divs)-1]

  data = [
    0,

    abs(float(note.pitch_space - voice.note.pitch_space)) / const.MAX_PITCH_DISTANCE,
    note.pitch_space == voice.note.pitch_space,
    note.pitch_space > voice.note.pitch_space,
    note.pitch_space < voice.note.pitch_space,

    abs(float(note.pitch_space - voice.avg_pitch_space)) / const.MAX_PITCH_DISTANCE,
    note.pitch_space == voice.avg_pitch_space,
    note.pitch_space > voice.avg_pitch_space,
    note.pitch_space < voice.avg_pitch_space,

    abs(float(note.pitch_space - voice.max_pitch_space)) / const.MAX_PITCH_DISTANCE,
    note.pitch_space == voice.max_pitch_space,
    note.pitch_space > voice.max_pitch_space,
    note.pitch_space < voice.max_pitch_space,

    abs(float(note.pitch_space - voice.min_pitch_space)) / const.MAX_PITCH_DISTANCE,
    note.pitch_space == voice.min_pitch_space,
    note.pitch_space > voice.min_pitch_space,
    note.pitch_space < voice.min_pitch_space,

    abs(
      voice.std_pitch_space - 
      abs(note.pitch_space - voice.avg_pitch_space)
    ) / const.MAX_PITCH_DISTANCE,
    abs(note.pitch_space - voice.avg_pitch_space) < voice.std_pitch_space,

    1 if note.note_above is None else abs(
      note.note_above.pitch_space - voice.note.pitch_space
    ) / const.MAX_PITCH_DISTANCE,

    1 if note.note_below is None else abs(
      note.note_below.pitch_space - voice.note.pitch_space
    ) / const.MAX_PITCH_DISTANCE,

    # Note in voice
    1 if voice.note.note_above is None else abs(
      voice.note.note_above.pitch_space - note.pitch_space
    ) / const.MAX_PITCH_DISTANCE,

    1 if voice.note.note_below is None else abs(
      voice.note.note_below.pitch_space - note.pitch_space
    ) / const.MAX_PITCH_DISTANCE,

    # Last above and below
    1 if voice.last_above is None else abs(
      voice.last_above.pitch_space - note.pitch_space
    ) / const.MAX_PITCH_DISTANCE,

    1 if voice.last_below is None else abs(
      voice.last_below.pitch_space - note.pitch_space
    ) / const.MAX_PITCH_DISTANCE,

    # Subset above and below
    1 if voice.voice_above is None else abs(
      voice.voice_above.pitch_space - note.pitch_space
    ) / const.MAX_PITCH_DISTANCE,

    1 if voice.voice_below is None else abs(
      voice.voice_below.pitch_space - note.pitch_space
    ) / const.MAX_PITCH_DISTANCE,

    # Consecutive repeats
    note.pitch_space != voice.note.pitch_space,
    note.pitch_space == voice.note.pitch_space and voice.cons_repeat == 0,
    note.pitch_space == voice.note.pitch_space and voice.cons_repeat == 1,
    note.pitch_space == voice.note.pitch_space and voice.cons_repeat == 2,
    note.pitch_space == voice.note.pitch_space and voice.cons_repeat == 3,
    note.pitch_space == voice.note.pitch_space and voice.cons_repeat > 3,

    # Shared div note
    # Voice above and below
    voice_above_div is not None,
    1 if voice_above_div is None else abs(voice_above_div.pitch_space - note.pitch_space) / const.MAX_PITCH_DISTANCE,
    0 if voice_above_div is None else voice_above_div.pitch_space > note.pitch_space,
    0 if voice_above_div is None else voice_above_div.pitch_space < note.pitch_space,
    0 if voice_above_div is None else voice_above_div.pitch_space == note.pitch_space,

    voice_below_div is not None,
    1 if voice_below_div is None else abs(voice_below_div.pitch_space - note.pitch_space) / const.MAX_PITCH_DISTANCE,
    0 if voice_below_div is None else voice_below_div.pitch_space > note.pitch_space,
    0 if voice_below_div is None else voice_below_div.pitch_space < note.pitch_space,
    0 if voice_below_div is None else voice_below_div.pitch_space == note.pitch_space,

    # Last above and below
    last_above_div is not None,
    1 if last_above_div is None else abs(last_above_div.pitch_space - note.pitch_space) / const.MAX_PITCH_DISTANCE,
    0 if last_above_div is None else last_above_div.pitch_space > note.pitch_space,
    0 if last_above_div is None else last_above_div.pitch_space < note.pitch_space,
    0 if last_above_div is None else last_above_div.pitch_space == note.pitch_space,

    last_below_div is not None,
    1 if last_below_div is None else abs(last_below_div.pitch_space - note.pitch_space) / const.MAX_PITCH_DISTANCE,
    0 if last_below_div is None else last_below_div.pitch_space > note.pitch_space,
    0 if last_below_div is None else last_below_div.pitch_space < note.pitch_space,
    0 if last_below_div is None else last_below_div.pitch_space == note.pitch_space,

    # nv above and below
    nv_above_div is not None,
    1 if nv_above_div is None else abs(nv_above_div.pitch_space - note.pitch_space) / const.MAX_PITCH_DISTANCE,
    0 if nv_above_div is None else nv_above_div.pitch_space > note.pitch_space,
    0 if nv_above_div is None else nv_above_div.pitch_space < note.pitch_space,
    0 if nv_above_div is None else nv_above_div.pitch_space == note.pitch_space,

    nv_below_div is not None,
    1 if nv_below_div is None else abs(nv_below_div.pitch_space - note.pitch_space) / const.MAX_PITCH_DISTANCE,
    0 if nv_below_div is None else nv_below_div.pitch_space > note.pitch_space,
    0 if nv_below_div is None else nv_below_div.pitch_space < note.pitch_space,
    0 if nv_below_div is None else nv_below_div.pitch_space == note.pitch_space,

    # Conv notes
    len(voice.conv_notes) > 0,

    abs(voice.conv_notes[0].pitch_space - note.note_above.pitch_space) / const.MAX_PITCH_DISTANCE if len(voice.conv_notes) > 0 and note.note_above is not None else 1,
    voice.conv_notes[0].pitch_space > note.note_above.pitch_space if len(voice.conv_notes) > 0 and note.note_above is not None else 0,
    voice.conv_notes[0].pitch_space < note.note_above.pitch_space if len(voice.conv_notes) > 0 and note.note_above is not None else 0,
    voice.conv_notes[0].pitch_space == note.note_above.pitch_space if len(voice.conv_notes) > 0 and note.note_above is not None else 0,

    abs(voice.conv_notes[0].pitch_space - note.pitch_space) / const.MAX_PITCH_DISTANCE if len(voice.conv_notes) > 0 else 1,
    voice.conv_notes[0].pitch_space > note.pitch_space if len(voice.conv_notes) > 0 else 0,
    voice.conv_notes[0].pitch_space < note.pitch_space if len(voice.conv_notes) > 0 else 0,
    voice.conv_notes[0].pitch_space == note.pitch_space if len(voice.conv_notes) > 0 else 0,

    abs(voice.conv_notes[0].pitch_space - note.note_below.pitch_space) / const.MAX_PITCH_DISTANCE if len(voice.conv_notes) > 0 and note.note_below is not None else 1,
    voice.conv_notes[0].pitch_space > note.note_below.pitch_space if len(voice.conv_notes) > 0 and note.note_below is not None else 0,
    voice.conv_notes[0].pitch_space < note.note_below.pitch_space if len(voice.conv_notes) > 0 and note.note_below is not None else 0,
    voice.conv_notes[0].pitch_space == note.note_below.pitch_space if len(voice.conv_notes) > 0 and note.note_below is not None else 0,

    abs(voice.conv_notes[0].pitch_space - voice.right[0].pitch_space) / const.MAX_PITCH_DISTANCE if len(voice.conv_notes) > 0 and len(voice.right) > 0 else 1,
    voice.conv_notes[0].pitch_space > voice.right[0].pitch_space if len(voice.conv_notes) > 0 and len(voice.right) > 0 else 0,
    voice.conv_notes[0].pitch_space < voice.right[0].pitch_space if len(voice.conv_notes) > 0 and len(voice.right) > 0 else 0,
    voice.conv_notes[0].pitch_space == voice.right[0].pitch_space if len(voice.conv_notes) > 0 and len(voice.right) > 0 else 0,

    abs(voice.conv_notes[0].pitch_space - voice.right[len_right-1].pitch_space) / const.MAX_PITCH_DISTANCE if len(voice.conv_notes) > 0 and len(voice.right) > 0 else 1,
    voice.conv_notes[0].pitch_space > voice.right[len_right-1].pitch_space if len(voice.conv_notes) > 0 and len(voice.right) > 0 else 0,
    voice.conv_notes[0].pitch_space < voice.right[len_right-1].pitch_space if len(voice.conv_notes) > 0 and len(voice.right) > 0 else 0,
    voice.conv_notes[0].pitch_space == voice.right[len_right-1].pitch_space if len(voice.conv_notes) > 0 and len(voice.right) > 0 else 0,

    abs(voice.conv_notes[len_conv_notes-1].pitch_space - note.note_above.pitch_space) / const.MAX_PITCH_DISTANCE if len(voice.conv_notes) > 0 and note.note_above is not None else 1,
    voice.conv_notes[len_conv_notes-1].pitch_space > note.note_above.pitch_space if len(voice.conv_notes) > 0 and note.note_above is not None else 0,
    voice.conv_notes[len_conv_notes-1].pitch_space < note.note_above.pitch_space if len(voice.conv_notes) > 0 and note.note_above is not None else 0,
    voice.conv_notes[len_conv_notes-1].pitch_space == note.note_above.pitch_space if len(voice.conv_notes) > 0 and note.note_above is not None else 0,

    abs(voice.conv_notes[len_conv_notes-1].pitch_space - note.pitch_space) / const.MAX_PITCH_DISTANCE if len(voice.conv_notes) > 0 else 1,
    voice.conv_notes[len_conv_notes-1].pitch_space > note.pitch_space if len(voice.conv_notes) > 0 else 0,
    voice.conv_notes[len_conv_notes-1].pitch_space < note.pitch_space if len(voice.conv_notes) > 0 else 0,
    voice.conv_notes[len_conv_notes-1].pitch_space == note.pitch_space if len(voice.conv_notes) > 0 else 0,

    abs(voice.conv_notes[len_conv_notes-1].pitch_space - note.note_below.pitch_space) / const.MAX_PITCH_DISTANCE if len(voice.conv_notes) > 0 and note.note_below is not None else 1,
    voice.conv_notes[len_conv_notes-1].pitch_space > note.note_below.pitch_space if len(voice.conv_notes) > 0 and note.note_below is not None else 0,
    voice.conv_notes[len_conv_notes-1].pitch_space < note.note_below.pitch_space if len(voice.conv_notes) > 0 and note.note_below is not None else 0,
    voice.conv_notes[len_conv_notes-1].pitch_space == note.note_below.pitch_space if len(voice.conv_notes) > 0 and note.note_below is not None else 0,

    abs(voice.conv_notes[len_conv_notes-1].pitch_space - voice.right[0].pitch_space) / const.MAX_PITCH_DISTANCE if len(voice.conv_notes) > 0 and len(voice.right) > 0 else 1,
    voice.conv_notes[len_conv_notes-1].pitch_space > voice.right[0].pitch_space if len(voice.conv_notes) > 0 and len(voice.right) > 0 else 0,
    voice.conv_notes[len_conv_notes-1].pitch_space < voice.right[0].pitch_space if len(voice.conv_notes) > 0 and len(voice.right) > 0 else 0,
    voice.conv_notes[len_conv_notes-1].pitch_space == voice.right[0].pitch_space if len(voice.conv_notes) > 0 and len(voice.right) > 0 else 0,

    abs(voice.conv_notes[len_conv_notes-1].pitch_space - voice.right[len_right-1].pitch_space) / const.MAX_PITCH_DISTANCE if len(voice.conv_notes) > 0 and len(voice.right) > 0 else 1,
    voice.conv_notes[len_conv_notes-1].pitch_space > voice.right[len_right-1].pitch_space if len(voice.conv_notes) > 0 and len(voice.right) > 0 else 0,
    voice.conv_notes[len_conv_notes-1].pitch_space < voice.right[len_right-1].pitch_space if len(voice.conv_notes) > 0 and len(voice.right) > 0 else 0,
    voice.conv_notes[len_conv_notes-1].pitch_space == voice.right[len_right-1].pitch_space if len(voice.conv_notes) > 0 and len(voice.right) > 0 else 0,

    # Temporal
    float(note.beat_onset - voice.note.beat_onset) / const.MAX_BEAT_ONSET_DISTANCE,
    max(0, float(note.beat_onset - voice.beat_offset)) / const.MAX_BEAT_ONSET_DISTANCE,
    note.beat_onset == voice.note.beat_offset,
    note.beat_onset > voice.note.beat_offset,
    note.beat_onset < voice.note.beat_offset,

    float(note.beat_onset - voice.voice_above.note.beat_onset) / const.MAX_BEAT_ONSET_DISTANCE if voice.voice_above is not None else 1,
    max(0, float(note.beat_onset - voice.voice_above.beat_offset)) / const.MAX_BEAT_ONSET_OFFSET if voice.voice_above is not None else 1,
    note.beat_onset == voice.voice_above.note.beat_offset if voice.voice_above is not None else 0,
    note.beat_onset > voice.voice_above.note.beat_offset if voice.voice_above is not None else 0,
    note.beat_onset < voice.voice_above.note.beat_offset if voice.voice_above is not None else 0,

    float(note.beat_onset - voice.voice_below.note.beat_onset) / const.MAX_BEAT_ONSET_DISTANCE if voice.voice_below is not None else 1,
    max(0, float(note.beat_onset - voice.voice_below.beat_offset)) / const.MAX_BEAT_ONSET_OFFSET if voice.voice_below is not None else 1,
    note.beat_onset == voice.voice_below.note.beat_offset if voice.voice_below is not None else 0,
    note.beat_onset > voice.voice_below.note.beat_offset if voice.voice_below is not None else 0,
    note.beat_onset < voice.voice_below.note.beat_offset if voice.voice_below is not None else 0,

    float(note.beat_onset - voice.last_above.note.beat_onset) / const.MAX_BEAT_ONSET_DISTANCE if voice.last_above is not None else 1,
    max(0, float(note.beat_onset - voice.last_above.beat_offset)) / const.MAX_BEAT_ONSET_OFFSET if voice.last_above is not None else 1,
    note.beat_onset == voice.last_above.note.beat_offset if voice.last_above is not None else 0,
    note.beat_onset > voice.last_above.note.beat_offset if voice.last_above is not None else 0,
    note.beat_onset < voice.last_above.note.beat_offset if voice.last_above is not None else 0,

    float(note.beat_onset - voice.last_below.note.beat_onset) / const.MAX_BEAT_ONSET_DISTANCE if voice.last_below is not None else 1,
    max(0, float(note.beat_onset - voice.last_below.beat_offset)) / const.MAX_BEAT_ONSET_OFFSET if voice.last_below is not None else 1,
    note.beat_onset == voice.last_below.note.beat_offset if voice.last_below is not None else 0,
    note.beat_onset > voice.last_below.note.beat_offset if voice.last_below is not None else 0,
    note.beat_onset < voice.last_below.note.beat_offset if voice.last_below is not None else 0,

    abs(float(note.beat_duration - voice.note.beat_duration)) / const.MAX_BEAT_DUR_DISTANCE,
    note.beat_onset == voice.note.beat_duration,
    note.beat_onset > voice.note.beat_duration,
    note.beat_onset < voice.note.beat_duration,

    abs(float(note.beat_duration - voice.voice_above.note.beat_duration)) / const.MAX_BEAT_DUR_DISTANCE if voice.voice_above is not None else 1,
    note.beat_duration == voice.voice_above.note.beat_duration if voice.voice_above is not None else 0,
    note.beat_duration > voice.voice_above.note.beat_duration if voice.voice_above is not None else 0,
    note.beat_duration < voice.voice_above.note.beat_duration if voice.voice_above is not None else 0,

    abs(float(note.beat_duration - voice.voice_below.note.beat_duration)) / const.MAX_BEAT_DUR_DISTANCE if voice.voice_below is not None else 1,
    note.beat_duration == voice.voice_below.note.beat_duration if voice.voice_below is not None else 0,
    note.beat_duration > voice.voice_below.note.beat_duration if voice.voice_below is not None else 0,
    note.beat_duration < voice.voice_below.note.beat_duration if voice.voice_below is not None else 0,

    abs(float(note.beat_duration - voice.last_above.note.beat_duration)) / const.MAX_BEAT_DUR_DISTANCE if voice.last_above is not None else 1,
    note.beat_duration == voice.last_above.note.beat_duration if voice.last_above is not None else 0,
    note.beat_duration > voice.last_above.note.beat_duration if voice.last_above is not None else 0,
    note.beat_duration < voice.last_above.note.beat_duration if voice.last_above is not None else 0,

    abs(float(note.beat_duration - voice.last_below.note.beat_duration)) / const.MAX_BEAT_DUR_DISTANCE if voice.last_below is not None else 1,
    note.beat_duration == voice.last_below.note.beat_duration if voice.last_below is not None else 0,
    note.beat_duration > voice.last_below.note.beat_duration if voice.last_below is not None else 0,
    note.beat_duration < voice.last_below.note.beat_duration if voice.last_below is not None else 0,

    # Positional
    float(note.chord_index - voice.note.chord_index) / const.MAX_ONSET_DISTANCE,

    abs(float(note.index - voice.last_index)) / const.MAX_INDEX_DISTANCE,
    note.index == voice.last_index,
    note.index == voice.last_index + 1,
    note.index == voice.last_index - 1,
    note.index > voice.last_index + 1,
    note.index < voice.last_index - 1,

    abs(float(note.index - voice.subset_index)) / const.MAX_INDEX_DISTANCE,
    note.index == voice.subset_index,
    note.index == voice.subset_index + 1,
    note.index == voice.subset_index - 1,
    note.index > voice.subset_index + 1,
    note.index < voice.subset_index - 1,

    abs(float(note.index - voice.note.index)) / const.MAX_INDEX_DISTANCE,
    note.index == voice.note.index,
    note.index == voice.note.index + 1,
    note.index == voice.note.index - 1,
    note.index > voice.note.index + 1,
    note.index < voice.note.index - 1,

    abs(float(note.chord_length - voice.last_length)) / const.MAX_LENGTH_DISTANCE,
    note.chord_length == voice.last_length,
    note.chord_length == voice.last_length + 1,
    note.chord_length == voice.last_length - 1,
    note.chord_length > voice.last_length + 1,
    note.chord_length < voice.last_length - 1,

    abs(float(note.chord_length - voice.subset_length)) / const.MAX_LENGTH_DISTANCE,
    note.chord_length == voice.subset_length,
    note.chord_length == voice.subset_length + 1,
    note.chord_length == voice.subset_length - 1,
    note.chord_length > voice.subset_length + 1,
    note.chord_length < voice.subset_length - 1,

    abs(float(note.chord_length - voice.note.chord_length)) / const.MAX_LENGTH_DISTANCE,
    note.chord_length == voice.note.chord_length,
    note.chord_length == voice.note.chord_length + 1,
    note.chord_length == voice.note.chord_length - 1,
    note.chord_length > voice.note.chord_length + 1,
    note.chord_length < voice.note.chord_length - 1,

    abs(float(note.degree - voice.note.degree)) / const.MAX_DEGREE_DISTANCE,
    note.degree > voice.note.degree,
    note.degree < voice.note.degree,
    note.degree == voice.note.degree,

    abs(float(note.chord_step - voice.note.chord_step)) / const.MAX_DEGREE_DISTANCE,
    note.chord_step > voice.note.chord_step,
    note.chord_step < voice.note.chord_step,
    note.chord_step == voice.note.chord_step,

    abs(float(note.beat_strength - voice.note.beat_strength)),
    note.beat_strength > voice.note.beat_strength,
    note.beat_strength < voice.note.beat_strength,
    note.beat_strength == voice.note.beat_strength,

    note.repeat_count <= 4 and voice.note.repeat_count <= 4,
    note.repeat_count <= 4 and voice.note.repeat_count > 4,

    note.repeat_count > 4 and voice.note.repeat_count <= 4,
    note.repeat_count > 4 and voice.note.repeat_count > 4,
    note.repeat_count > 4 and voice.note.repeat_count > 4,

    # len(note.poly_pairs.left) > 0,
    # len(note.poly_pairs.left[0].poly_pairs.left) > 0 if len(note.poly_pairs.left) > 0 else False,
    #
    # # (note.poly_left.pitch_space > note.pitch_space) if note.poly_left is not None else False
    # note.poly_pairs.left[0].pitch_space > note.pitch_space if len(note.poly_pairs.left) > 0 else False,
    # note.poly_pairs.left[0].pitch_space < note.pitch_space if len(note.poly_pairs.left) > 0 else False,
    # note.poly_pairs.left[0].pitch_space == note.pitch_space if len(note.poly_pairs.left) > 0 else False,
    #
    # note.poly_left_count == 0,
    # note.poly_left_count == 1,
    # note.poly_left_count == 2,
    # note.poly_left_count == 3,
    # note.poly_left_count == 4,
    # note.poly_left_count == 5,
    # note.poly_left_count > 5,
    #
    # note.poly_right_count == 0,
    # note.poly_right_count == 1,
    # note.poly_right_count == 2,
    # note.poly_right_count == 3,
    # note.poly_right_count == 4,
    # note.poly_right_count == 5,
    # note.poly_right_count > 5,
    #
    # (note.poly_left_count + note.poly_right_count) == 5,
    # (note.poly_left_count + note.poly_right_count) == 6,
    # (note.poly_left_count + note.poly_right_count) == 7,
    # (note.poly_left_count + note.poly_right_count) == 8,
    # (note.poly_left_count + note.poly_right_count) > 8,
    #
    # note.poly_repeat_left == 0,
    # note.poly_repeat_left == 1,
    # note.poly_repeat_left == 2,
    # note.poly_repeat_left > 2,
    #
    # note.poly_repeat_right == 0,
    # note.poly_repeat_right == 1,
    # note.poly_repeat_right == 2,
    # note.poly_repeat_right > 2,
    #
    # (note.poly_repeat_left + note.poly_repeat_right) == 0,
    # (note.poly_repeat_left + note.poly_repeat_right) == 1,
    # (note.poly_repeat_left + note.poly_repeat_right) == 2,
    # (note.poly_repeat_left + note.poly_repeat_right) == 3,
    # (note.poly_repeat_left + note.poly_repeat_right) == 4,
    # (note.poly_repeat_left + note.poly_repeat_right) == 5,
    # (note.poly_repeat_left + note.poly_repeat_right) > 5,
    #
    # voice.note.poly_repeat_left == 0,
    # voice.note.poly_repeat_left == 1,
    # voice.note.poly_repeat_left == 2,
    # voice.note.poly_repeat_left > 2,
    #
    # voice.note.poly_repeat_right == 0,
    # voice.note.poly_repeat_right == 1,
    # voice.note.poly_repeat_right == 2,
    # voice.note.poly_repeat_right > 2,
    #
    # (voice.note.poly_repeat_left + voice.note.poly_repeat_right) == 0,
    # (voice.note.poly_repeat_left + voice.note.poly_repeat_right) == 1,
    # (voice.note.poly_repeat_left + voice.note.poly_repeat_right) == 2,
    # (voice.note.poly_repeat_left + voice.note.poly_repeat_right) == 3,
    # (voice.note.poly_repeat_left + voice.note.poly_repeat_right) == 4,
    # (voice.note.poly_repeat_left + voice.note.poly_repeat_right) == 5,
    # (voice.note.poly_repeat_left + voice.note.poly_repeat_right) > 5,
    #
    # note.zig_zag == 0,
    # note.zig_zag == 1,
    # note.zig_zag == 2,
    #
    # voice.note.zig_zag == 0,
    # voice.note.zig_zag == 1,
    # voice.note.zig_zag == 2,
    #
    # note.zig_zag == voice.note.zig_zag,
    #
    # voice.note is note.poly_pairs.left[0] if len(note.poly_pairs.left) > 0 else False,
    # note.poly_pairs.left[0].poly_pairs.left[0] is voice.note if len(note.poly_pairs.left) > 0 and len(note.poly_pairs.left[0].poly_pairs.left) > 0 else False,
  ]

  assert len(data) == COUNT, len(data)
  return data
