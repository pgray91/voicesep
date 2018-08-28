import voicesep.utils.constants as const
COUNT = 411
def create(voice):
  prev_voice_top = voice.left[0] if len(voice.left) > 0 else None
  prev_voice_top2 = prev_voice_top.left[0] if prev_voice_top and len(prev_voice_top.left) > 0 else None
  prev_voice_top3 = prev_voice_top2.left[0] if prev_voice_top2 and len(prev_voice_top2.left) > 0 else None

  len_left = len(voice.left)
  prev_voice_bottom = voice.left[len_left-1] if len(voice.left) > 0 else None

  len_left = len(prev_voice_bottom.left) if prev_voice_bottom else 0 
  prev_voice_bottom2 = prev_voice_bottom.left[len_left-1] if prev_voice_bottom and len(prev_voice_bottom.left) > 0 else None

  len_left = len(prev_voice_bottom2.left) if prev_voice_bottom2 else 0 
  prev_voice_bottom3 = prev_voice_bottom2.left[len_left-1] if prev_voice_bottom2 and len(prev_voice_bottom2.left) > 0 else None

  data = [
    # Pitch
    voice.note.pitch_space >= 80,
    voice.note.pitch_space >= 75 and voice.note.pitch_space < 80,
    voice.note.pitch_space >= 70 and voice.note.pitch_space < 75,
    voice.note.pitch_space >= 65 and voice.note.pitch_space < 70,
    voice.note.pitch_space >= 60 and voice.note.pitch_space < 65,
    voice.note.pitch_space >= 55 and voice.note.pitch_space < 60,
    voice.note.pitch_space >= 50 and voice.note.pitch_space < 55,
    voice.note.pitch_space >= 45 and voice.note.pitch_space < 50,
    voice.note.pitch_space >= 40 and voice.note.pitch_space < 45,
    voice.note.pitch_space < 40,

    voice.avg_pitch_space >= 80,
    voice.avg_pitch_space >= 75 and voice.avg_pitch_space < 80,
    voice.avg_pitch_space >= 70 and voice.avg_pitch_space < 75,
    voice.avg_pitch_space >= 65 and voice.avg_pitch_space < 70,
    voice.avg_pitch_space >= 60 and voice.avg_pitch_space < 65,
    voice.avg_pitch_space >= 55 and voice.avg_pitch_space < 60,
    voice.avg_pitch_space >= 50 and voice.avg_pitch_space < 55,
    voice.avg_pitch_space >= 45 and voice.avg_pitch_space < 50,
    voice.avg_pitch_space >= 40 and voice.avg_pitch_space < 45,
    voice.avg_pitch_space < 40,

    voice.max_pitch_space >= 80,
    voice.max_pitch_space >= 75 and voice.max_pitch_space < 80,
    voice.max_pitch_space >= 70 and voice.max_pitch_space < 75,
    voice.max_pitch_space >= 65 and voice.max_pitch_space < 70,
    voice.max_pitch_space >= 60 and voice.max_pitch_space < 65,
    voice.max_pitch_space >= 55 and voice.max_pitch_space < 60,
    voice.max_pitch_space >= 50 and voice.max_pitch_space < 55,
    voice.max_pitch_space >= 45 and voice.max_pitch_space < 50,
    voice.max_pitch_space >= 40 and voice.max_pitch_space < 45,
    voice.max_pitch_space < 40,

    voice.min_pitch_space >= 80,
    voice.min_pitch_space >= 75 and voice.min_pitch_space < 80,
    voice.min_pitch_space >= 70 and voice.min_pitch_space < 75,
    voice.min_pitch_space >= 65 and voice.min_pitch_space < 70,
    voice.min_pitch_space >= 60 and voice.min_pitch_space < 65,
    voice.min_pitch_space >= 55 and voice.min_pitch_space < 60,
    voice.min_pitch_space >= 50 and voice.min_pitch_space < 55,
    voice.min_pitch_space >= 45 and voice.min_pitch_space < 50,
    voice.min_pitch_space >= 40 and voice.min_pitch_space < 45,
    voice.min_pitch_space < 40,
      

      # Note above
    abs(voice.note.pitch_space - voice.note.note_above.pitch_space) / const.MAX_PITCH_DISTANCE if voice.note.note_above else 1,
    abs(voice.note.pitch_space - voice.note.note_below.pitch_space) / const.MAX_PITCH_DISTANCE if voice.note.note_below else 1,

    voice.avg_pitch_dis_above / const.MAX_PITCH_DISTANCE,
    voice.avg_pitch_dis_below / const.MAX_PITCH_DISTANCE,

      # Voice above
    abs(voice.note.pitch_space - voice.voice_above.pitch_space) / const.MAX_PITCH_DISTANCE if voice.voice_above else 1,
    abs(voice.note.pitch_space - voice.voice_below.pitch_space) / const.MAX_PITCH_DISTANCE if voice.voice_below else 1,

    voice.note.pitch_space < voice.voice_above.pitch_space if voice.voice_above else 0,
    voice.note.pitch_space > voice.voice_above.pitch_space if voice.voice_above else 0,
    voice.note.pitch_space == voice.voice_above.pitch_space if voice.voice_above else 0,

    voice.note.pitch_space < voice.voice_below.pitch_space if voice.voice_below else 0,
    voice.note.pitch_space > voice.voice_below.pitch_space if voice.voice_below else 0,
    voice.note.pitch_space == voice.voice_below.pitch_space if voice.voice_below else 0,

    abs(voice.avg_pitch_space - voice.voice_above.avg_pitch_space) / const.MAX_PITCH_DISTANCE if voice.voice_above else 1,
    abs(voice.avg_pitch_space - voice.voice_below.avg_pitch_space) / const.MAX_PITCH_DISTANCE if voice.voice_below else 1,

    voice.avg_pitch_space < voice.voice_above.avg_pitch_space if voice.voice_above else 0,
    voice.avg_pitch_space > voice.voice_above.avg_pitch_space if voice.voice_above else 0,
    voice.avg_pitch_space == voice.voice_above.avg_pitch_space if voice.voice_above else 0,

    voice.avg_pitch_space < voice.voice_below.avg_pitch_space if voice.voice_below else 0,
    voice.avg_pitch_space > voice.voice_below.avg_pitch_space if voice.voice_below else 0,
    voice.avg_pitch_space == voice.voice_below.avg_pitch_space if voice.voice_below else 0,

      # Last above
    abs(voice.note.pitch_space - voice.last_above.pitch_space) / const.MAX_PITCH_DISTANCE if voice.last_above else 1,
    abs(voice.note.pitch_space - voice.last_below.pitch_space) / const.MAX_PITCH_DISTANCE if voice.last_below else 1,

    voice.note.pitch_space < voice.last_above.pitch_space if voice.last_above else 0,
    voice.note.pitch_space > voice.last_above.pitch_space if voice.last_above else 0,
    voice.note.pitch_space == voice.last_above.pitch_space if voice.last_above else 0,

    voice.note.pitch_space < voice.last_below.pitch_space if voice.last_below else 0,
    voice.note.pitch_space > voice.last_below.pitch_space if voice.last_below else 0,
    voice.note.pitch_space == voice.last_below.pitch_space if voice.last_below else 0,

    abs(voice.avg_pitch_space - voice.last_above.avg_pitch_space) / const.MAX_PITCH_DISTANCE if voice.last_above else 1,
    abs(voice.avg_pitch_space - voice.last_below.avg_pitch_space) / const.MAX_PITCH_DISTANCE if voice.last_below else 1,

    voice.avg_pitch_space < voice.last_above.avg_pitch_space if voice.last_above else 0,
    voice.avg_pitch_space > voice.last_above.avg_pitch_space if voice.last_above else 0,
    voice.avg_pitch_space == voice.last_above.avg_pitch_space if voice.last_above else 0,

    voice.avg_pitch_space < voice.last_below.avg_pitch_space if voice.last_below else 0,
    voice.avg_pitch_space > voice.last_below.avg_pitch_space if voice.last_below else 0,
    voice.avg_pitch_space == voice.last_below.avg_pitch_space if voice.last_below else 0,

    abs(voice.pitch_space - prev_voice_top.pitch_space) / const.MAX_PITCH_DISTANCE if prev_voice_top else 1,
    voice.pitch_space < prev_voice_top.pitch_space if prev_voice_top else 0,
    voice.pitch_space > prev_voice_top.pitch_space if prev_voice_top else 0,
    voice.pitch_space == prev_voice_top.pitch_space if prev_voice_top else 0,

    abs(prev_voice_top.pitch_space - prev_voice_top.note.note_above.pitch_space) / const.MAX_PITCH_DISTANCE if prev_voice_top and prev_voice_top.note.note_above else 1,

    abs(prev_voice_top.pitch_space - prev_voice_top2.pitch_space) / const.MAX_PITCH_DISTANCE if prev_voice_top and prev_voice_top2 else 1,
    prev_voice_top.pitch_space < prev_voice_top2.pitch_space if prev_voice_top and prev_voice_top2 else 0,
    prev_voice_top.pitch_space > prev_voice_top2.pitch_space if prev_voice_top and prev_voice_top2 else 0,
    prev_voice_top.pitch_space == prev_voice_top2.pitch_space if prev_voice_top and prev_voice_top2 else 0,

    abs(prev_voice_top2.pitch_space - prev_voice_top2.note.note_above.pitch_space) / const.MAX_PITCH_DISTANCE if prev_voice_top2 and prev_voice_top2.note.note_above else 1,

    abs(prev_voice_top2.pitch_space - prev_voice_top3.pitch_space) / const.MAX_PITCH_DISTANCE if prev_voice_top2 and prev_voice_top3 else 1,
    prev_voice_top2.pitch_space < prev_voice_top3.pitch_space if prev_voice_top2 and prev_voice_top3 else 0,
    prev_voice_top2.pitch_space > prev_voice_top3.pitch_space if prev_voice_top2 and prev_voice_top3 else 0,
    prev_voice_top2.pitch_space == prev_voice_top3.pitch_space if prev_voice_top2 and prev_voice_top3 else 0,

    abs(prev_voice_top3.pitch_space - prev_voice_top3.note.note_above.pitch_space) / const.MAX_PITCH_DISTANCE if prev_voice_top3 and prev_voice_top3.note.note_above else 1,

    abs(voice.pitch_space - prev_voice_bottom.pitch_space) / const.MAX_PITCH_DISTANCE if prev_voice_bottom else 1,
    voice.pitch_space < prev_voice_bottom.pitch_space if prev_voice_bottom else 0,
    voice.pitch_space > prev_voice_bottom.pitch_space if prev_voice_bottom else 0,
    voice.pitch_space == prev_voice_bottom.pitch_space if prev_voice_bottom else 0,

    abs(prev_voice_bottom.pitch_space - prev_voice_bottom.note.note_below.pitch_space) / const.MAX_PITCH_DISTANCE if prev_voice_bottom and prev_voice_bottom.note.note_below else 1,

    abs(prev_voice_bottom.pitch_space - prev_voice_bottom2.pitch_space) / const.MAX_PITCH_DISTANCE if prev_voice_bottom and prev_voice_bottom2 else 1,
    prev_voice_bottom.pitch_space < prev_voice_bottom2.pitch_space if prev_voice_bottom and prev_voice_bottom2 else 0,
    prev_voice_bottom.pitch_space > prev_voice_bottom2.pitch_space if prev_voice_bottom and prev_voice_bottom2 else 0,
    prev_voice_bottom.pitch_space == prev_voice_bottom2.pitch_space if prev_voice_bottom and prev_voice_bottom2 else 0,

    abs(prev_voice_bottom2.pitch_space - prev_voice_bottom2.note.note_below.pitch_space) / const.MAX_PITCH_DISTANCE if prev_voice_bottom2 and prev_voice_bottom2.note.note_below else 1,

    abs(prev_voice_bottom2.pitch_space - prev_voice_bottom3.pitch_space) / const.MAX_PITCH_DISTANCE if prev_voice_bottom2 and prev_voice_bottom3 else 1,
    prev_voice_bottom2.pitch_space < prev_voice_bottom3.pitch_space if prev_voice_bottom2 and prev_voice_bottom3 else 0,
    prev_voice_bottom2.pitch_space > prev_voice_bottom3.pitch_space if prev_voice_bottom2 and prev_voice_bottom3 else 0,
    prev_voice_bottom2.pitch_space == prev_voice_bottom3.pitch_space if prev_voice_bottom2 and prev_voice_bottom3 else 0,

    abs(prev_voice_bottom3.pitch_space - prev_voice_bottom3.note.note_below.pitch_space) / const.MAX_PITCH_DISTANCE if prev_voice_bottom3 and prev_voice_bottom3.note.note_below else 1,

    voice.blocked,

    # Div note distance
    # 1 if len(voice.pairs.rightvoice.min_pitch_space < 40,
    voice.div_count == 0,
    voice.div_count == 1,
    voice.div_count == 2,
    voice.div_count == 3,

    # Temporal
    voice.note.beat_duration >= 4,
    voice.note.beat_duration >= 3 and voice.note.beat_duration < 4,
    voice.note.beat_duration >= 2 and voice.note.beat_duration < 3,
    voice.note.beat_duration >= 1.75 and voice.note.beat_duration < 2,
    voice.note.beat_duration >= 1.5 and voice.note.beat_duration < 1.75,
    voice.note.beat_duration >= 1.25 and voice.note.beat_duration < 1.5,
    voice.note.beat_duration >= 1 and voice.note.beat_duration < 1.25,
    voice.note.beat_duration >= 0.875 and voice.note.beat_duration < 1,
    voice.note.beat_duration >= 0.75 and voice.note.beat_duration < 0.875,
    voice.note.beat_duration >= 0.625 and voice.note.beat_duration < 0.75,
    voice.note.beat_duration >= 0.5 and voice.note.beat_duration < 0.625,
    voice.note.beat_duration >= 0.375 and voice.note.beat_duration < 0.5,
    voice.note.beat_duration >= 0.25 and voice.note.beat_duration < 0.375,
    voice.note.beat_duration >= 0.125 and voice.note.beat_duration < 0.25,
    voice.note.beat_duration < 0.125,

    voice.rest_count_top == 0,
    voice.rest_count_top == 1,
    voice.rest_count_top == 2,
    voice.rest_count_top == 3,
    voice.rest_count_top == 4,
    voice.rest_count_top == 5,
    voice.rest_count_top > 5,

    voice.rest_count_bottom == 0,
    voice.rest_count_bottom == 1,
    voice.rest_count_bottom == 2,
    voice.rest_count_bottom == 3,
    voice.rest_count_bottom == 4,
    voice.rest_count_bottom == 5,
    voice.rest_count_bottom > 5,

    voice.dur_diff_count_above == 0,
    voice.dur_diff_count_above == 1,
    voice.dur_diff_count_above == 2,
    voice.dur_diff_count_above == 3,
    voice.dur_diff_count_above == 4,
    voice.dur_diff_count_above == 5,
    voice.dur_diff_count_above > 5,

    voice.dur_diff_count_below == 0,
    voice.dur_diff_count_below == 1,
    voice.dur_diff_count_below == 2,
    voice.dur_diff_count_below == 3,
    voice.dur_diff_count_below == 4,
    voice.dur_diff_count_below == 5,
    voice.dur_diff_count_below > 5,

    # Note above and below
    abs(float(voice.note.beat_duration - voice.note.note_above.beat_duration)) / const.MAX_BEAT_DUR_DISTANCE if voice.note.note_above else 1,
    voice.note.beat_duration < voice.note.note_above.beat_duration if voice.note.note_above else 0,
    voice.note.beat_duration > voice.note.note_above.beat_duration if voice.note.note_above else 0,
    voice.note.beat_duration == voice.note.note_above.beat_duration if voice.note.note_above else 0,

    abs(float(voice.note.beat_duration - voice.note.note_below.beat_duration)) / const.MAX_BEAT_DUR_DISTANCE if voice.note.note_below else 1,
    voice.note.beat_duration < voice.note.note_below.beat_duration if voice.note.note_below else 0,
    voice.note.beat_duration > voice.note.note_below.beat_duration if voice.note.note_below else 0,
    voice.note.beat_duration == voice.note.note_below.beat_duration if voice.note.note_below else 0,

    # Voice above and below
    abs(float(voice.note.beat_duration - voice.voice_above.note.beat_duration)) / const.MAX_BEAT_DUR_DISTANCE if voice.voice_above else 1,
    voice.note.beat_duration < voice.voice_above.note.beat_duration if voice.voice_above else 0,
    voice.note.beat_duration > voice.voice_above.note.beat_duration if voice.voice_above else 0,
    voice.note.beat_duration == voice.voice_above.note.beat_duration if voice.voice_above else 0,

    abs(float(voice.note.beat_duration - voice.voice_below.note.beat_duration)) / const.MAX_BEAT_DUR_DISTANCE if voice.voice_below else 1,
    voice.note.beat_duration < voice.voice_below.note.beat_duration if voice.voice_below else 0,
    voice.note.beat_duration > voice.voice_below.note.beat_duration if voice.voice_below else 0,
    voice.note.beat_duration == voice.voice_below.note.beat_duration if voice.voice_below else 0,

    # Last
    abs(float(voice.note.beat_duration - voice.last_above.note.beat_duration)) / const.MAX_BEAT_DUR_DISTANCE if voice.last_above else 1,
    voice.note.beat_duration < voice.last_above.note.beat_duration if voice.last_above else 0,
    voice.note.beat_duration > voice.last_above.note.beat_duration if voice.last_above else 0,
    voice.note.beat_duration == voice.last_above.note.beat_duration if voice.last_above else 0,

    abs(float(voice.note.beat_duration - voice.last_below.note.beat_duration)) / const.MAX_BEAT_DUR_DISTANCE if voice.last_below else 1,
    voice.note.beat_duration < voice.last_below.note.beat_duration if voice.last_below else 0,
    voice.note.beat_duration > voice.last_below.note.beat_duration if voice.last_below else 0,
    voice.note.beat_duration == voice.last_below.note.beat_duration if voice.last_below else 0,

    # Prev
    max(float(voice.note.beat_onset - prev_voice_top.note.beat_onset), 0) / const.MAX_BEAT_ONSET_DISTANCE if prev_voice_top else 1,
    voice.note.beat_onset < prev_voice_top.note.beat_onset if prev_voice_top else 0,
    voice.note.beat_onset > prev_voice_top.note.beat_onset if prev_voice_top else 0,
    voice.note.beat_onset == prev_voice_top.note.beat_onset if prev_voice_top else 0,

    max(float(voice.note.beat_onset - prev_voice_top.note.beat_offset), 0) / const.MAX_BEAT_ONSET_OFFSET if prev_voice_top else 1,
    voice.note.beat_onset < prev_voice_top.note.beat_offset if prev_voice_top else 0,
    voice.note.beat_onset > prev_voice_top.note.beat_offset if prev_voice_top else 0,
    voice.note.beat_onset == prev_voice_top.note.beat_offset if prev_voice_top else 0,

    max(float(prev_voice_top.note.beat_onset - prev_voice_top2.note.beat_onset), 0) / const.MAX_BEAT_ONSET_DISTANCE if prev_voice_top and prev_voice_top2 else 1,
    prev_voice_top.note.beat_onset < prev_voice_top2.note.beat_onset if prev_voice_top and prev_voice_top2 else 0,
    prev_voice_top.note.beat_onset > prev_voice_top2.note.beat_onset if prev_voice_top and prev_voice_top2 else 0,
    prev_voice_top.note.beat_onset == prev_voice_top2.note.beat_onset if prev_voice_top and prev_voice_top2 else 0,

    max(float(prev_voice_top.note.beat_onset - prev_voice_top2.note.beat_offset), 0) / const.MAX_BEAT_ONSET_OFFSET if prev_voice_top and prev_voice_top2 else 1,
    prev_voice_top.note.beat_onset < prev_voice_top2.note.beat_offset if prev_voice_top and prev_voice_top2 else 0,
    prev_voice_top.note.beat_onset > prev_voice_top2.note.beat_offset if prev_voice_top and prev_voice_top2 else 0,
    prev_voice_top.note.beat_onset == prev_voice_top2.note.beat_offset if prev_voice_top and prev_voice_top2 else 0,

    max(float(prev_voice_top2.note.beat_onset - prev_voice_top3.note.beat_onset), 0) / const.MAX_BEAT_ONSET_DISTANCE if prev_voice_top2 and prev_voice_top3 else 1,
    prev_voice_top2.note.beat_onset < prev_voice_top3.note.beat_onset if prev_voice_top2 and prev_voice_top3 else 0,
    prev_voice_top2.note.beat_onset > prev_voice_top3.note.beat_onset if prev_voice_top2 and prev_voice_top3 else 0,
    prev_voice_top2.note.beat_onset == prev_voice_top3.note.beat_onset if prev_voice_top2 and prev_voice_top3 else 0,

    max(float(prev_voice_top2.note.beat_onset - prev_voice_top3.note.beat_offset), 0) / const.MAX_BEAT_ONSET_OFFSET if prev_voice_top2 and prev_voice_top3 else 1,
    prev_voice_top2.note.beat_onset < prev_voice_top3.note.beat_offset if prev_voice_top2 and prev_voice_top3 else 0,
    prev_voice_top2.note.beat_onset > prev_voice_top3.note.beat_offset if prev_voice_top2 and prev_voice_top3 else 0,
    prev_voice_top2.note.beat_onset == prev_voice_top3.note.beat_offset if prev_voice_top2 and prev_voice_top3 else 0,

    max(float(voice.note.beat_onset - prev_voice_bottom.note.beat_onset), 0) / const.MAX_BEAT_ONSET_DISTANCE if prev_voice_bottom else 1,
    voice.note.beat_onset < prev_voice_bottom.note.beat_onset if prev_voice_bottom else 0,
    voice.note.beat_onset > prev_voice_bottom.note.beat_onset if prev_voice_bottom else 0,
    voice.note.beat_onset == prev_voice_bottom.note.beat_onset if prev_voice_bottom else 0,

    max(float(voice.note.beat_onset - prev_voice_bottom.note.beat_offset), 0) / const.MAX_BEAT_ONSET_OFFSET if prev_voice_bottom else 1,
    voice.note.beat_onset < prev_voice_bottom.note.beat_offset if prev_voice_bottom else 0,
    voice.note.beat_onset > prev_voice_bottom.note.beat_offset if prev_voice_bottom else 0,
    voice.note.beat_onset == prev_voice_bottom.note.beat_offset if prev_voice_bottom else 0,

    max(float(prev_voice_bottom.note.beat_onset - prev_voice_bottom2.note.beat_onset), 0) / const.MAX_BEAT_ONSET_DISTANCE if prev_voice_bottom and prev_voice_bottom2 else 1,
    prev_voice_bottom.note.beat_onset < prev_voice_bottom2.note.beat_onset if prev_voice_bottom and prev_voice_bottom2 else 0,
    prev_voice_bottom.note.beat_onset > prev_voice_bottom2.note.beat_onset if prev_voice_bottom and prev_voice_bottom2 else 0,
    prev_voice_bottom.note.beat_onset == prev_voice_bottom2.note.beat_onset if prev_voice_bottom and prev_voice_bottom2 else 0,

    max(float(prev_voice_bottom.note.beat_onset - prev_voice_bottom2.note.beat_offset), 0) / const.MAX_BEAT_ONSET_OFFSET if prev_voice_bottom and prev_voice_bottom2 else 1,
    prev_voice_bottom.note.beat_onset < prev_voice_bottom2.note.beat_offset if prev_voice_bottom and prev_voice_bottom2 else 0,
    prev_voice_bottom.note.beat_onset > prev_voice_bottom2.note.beat_offset if prev_voice_bottom and prev_voice_bottom2 else 0,
    prev_voice_bottom.note.beat_onset == prev_voice_bottom2.note.beat_offset if prev_voice_bottom and prev_voice_bottom2 else 0,

    max(float(prev_voice_bottom2.note.beat_onset - prev_voice_bottom3.note.beat_onset), 0) / const.MAX_BEAT_ONSET_DISTANCE if prev_voice_bottom2 and prev_voice_bottom3 else 1,
    prev_voice_bottom2.note.beat_onset < prev_voice_bottom3.note.beat_onset if prev_voice_bottom2 and prev_voice_bottom3 else 0,
    prev_voice_bottom2.note.beat_onset > prev_voice_bottom3.note.beat_onset if prev_voice_bottom2 and prev_voice_bottom3 else 0,
    prev_voice_bottom2.note.beat_onset == prev_voice_bottom3.note.beat_onset if prev_voice_bottom2 and prev_voice_bottom3 else 0,

    max(float(prev_voice_bottom2.note.beat_onset - prev_voice_bottom3.note.beat_offset), 0) / const.MAX_BEAT_ONSET_OFFSET if prev_voice_bottom2 and prev_voice_bottom3 else 1,
    prev_voice_bottom2.note.beat_onset < prev_voice_bottom3.note.beat_offset if prev_voice_bottom2 and prev_voice_bottom3 else 0,
    prev_voice_bottom2.note.beat_onset > prev_voice_bottom3.note.beat_offset if prev_voice_bottom2 and prev_voice_bottom3 else 0,
    prev_voice_bottom2.note.beat_onset == prev_voice_bottom3.note.beat_offset if prev_voice_bottom2 and prev_voice_bottom3 else 0,
   
    # Positional
    prev_voice_top is None,
    prev_voice_top2 is None,
    prev_voice_top3 is None,

    prev_voice_bottom is None,
    prev_voice_bottom2 is None,
    prev_voice_bottom3 is None,

    voice.note.note_above is None,
    voice.note.note_below is None,

    voice.voice_above is None,
    voice.voice_below is None,

    voice.last_above is None,
    voice.last_below is None,

    voice.last_above is not voice.voice_above and voice.nv_above is not voice.last_above and voice.nv_above is not voice.voice_above,
    voice.nv_above is voice.voice_above and voice.nv_above is voice.last_above,
    voice.nv_above is voice.voice_above and voice.nv_above is not voice.last_above,
    voice.last_above is not voice.voice_above and voice.nv_above is voice.last_above,
    voice.last_above is voice.voice_above and voice.nv_above is not voice.last_above,

    voice.last_below is not voice.voice_below and voice.nv_below is not voice.last_below and voice.nv_below is not voice.voice_below,
    voice.nv_below is voice.voice_below and voice.nv_below is voice.last_below,
    voice.nv_below is voice.voice_below and voice.nv_below is not voice.last_below,
    voice.last_below is not voice.voice_below and voice.nv_below is voice.last_below,
    voice.last_below is voice.voice_below and voice.nv_below is not voice.last_below,

    voice.note.index == 0,
    voice.note.index == 1,
    voice.note.index == 2,
    voice.note.index == 3,
    voice.note.index == 4,
    voice.note.index == 5,
    voice.note.index == 6,
    voice.note.index == 7,

    voice.subset_index == 0,
    voice.subset_index == 1,
    voice.subset_index == 2,
    voice.subset_index == 3,
    voice.subset_index == 4,
    voice.subset_index == 5,
    voice.subset_index == 6,
    voice.subset_index == 7,
    voice.subset_index == 8,
    voice.subset_index == 9,
    voice.subset_index == 10,
    voice.subset_index == 11,
    voice.subset_index == 12,
    voice.subset_index == 13,
    voice.subset_index == 14,

    voice.last_index == 0,
    voice.last_index == 0.5,
    voice.last_index == 1,
    voice.last_index == 1.5,
    voice.last_index == 2,
    voice.last_index == 2.5,
    voice.last_index == 3,
    voice.last_index == 3.5,
    voice.last_index == 4,
    voice.last_index == 4.5,
    voice.last_index == 5,
    voice.last_index == 5.5,
    voice.last_index == 6,
    voice.last_index == 6.5,
    voice.last_index == 7,
    voice.last_index == 7.5,
    voice.last_index == 8,
    voice.last_index == 8.5,
    voice.last_index == 9,
    voice.last_index == 9.5,
    voice.last_index == 10,

    voice.note.chord_length == 1,
    voice.note.chord_length == 2,
    voice.note.chord_length == 3,
    voice.note.chord_length == 4,
    voice.note.chord_length == 5,
    voice.note.chord_length == 6,
    voice.note.chord_length == 7,
    voice.note.chord_length == 8,

    voice.subset_length == 1,
    voice.subset_length == 2,
    voice.subset_length == 3,
    voice.subset_length == 4,
    voice.subset_length == 5,
    voice.subset_length == 6,
    voice.subset_length == 7,
    voice.subset_length == 8,
    voice.subset_length == 9,
    voice.subset_length == 10,
    voice.subset_length == 11,
    voice.subset_length == 12,
    voice.subset_length == 13,
    voice.subset_length == 14,
    voice.subset_length == 15,

    voice.last_length == 1,
    voice.last_length == 2,
    voice.last_length == 3,
    voice.last_length == 4,
    voice.last_length == 5,
    voice.last_length == 6,
    voice.last_length == 7,
    voice.last_length == 8,
    voice.last_length == 9,
    voice.last_length == 10,
    voice.last_length == 11,

    prev_voice_top.note.index == 0 if prev_voice_top else 0,
    prev_voice_top.note.index > 0 and prev_voice_top.note.index < prev_voice_top.note.chord_length - 1 if prev_voice_top else 0,
    prev_voice_top.note.index == prev_voice_top.note.chord_length - 1 if prev_voice_top else 0,

    prev_voice_top2.note.index == 0 if prev_voice_top2 else 0,
    prev_voice_top2.note.index > 0 and prev_voice_top2.note.index < prev_voice_top2.note.chord_length - 1 if prev_voice_top2 else 0,
    prev_voice_top2.note.index == prev_voice_top2.note.chord_length - 1 if prev_voice_top2 else 0,

    prev_voice_top3.note.index == 0 if prev_voice_top3 else 0,
    prev_voice_top3.note.index > 0 and prev_voice_top3.note.index < prev_voice_top3.note.chord_length - 1 if prev_voice_top3 else 0,
    prev_voice_top3.note.index == prev_voice_top3.note.chord_length - 1 if prev_voice_top3 else 0,

    prev_voice_bottom.note.index == 0 if prev_voice_bottom else 0,
    prev_voice_bottom.note.index > 0 and prev_voice_bottom.note.index < prev_voice_bottom.note.chord_length - 1 if prev_voice_bottom else 0,
    prev_voice_bottom.note.index == prev_voice_bottom.note.chord_length - 1 if prev_voice_bottom else 0,

    prev_voice_bottom2.note.index == 0 if prev_voice_bottom2 else 0,
    prev_voice_bottom2.note.index > 0 and prev_voice_bottom2.note.index < prev_voice_bottom2.note.chord_length - 1 if prev_voice_bottom2 else 0,
    prev_voice_bottom2.note.index == prev_voice_bottom2.note.chord_length - 1 if prev_voice_bottom2 else 0,

    prev_voice_bottom3.note.index == 0 if prev_voice_bottom3 else 0,
    prev_voice_bottom3.note.index > 0 and prev_voice_bottom3.note.index < prev_voice_bottom3.note.chord_length - 1 if prev_voice_bottom3 else 0,
    prev_voice_bottom3.note.index == prev_voice_bottom3.note.chord_length - 1 if prev_voice_bottom3 else 0,
   
    voice.length_top == 1,
    voice.length_top == 2,
    voice.length_top == 3,
    voice.length_top == 4,
    voice.length_top == 5,
    voice.length_top == 6,
    voice.length_top == 7,
    voice.length_top == 8,
    voice.length_top == 9,
    voice.length_top == 10,
    
    voice.length_bottom == 1,
    voice.length_bottom == 2,
    voice.length_bottom == 3,
    voice.length_bottom == 4,
    voice.length_bottom == 5,
    voice.length_bottom == 6,
    voice.length_bottom == 7,
    voice.length_bottom == 8,
    voice.length_bottom == 9,
    voice.length_bottom == 10,

    voice.position == 0,
    voice.position == 1,
    voice.position == 2,
    voice.position == 3,
    voice.position == 4,
    voice.position == 5,
    voice.position == 6,
    voice.position == 7,
    voice.position == 8,
    voice.position > 8,

    voice.note_count == 1,
    voice.note_count == 2,
    voice.note_count == 3,
    voice.note_count == 4,
    voice.note_count == 5,
    voice.note_count == 6,
    voice.note_count == 7,
    voice.note_count == 8,
    voice.note_count == 9,
    voice.note_count == 10,
    voice.note_count == 11,
    voice.note_count == 12,


    # Tonal
    voice.note.degree == 1,
    voice.note.degree == 2,
    voice.note.degree == 3,
    voice.note.degree == 4,
    voice.note.degree == 5,
    voice.note.degree == 6,
    voice.note.degree == 7,

    voice.note.chord_step == 1,
    voice.note.chord_step == 2,
    voice.note.chord_step == 3,
    voice.note.chord_step == 4,
    voice.note.chord_step == 5,
    voice.note.chord_step == 6,
    voice.note.chord_step == 7,

    # Metrical
    voice.note.beat_strength == 1,
    voice.note.beat_strength >= 0.9 and voice.note.beat_strength < 1,
    voice.note.beat_strength >= 0.8 and voice.note.beat_strength < 0.9,
    voice.note.beat_strength >= 0.7 and voice.note.beat_strength < 0.8,
    voice.note.beat_strength >= 0.6 and voice.note.beat_strength < 0.7,
    voice.note.beat_strength >= 0.5 and voice.note.beat_strength < 0.6,
    voice.note.beat_strength >= 0.4 and voice.note.beat_strength < 0.5,
    voice.note.beat_strength >= 0.3 and voice.note.beat_strength < 0.4,
    voice.note.beat_strength >= 0.2 and voice.note.beat_strength < 0.3,
    voice.note.beat_strength >= 0.1 and voice.note.beat_strength < 0.2,
    voice.note.beat_strength < 0.1,
  ]

  assert len(data) == COUNT, len(data)
  return data
