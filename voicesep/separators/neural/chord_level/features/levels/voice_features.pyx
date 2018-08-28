#cython: language_level=3
import cython
import voicesep.utils.constants as const

cdef int COUNT = 411

    # avg_pitch_prox
    # average duration
    # average distance between notes
    # standard deviations
    # Check and see if note.note_aboves are all connected in one voice
    # Same for note.note_belows

    # Measure how smooth the voice is
    # Is div note above or below
    # Beat duration differences for previous 3


@cython.boundscheck(False)
@cython.wraparound(False)
cdef create(float[:,::1] all_voice_data, list active_subset):
  cdef int len_active_subset = len(active_subset)

  cdef int all_voice_data_len = len(all_voice_data)
  assert all_voice_data_len == len_active_subset + 1

  cdef int all_voice_len = len(all_voice_data[0, :])
  assert all_voice_len == COUNT

  cdef int i, j = 0
  cdef int len_left = 0

  for i, voice in enumerate(active_subset):
    # assert voice.subset_index < 14, voice.subset_index
    # assert voice.last_index < 10, voice.last_index
    # assert voice.length < 20, voice.length
    # assert voice.note_count < 25, voice.note_count

    j = 0

    # Pitch
    all_voice_data[i, j] = voice.note.pitch_space >= 80; j += 1
    all_voice_data[i, j] = voice.note.pitch_space >= 75 and voice.note.pitch_space < 80; j += 1
    all_voice_data[i, j] = voice.note.pitch_space >= 70 and voice.note.pitch_space < 75; j += 1
    all_voice_data[i, j] = voice.note.pitch_space >= 65 and voice.note.pitch_space < 70; j += 1
    all_voice_data[i, j] = voice.note.pitch_space >= 60 and voice.note.pitch_space < 65; j += 1
    all_voice_data[i, j] = voice.note.pitch_space >= 55 and voice.note.pitch_space < 60; j += 1
    all_voice_data[i, j] = voice.note.pitch_space >= 50 and voice.note.pitch_space < 55; j += 1
    all_voice_data[i, j] = voice.note.pitch_space >= 45 and voice.note.pitch_space < 50; j += 1
    all_voice_data[i, j] = voice.note.pitch_space >= 40 and voice.note.pitch_space < 45; j += 1
    all_voice_data[i, j] = voice.note.pitch_space < 40; j += 1

    all_voice_data[i, j] = voice.avg_pitch_space >= 80; j += 1
    all_voice_data[i, j] = voice.avg_pitch_space >= 75 and voice.avg_pitch_space < 80; j += 1
    all_voice_data[i, j] = voice.avg_pitch_space >= 70 and voice.avg_pitch_space < 75; j += 1
    all_voice_data[i, j] = voice.avg_pitch_space >= 65 and voice.avg_pitch_space < 70; j += 1
    all_voice_data[i, j] = voice.avg_pitch_space >= 60 and voice.avg_pitch_space < 65; j += 1
    all_voice_data[i, j] = voice.avg_pitch_space >= 55 and voice.avg_pitch_space < 60; j += 1
    all_voice_data[i, j] = voice.avg_pitch_space >= 50 and voice.avg_pitch_space < 55; j += 1
    all_voice_data[i, j] = voice.avg_pitch_space >= 45 and voice.avg_pitch_space < 50; j += 1
    all_voice_data[i, j] = voice.avg_pitch_space >= 40 and voice.avg_pitch_space < 45; j += 1
    all_voice_data[i, j] = voice.avg_pitch_space < 40; j += 1

    all_voice_data[i, j] = voice.max_pitch_space >= 80; j += 1
    all_voice_data[i, j] = voice.max_pitch_space >= 75 and voice.max_pitch_space < 80; j += 1
    all_voice_data[i, j] = voice.max_pitch_space >= 70 and voice.max_pitch_space < 75; j += 1
    all_voice_data[i, j] = voice.max_pitch_space >= 65 and voice.max_pitch_space < 70; j += 1
    all_voice_data[i, j] = voice.max_pitch_space >= 60 and voice.max_pitch_space < 65; j += 1
    all_voice_data[i, j] = voice.max_pitch_space >= 55 and voice.max_pitch_space < 60; j += 1
    all_voice_data[i, j] = voice.max_pitch_space >= 50 and voice.max_pitch_space < 55; j += 1
    all_voice_data[i, j] = voice.max_pitch_space >= 45 and voice.max_pitch_space < 50; j += 1
    all_voice_data[i, j] = voice.max_pitch_space >= 40 and voice.max_pitch_space < 45; j += 1
    all_voice_data[i, j] = voice.max_pitch_space < 40; j += 1

    all_voice_data[i, j] = voice.min_pitch_space >= 80; j += 1
    all_voice_data[i, j] = voice.min_pitch_space >= 75 and voice.min_pitch_space < 80; j += 1
    all_voice_data[i, j] = voice.min_pitch_space >= 70 and voice.min_pitch_space < 75; j += 1
    all_voice_data[i, j] = voice.min_pitch_space >= 65 and voice.min_pitch_space < 70; j += 1
    all_voice_data[i, j] = voice.min_pitch_space >= 60 and voice.min_pitch_space < 65; j += 1
    all_voice_data[i, j] = voice.min_pitch_space >= 55 and voice.min_pitch_space < 60; j += 1
    all_voice_data[i, j] = voice.min_pitch_space >= 50 and voice.min_pitch_space < 55; j += 1
    all_voice_data[i, j] = voice.min_pitch_space >= 45 and voice.min_pitch_space < 50; j += 1
    all_voice_data[i, j] = voice.min_pitch_space >= 40 and voice.min_pitch_space < 45; j += 1
    all_voice_data[i, j] = voice.min_pitch_space < 40; j += 1
      

      # Note above
    all_voice_data[i, j] = abs(voice.note.pitch_space - voice.note.note_above.pitch_space) / const.MAX_PITCH_DISTANCE if voice.note.note_above else 1; j += 1
    all_voice_data[i, j] = abs(voice.note.pitch_space - voice.note.note_below.pitch_space) / const.MAX_PITCH_DISTANCE if voice.note.note_below else 1; j += 1

    all_voice_data[i, j] = voice.avg_pitch_dis_above / const.MAX_PITCH_DISTANCE; j += 1
    all_voice_data[i, j] = voice.avg_pitch_dis_below / const.MAX_PITCH_DISTANCE; j += 1

      # Voice above
    all_voice_data[i, j] = abs(voice.note.pitch_space - voice.voice_above.pitch_space) / const.MAX_PITCH_DISTANCE if voice.voice_above else 1; j += 1
    all_voice_data[i, j] = abs(voice.note.pitch_space - voice.voice_below.pitch_space) / const.MAX_PITCH_DISTANCE if voice.voice_below else 1; j += 1

    all_voice_data[i, j] = voice.note.pitch_space < voice.voice_above.pitch_space if voice.voice_above else 0; j += 1
    all_voice_data[i, j] = voice.note.pitch_space > voice.voice_above.pitch_space if voice.voice_above else 0; j += 1
    all_voice_data[i, j] = voice.note.pitch_space == voice.voice_above.pitch_space if voice.voice_above else 0; j += 1

    all_voice_data[i, j] = voice.note.pitch_space < voice.voice_below.pitch_space if voice.voice_below else 0; j += 1
    all_voice_data[i, j] = voice.note.pitch_space > voice.voice_below.pitch_space if voice.voice_below else 0; j += 1
    all_voice_data[i, j] = voice.note.pitch_space == voice.voice_below.pitch_space if voice.voice_below else 0; j += 1

    all_voice_data[i, j] = abs(voice.avg_pitch_space - voice.voice_above.avg_pitch_space) / const.MAX_PITCH_DISTANCE if voice.voice_above else 1; j += 1
    all_voice_data[i, j] = abs(voice.avg_pitch_space - voice.voice_below.avg_pitch_space) / const.MAX_PITCH_DISTANCE if voice.voice_below else 1; j += 1

    all_voice_data[i, j] = voice.avg_pitch_space < voice.voice_above.avg_pitch_space if voice.voice_above else 0; j += 1
    all_voice_data[i, j] = voice.avg_pitch_space > voice.voice_above.avg_pitch_space if voice.voice_above else 0; j += 1
    all_voice_data[i, j] = voice.avg_pitch_space == voice.voice_above.avg_pitch_space if voice.voice_above else 0; j += 1

    all_voice_data[i, j] = voice.avg_pitch_space < voice.voice_below.avg_pitch_space if voice.voice_below else 0; j += 1
    all_voice_data[i, j] = voice.avg_pitch_space > voice.voice_below.avg_pitch_space if voice.voice_below else 0; j += 1
    all_voice_data[i, j] = voice.avg_pitch_space == voice.voice_below.avg_pitch_space if voice.voice_below else 0; j += 1

      # Last above
    all_voice_data[i, j] = abs(voice.note.pitch_space - voice.last_above.pitch_space) / const.MAX_PITCH_DISTANCE if voice.last_above else 1; j += 1
    all_voice_data[i, j] = abs(voice.note.pitch_space - voice.last_below.pitch_space) / const.MAX_PITCH_DISTANCE if voice.last_below else 1; j += 1

    all_voice_data[i, j] = voice.note.pitch_space < voice.last_above.pitch_space if voice.last_above else 0; j += 1
    all_voice_data[i, j] = voice.note.pitch_space > voice.last_above.pitch_space if voice.last_above else 0; j += 1
    all_voice_data[i, j] = voice.note.pitch_space == voice.last_above.pitch_space if voice.last_above else 0; j += 1

    all_voice_data[i, j] = voice.note.pitch_space < voice.last_below.pitch_space if voice.last_below else 0; j += 1
    all_voice_data[i, j] = voice.note.pitch_space > voice.last_below.pitch_space if voice.last_below else 0; j += 1
    all_voice_data[i, j] = voice.note.pitch_space == voice.last_below.pitch_space if voice.last_below else 0; j += 1

    all_voice_data[i, j] = abs(voice.avg_pitch_space - voice.last_above.avg_pitch_space) / const.MAX_PITCH_DISTANCE if voice.last_above else 1; j += 1
    all_voice_data[i, j] = abs(voice.avg_pitch_space - voice.last_below.avg_pitch_space) / const.MAX_PITCH_DISTANCE if voice.last_below else 1; j += 1

    all_voice_data[i, j] = voice.avg_pitch_space < voice.last_above.avg_pitch_space if voice.last_above else 0; j += 1
    all_voice_data[i, j] = voice.avg_pitch_space > voice.last_above.avg_pitch_space if voice.last_above else 0; j += 1
    all_voice_data[i, j] = voice.avg_pitch_space == voice.last_above.avg_pitch_space if voice.last_above else 0; j += 1

    all_voice_data[i, j] = voice.avg_pitch_space < voice.last_below.avg_pitch_space if voice.last_below else 0; j += 1
    all_voice_data[i, j] = voice.avg_pitch_space > voice.last_below.avg_pitch_space if voice.last_below else 0; j += 1
    all_voice_data[i, j] = voice.avg_pitch_space == voice.last_below.avg_pitch_space if voice.last_below else 0; j += 1

    prev_voice_top = voice.left[0] if len(voice.left) > 0 else None
    all_voice_data[i, j] = abs(voice.pitch_space - prev_voice_top.pitch_space) / const.MAX_PITCH_DISTANCE if prev_voice_top else 1; j += 1
    all_voice_data[i, j] = voice.pitch_space < prev_voice_top.pitch_space if prev_voice_top else 0; j += 1
    all_voice_data[i, j] = voice.pitch_space > prev_voice_top.pitch_space if prev_voice_top else 0; j += 1
    all_voice_data[i, j] = voice.pitch_space == prev_voice_top.pitch_space if prev_voice_top else 0; j += 1

    all_voice_data[i, j] = abs(prev_voice_top.pitch_space - prev_voice_top.note.note_above.pitch_space) / const.MAX_PITCH_DISTANCE if prev_voice_top and prev_voice_top.note.note_above else 1; j += 1

    prev_voice_top2 = prev_voice_top.left[0] if prev_voice_top and len(prev_voice_top.left) > 0 else None
    all_voice_data[i, j] = abs(prev_voice_top.pitch_space - prev_voice_top2.pitch_space) / const.MAX_PITCH_DISTANCE if prev_voice_top and prev_voice_top2 else 1; j += 1
    all_voice_data[i, j] = prev_voice_top.pitch_space < prev_voice_top2.pitch_space if prev_voice_top and prev_voice_top2 else 0; j += 1
    all_voice_data[i, j] = prev_voice_top.pitch_space > prev_voice_top2.pitch_space if prev_voice_top and prev_voice_top2 else 0; j += 1
    all_voice_data[i, j] = prev_voice_top.pitch_space == prev_voice_top2.pitch_space if prev_voice_top and prev_voice_top2 else 0; j += 1

    all_voice_data[i, j] = abs(prev_voice_top2.pitch_space - prev_voice_top2.note.note_above.pitch_space) / const.MAX_PITCH_DISTANCE if prev_voice_top2 and prev_voice_top2.note.note_above else 1; j += 1

    prev_voice_top3 = prev_voice_top2.left[0] if prev_voice_top2 and len(prev_voice_top2.left) > 0 else None
    all_voice_data[i, j] = abs(prev_voice_top2.pitch_space - prev_voice_top3.pitch_space) / const.MAX_PITCH_DISTANCE if prev_voice_top2 and prev_voice_top3 else 1; j += 1
    all_voice_data[i, j] = prev_voice_top2.pitch_space < prev_voice_top3.pitch_space if prev_voice_top2 and prev_voice_top3 else 0; j += 1
    all_voice_data[i, j] = prev_voice_top2.pitch_space > prev_voice_top3.pitch_space if prev_voice_top2 and prev_voice_top3 else 0; j += 1
    all_voice_data[i, j] = prev_voice_top2.pitch_space == prev_voice_top3.pitch_space if prev_voice_top2 and prev_voice_top3 else 0; j += 1

    all_voice_data[i, j] = abs(prev_voice_top3.pitch_space - prev_voice_top3.note.note_above.pitch_space) / const.MAX_PITCH_DISTANCE if prev_voice_top3 and prev_voice_top3.note.note_above else 1; j += 1

    len_left = len(voice.left)
    prev_voice_bottom = voice.left[len_left-1] if len(voice.left) > 0 else None
    all_voice_data[i, j] = abs(voice.pitch_space - prev_voice_bottom.pitch_space) / const.MAX_PITCH_DISTANCE if prev_voice_bottom else 1; j += 1
    all_voice_data[i, j] = voice.pitch_space < prev_voice_bottom.pitch_space if prev_voice_bottom else 0; j += 1
    all_voice_data[i, j] = voice.pitch_space > prev_voice_bottom.pitch_space if prev_voice_bottom else 0; j += 1
    all_voice_data[i, j] = voice.pitch_space == prev_voice_bottom.pitch_space if prev_voice_bottom else 0; j += 1

    all_voice_data[i, j] = abs(prev_voice_bottom.pitch_space - prev_voice_bottom.note.note_below.pitch_space) / const.MAX_PITCH_DISTANCE if prev_voice_bottom and prev_voice_bottom.note.note_below else 1; j += 1

    len_left = len(prev_voice_bottom.left) if prev_voice_bottom else 0 
    prev_voice_bottom2 = prev_voice_bottom.left[len_left-1] if prev_voice_bottom and len(prev_voice_bottom.left) > 0 else None
    all_voice_data[i, j] = abs(prev_voice_bottom.pitch_space - prev_voice_bottom2.pitch_space) / const.MAX_PITCH_DISTANCE if prev_voice_bottom and prev_voice_bottom2 else 1; j += 1
    all_voice_data[i, j] = prev_voice_bottom.pitch_space < prev_voice_bottom2.pitch_space if prev_voice_bottom and prev_voice_bottom2 else 0; j += 1
    all_voice_data[i, j] = prev_voice_bottom.pitch_space > prev_voice_bottom2.pitch_space if prev_voice_bottom and prev_voice_bottom2 else 0; j += 1
    all_voice_data[i, j] = prev_voice_bottom.pitch_space == prev_voice_bottom2.pitch_space if prev_voice_bottom and prev_voice_bottom2 else 0; j += 1

    all_voice_data[i, j] = abs(prev_voice_bottom2.pitch_space - prev_voice_bottom2.note.note_below.pitch_space) / const.MAX_PITCH_DISTANCE if prev_voice_bottom2 and prev_voice_bottom2.note.note_below else 1; j += 1

    len_left = len(prev_voice_bottom2.left) if prev_voice_bottom2 else 0 
    prev_voice_bottom3 = prev_voice_bottom2.left[len_left-1] if prev_voice_bottom2 and len(prev_voice_bottom2.left) > 0 else None
    all_voice_data[i, j] = abs(prev_voice_bottom2.pitch_space - prev_voice_bottom3.pitch_space) / const.MAX_PITCH_DISTANCE if prev_voice_bottom2 and prev_voice_bottom3 else 1; j += 1
    all_voice_data[i, j] = prev_voice_bottom2.pitch_space < prev_voice_bottom3.pitch_space if prev_voice_bottom2 and prev_voice_bottom3 else 0; j += 1
    all_voice_data[i, j] = prev_voice_bottom2.pitch_space > prev_voice_bottom3.pitch_space if prev_voice_bottom2 and prev_voice_bottom3 else 0; j += 1
    all_voice_data[i, j] = prev_voice_bottom2.pitch_space == prev_voice_bottom3.pitch_space if prev_voice_bottom2 and prev_voice_bottom3 else 0; j += 1

    all_voice_data[i, j] = abs(prev_voice_bottom3.pitch_space - prev_voice_bottom3.note.note_below.pitch_space) / const.MAX_PITCH_DISTANCE if prev_voice_bottom3 and prev_voice_bottom3.note.note_below else 1; j += 1

    all_voice_data[i, j] = voice.blocked; j += 1

    # Div note distance
    # all_voice_data[i, j] = 1 if len(voice.pairs.rightvoice.min_pitch_space < 40; j += 1
    all_voice_data[i, j] = voice.div_count == 0; j += 1
    all_voice_data[i, j] = voice.div_count == 1; j += 1
    all_voice_data[i, j] = voice.div_count == 2; j += 1
    all_voice_data[i, j] = voice.div_count == 3; j += 1

    # Temporal
    all_voice_data[i, j] = voice.note.beat_duration >= 4; j += 1
    all_voice_data[i, j] = voice.note.beat_duration >= 3 and voice.note.beat_duration < 4; j += 1
    all_voice_data[i, j] = voice.note.beat_duration >= 2 and voice.note.beat_duration < 3; j += 1
    all_voice_data[i, j] = voice.note.beat_duration >= 1.75 and voice.note.beat_duration < 2; j += 1
    all_voice_data[i, j] = voice.note.beat_duration >= 1.5 and voice.note.beat_duration < 1.75; j += 1
    all_voice_data[i, j] = voice.note.beat_duration >= 1.25 and voice.note.beat_duration < 1.5; j += 1
    all_voice_data[i, j] = voice.note.beat_duration >= 1 and voice.note.beat_duration < 1.25; j += 1
    all_voice_data[i, j] = voice.note.beat_duration >= 0.875 and voice.note.beat_duration < 1; j += 1
    all_voice_data[i, j] = voice.note.beat_duration >= 0.75 and voice.note.beat_duration < 0.875; j += 1
    all_voice_data[i, j] = voice.note.beat_duration >= 0.625 and voice.note.beat_duration < 0.75; j += 1
    all_voice_data[i, j] = voice.note.beat_duration >= 0.5 and voice.note.beat_duration < 0.625; j += 1
    all_voice_data[i, j] = voice.note.beat_duration >= 0.375 and voice.note.beat_duration < 0.5; j += 1
    all_voice_data[i, j] = voice.note.beat_duration >= 0.25 and voice.note.beat_duration < 0.375; j += 1
    all_voice_data[i, j] = voice.note.beat_duration >= 0.125 and voice.note.beat_duration < 0.25; j += 1
    all_voice_data[i, j] = voice.note.beat_duration < 0.125; j += 1

    all_voice_data[i, j] = voice.rest_count_top == 0; j += 1
    all_voice_data[i, j] = voice.rest_count_top == 1; j += 1
    all_voice_data[i, j] = voice.rest_count_top == 2; j += 1
    all_voice_data[i, j] = voice.rest_count_top == 3; j += 1
    all_voice_data[i, j] = voice.rest_count_top == 4; j += 1
    all_voice_data[i, j] = voice.rest_count_top == 5; j += 1
    all_voice_data[i, j] = voice.rest_count_top > 5; j += 1

    all_voice_data[i, j] = voice.rest_count_bottom == 0; j += 1
    all_voice_data[i, j] = voice.rest_count_bottom == 1; j += 1
    all_voice_data[i, j] = voice.rest_count_bottom == 2; j += 1
    all_voice_data[i, j] = voice.rest_count_bottom == 3; j += 1
    all_voice_data[i, j] = voice.rest_count_bottom == 4; j += 1
    all_voice_data[i, j] = voice.rest_count_bottom == 5; j += 1
    all_voice_data[i, j] = voice.rest_count_bottom > 5; j += 1

    all_voice_data[i, j] = voice.dur_diff_count_above == 0; j += 1
    all_voice_data[i, j] = voice.dur_diff_count_above == 1; j += 1
    all_voice_data[i, j] = voice.dur_diff_count_above == 2; j += 1
    all_voice_data[i, j] = voice.dur_diff_count_above == 3; j += 1
    all_voice_data[i, j] = voice.dur_diff_count_above == 4; j += 1
    all_voice_data[i, j] = voice.dur_diff_count_above == 5; j += 1
    all_voice_data[i, j] = voice.dur_diff_count_above > 5; j += 1

    all_voice_data[i, j] = voice.dur_diff_count_below == 0; j += 1
    all_voice_data[i, j] = voice.dur_diff_count_below == 1; j += 1
    all_voice_data[i, j] = voice.dur_diff_count_below == 2; j += 1
    all_voice_data[i, j] = voice.dur_diff_count_below == 3; j += 1
    all_voice_data[i, j] = voice.dur_diff_count_below == 4; j += 1
    all_voice_data[i, j] = voice.dur_diff_count_below == 5; j += 1
    all_voice_data[i, j] = voice.dur_diff_count_below > 5; j += 1

    # Note above and below
    all_voice_data[i, j] = abs(float(voice.note.beat_duration - voice.note.note_above.beat_duration)) / const.MAX_BEAT_DUR_DISTANCE if voice.note.note_above else 1; j += 1
    all_voice_data[i, j] = voice.note.beat_duration < voice.note.note_above.beat_duration if voice.note.note_above else 0; j += 1
    all_voice_data[i, j] = voice.note.beat_duration > voice.note.note_above.beat_duration if voice.note.note_above else 0; j += 1
    all_voice_data[i, j] = voice.note.beat_duration == voice.note.note_above.beat_duration if voice.note.note_above else 0; j += 1

    all_voice_data[i, j] = abs(float(voice.note.beat_duration - voice.note.note_below.beat_duration)) / const.MAX_BEAT_DUR_DISTANCE if voice.note.note_below else 1; j += 1
    all_voice_data[i, j] = voice.note.beat_duration < voice.note.note_below.beat_duration if voice.note.note_below else 0; j += 1
    all_voice_data[i, j] = voice.note.beat_duration > voice.note.note_below.beat_duration if voice.note.note_below else 0; j += 1
    all_voice_data[i, j] = voice.note.beat_duration == voice.note.note_below.beat_duration if voice.note.note_below else 0; j += 1

    # Voice above and below
    all_voice_data[i, j] = abs(float(voice.note.beat_duration - voice.voice_above.note.beat_duration)) / const.MAX_BEAT_DUR_DISTANCE if voice.voice_above else 1; j += 1
    all_voice_data[i, j] = voice.note.beat_duration < voice.voice_above.note.beat_duration if voice.voice_above else 0; j += 1
    all_voice_data[i, j] = voice.note.beat_duration > voice.voice_above.note.beat_duration if voice.voice_above else 0; j += 1
    all_voice_data[i, j] = voice.note.beat_duration == voice.voice_above.note.beat_duration if voice.voice_above else 0; j += 1

    all_voice_data[i, j] = abs(float(voice.note.beat_duration - voice.voice_below.note.beat_duration)) / const.MAX_BEAT_DUR_DISTANCE if voice.voice_below else 1; j += 1
    all_voice_data[i, j] = voice.note.beat_duration < voice.voice_below.note.beat_duration if voice.voice_below else 0; j += 1
    all_voice_data[i, j] = voice.note.beat_duration > voice.voice_below.note.beat_duration if voice.voice_below else 0; j += 1
    all_voice_data[i, j] = voice.note.beat_duration == voice.voice_below.note.beat_duration if voice.voice_below else 0; j += 1

    # Last
    all_voice_data[i, j] = abs(float(voice.note.beat_duration - voice.last_above.note.beat_duration)) / const.MAX_BEAT_DUR_DISTANCE if voice.last_above else 1; j += 1
    all_voice_data[i, j] = voice.note.beat_duration < voice.last_above.note.beat_duration if voice.last_above else 0; j += 1
    all_voice_data[i, j] = voice.note.beat_duration > voice.last_above.note.beat_duration if voice.last_above else 0; j += 1
    all_voice_data[i, j] = voice.note.beat_duration == voice.last_above.note.beat_duration if voice.last_above else 0; j += 1

    all_voice_data[i, j] = abs(float(voice.note.beat_duration - voice.last_below.note.beat_duration)) / const.MAX_BEAT_DUR_DISTANCE if voice.last_below else 1; j += 1
    all_voice_data[i, j] = voice.note.beat_duration < voice.last_below.note.beat_duration if voice.last_below else 0; j += 1
    all_voice_data[i, j] = voice.note.beat_duration > voice.last_below.note.beat_duration if voice.last_below else 0; j += 1
    all_voice_data[i, j] = voice.note.beat_duration == voice.last_below.note.beat_duration if voice.last_below else 0; j += 1

    # Prev
    all_voice_data[i, j] = max(float(voice.note.beat_onset - prev_voice_top.note.beat_onset), 0) / const.MAX_BEAT_ONSET_DISTANCE if prev_voice_top else 1; j += 1
    all_voice_data[i, j] = voice.note.beat_onset < prev_voice_top.note.beat_onset if prev_voice_top else 0; j += 1
    all_voice_data[i, j] = voice.note.beat_onset > prev_voice_top.note.beat_onset if prev_voice_top else 0; j += 1
    all_voice_data[i, j] = voice.note.beat_onset == prev_voice_top.note.beat_onset if prev_voice_top else 0; j += 1

    all_voice_data[i, j] = max(float(voice.note.beat_onset - prev_voice_top.note.beat_offset), 0) / const.MAX_BEAT_ONSET_OFFSET if prev_voice_top else 1; j += 1
    all_voice_data[i, j] = voice.note.beat_onset < prev_voice_top.note.beat_offset if prev_voice_top else 0; j += 1
    all_voice_data[i, j] = voice.note.beat_onset > prev_voice_top.note.beat_offset if prev_voice_top else 0; j += 1
    all_voice_data[i, j] = voice.note.beat_onset == prev_voice_top.note.beat_offset if prev_voice_top else 0; j += 1

    all_voice_data[i, j] = max(float(prev_voice_top.note.beat_onset - prev_voice_top2.note.beat_onset), 0) / const.MAX_BEAT_ONSET_DISTANCE if prev_voice_top and prev_voice_top2 else 1; j += 1
    all_voice_data[i, j] = prev_voice_top.note.beat_onset < prev_voice_top2.note.beat_onset if prev_voice_top and prev_voice_top2 else 0; j += 1
    all_voice_data[i, j] = prev_voice_top.note.beat_onset > prev_voice_top2.note.beat_onset if prev_voice_top and prev_voice_top2 else 0; j += 1
    all_voice_data[i, j] = prev_voice_top.note.beat_onset == prev_voice_top2.note.beat_onset if prev_voice_top and prev_voice_top2 else 0; j += 1

    all_voice_data[i, j] = max(float(prev_voice_top.note.beat_onset - prev_voice_top2.note.beat_offset), 0) / const.MAX_BEAT_ONSET_OFFSET if prev_voice_top and prev_voice_top2 else 1; j += 1
    all_voice_data[i, j] = prev_voice_top.note.beat_onset < prev_voice_top2.note.beat_offset if prev_voice_top and prev_voice_top2 else 0; j += 1
    all_voice_data[i, j] = prev_voice_top.note.beat_onset > prev_voice_top2.note.beat_offset if prev_voice_top and prev_voice_top2 else 0; j += 1
    all_voice_data[i, j] = prev_voice_top.note.beat_onset == prev_voice_top2.note.beat_offset if prev_voice_top and prev_voice_top2 else 0; j += 1

    all_voice_data[i, j] = max(float(prev_voice_top2.note.beat_onset - prev_voice_top3.note.beat_onset), 0) / const.MAX_BEAT_ONSET_DISTANCE if prev_voice_top2 and prev_voice_top3 else 1; j += 1
    all_voice_data[i, j] = prev_voice_top2.note.beat_onset < prev_voice_top3.note.beat_onset if prev_voice_top2 and prev_voice_top3 else 0; j += 1
    all_voice_data[i, j] = prev_voice_top2.note.beat_onset > prev_voice_top3.note.beat_onset if prev_voice_top2 and prev_voice_top3 else 0; j += 1
    all_voice_data[i, j] = prev_voice_top2.note.beat_onset == prev_voice_top3.note.beat_onset if prev_voice_top2 and prev_voice_top3 else 0; j += 1

    all_voice_data[i, j] = max(float(prev_voice_top2.note.beat_onset - prev_voice_top3.note.beat_offset), 0) / const.MAX_BEAT_ONSET_OFFSET if prev_voice_top2 and prev_voice_top3 else 1; j += 1
    all_voice_data[i, j] = prev_voice_top2.note.beat_onset < prev_voice_top3.note.beat_offset if prev_voice_top2 and prev_voice_top3 else 0; j += 1
    all_voice_data[i, j] = prev_voice_top2.note.beat_onset > prev_voice_top3.note.beat_offset if prev_voice_top2 and prev_voice_top3 else 0; j += 1
    all_voice_data[i, j] = prev_voice_top2.note.beat_onset == prev_voice_top3.note.beat_offset if prev_voice_top2 and prev_voice_top3 else 0; j += 1

    all_voice_data[i, j] = max(float(voice.note.beat_onset - prev_voice_bottom.note.beat_onset), 0) / const.MAX_BEAT_ONSET_DISTANCE if prev_voice_bottom else 1; j += 1
    all_voice_data[i, j] = voice.note.beat_onset < prev_voice_bottom.note.beat_onset if prev_voice_bottom else 0; j += 1
    all_voice_data[i, j] = voice.note.beat_onset > prev_voice_bottom.note.beat_onset if prev_voice_bottom else 0; j += 1
    all_voice_data[i, j] = voice.note.beat_onset == prev_voice_bottom.note.beat_onset if prev_voice_bottom else 0; j += 1

    all_voice_data[i, j] = max(float(voice.note.beat_onset - prev_voice_bottom.note.beat_offset), 0) / const.MAX_BEAT_ONSET_OFFSET if prev_voice_bottom else 1; j += 1
    all_voice_data[i, j] = voice.note.beat_onset < prev_voice_bottom.note.beat_offset if prev_voice_bottom else 0; j += 1
    all_voice_data[i, j] = voice.note.beat_onset > prev_voice_bottom.note.beat_offset if prev_voice_bottom else 0; j += 1
    all_voice_data[i, j] = voice.note.beat_onset == prev_voice_bottom.note.beat_offset if prev_voice_bottom else 0; j += 1

    all_voice_data[i, j] = max(float(prev_voice_bottom.note.beat_onset - prev_voice_bottom2.note.beat_onset), 0) / const.MAX_BEAT_ONSET_DISTANCE if prev_voice_bottom and prev_voice_bottom2 else 1; j += 1
    all_voice_data[i, j] = prev_voice_bottom.note.beat_onset < prev_voice_bottom2.note.beat_onset if prev_voice_bottom and prev_voice_bottom2 else 0; j += 1
    all_voice_data[i, j] = prev_voice_bottom.note.beat_onset > prev_voice_bottom2.note.beat_onset if prev_voice_bottom and prev_voice_bottom2 else 0; j += 1
    all_voice_data[i, j] = prev_voice_bottom.note.beat_onset == prev_voice_bottom2.note.beat_onset if prev_voice_bottom and prev_voice_bottom2 else 0; j += 1

    all_voice_data[i, j] = max(float(prev_voice_bottom.note.beat_onset - prev_voice_bottom2.note.beat_offset), 0) / const.MAX_BEAT_ONSET_OFFSET if prev_voice_bottom and prev_voice_bottom2 else 1; j += 1
    all_voice_data[i, j] = prev_voice_bottom.note.beat_onset < prev_voice_bottom2.note.beat_offset if prev_voice_bottom and prev_voice_bottom2 else 0; j += 1
    all_voice_data[i, j] = prev_voice_bottom.note.beat_onset > prev_voice_bottom2.note.beat_offset if prev_voice_bottom and prev_voice_bottom2 else 0; j += 1
    all_voice_data[i, j] = prev_voice_bottom.note.beat_onset == prev_voice_bottom2.note.beat_offset if prev_voice_bottom and prev_voice_bottom2 else 0; j += 1

    all_voice_data[i, j] = max(float(prev_voice_bottom2.note.beat_onset - prev_voice_bottom3.note.beat_onset), 0) / const.MAX_BEAT_ONSET_DISTANCE if prev_voice_bottom2 and prev_voice_bottom3 else 1; j += 1
    all_voice_data[i, j] = prev_voice_bottom2.note.beat_onset < prev_voice_bottom3.note.beat_onset if prev_voice_bottom2 and prev_voice_bottom3 else 0; j += 1
    all_voice_data[i, j] = prev_voice_bottom2.note.beat_onset > prev_voice_bottom3.note.beat_onset if prev_voice_bottom2 and prev_voice_bottom3 else 0; j += 1
    all_voice_data[i, j] = prev_voice_bottom2.note.beat_onset == prev_voice_bottom3.note.beat_onset if prev_voice_bottom2 and prev_voice_bottom3 else 0; j += 1

    all_voice_data[i, j] = max(float(prev_voice_bottom2.note.beat_onset - prev_voice_bottom3.note.beat_offset), 0) / const.MAX_BEAT_ONSET_OFFSET if prev_voice_bottom2 and prev_voice_bottom3 else 1; j += 1
    all_voice_data[i, j] = prev_voice_bottom2.note.beat_onset < prev_voice_bottom3.note.beat_offset if prev_voice_bottom2 and prev_voice_bottom3 else 0; j += 1
    all_voice_data[i, j] = prev_voice_bottom2.note.beat_onset > prev_voice_bottom3.note.beat_offset if prev_voice_bottom2 and prev_voice_bottom3 else 0; j += 1
    all_voice_data[i, j] = prev_voice_bottom2.note.beat_onset == prev_voice_bottom3.note.beat_offset if prev_voice_bottom2 and prev_voice_bottom3 else 0; j += 1
   
    # Positional
    all_voice_data[i, j] = prev_voice_top is None; j += 1
    all_voice_data[i, j] = prev_voice_top2 is None; j += 1
    all_voice_data[i, j] = prev_voice_top3 is None; j += 1

    all_voice_data[i, j] = prev_voice_bottom is None; j += 1
    all_voice_data[i, j] = prev_voice_bottom2 is None; j += 1
    all_voice_data[i, j] = prev_voice_bottom3 is None; j += 1

    all_voice_data[i, j] = voice.note.note_above is None; j += 1
    all_voice_data[i, j] = voice.note.note_below is None; j += 1

    all_voice_data[i, j] = voice.voice_above is None; j += 1
    all_voice_data[i, j] = voice.voice_below is None; j += 1

    all_voice_data[i, j] = voice.last_above is None; j += 1
    all_voice_data[i, j] = voice.last_below is None; j += 1

    all_voice_data[i, j] = voice.last_above is not voice.voice_above and voice.nv_above is not voice.last_above and voice.nv_above is not voice.voice_above; j += 1
    all_voice_data[i, j] = voice.nv_above is voice.voice_above and voice.nv_above is voice.last_above; j += 1
    all_voice_data[i, j] = voice.nv_above is voice.voice_above and voice.nv_above is not voice.last_above; j += 1
    all_voice_data[i, j] = voice.last_above is not voice.voice_above and voice.nv_above is voice.last_above; j += 1
    all_voice_data[i, j] = voice.last_above is voice.voice_above and voice.nv_above is not voice.last_above; j += 1

    all_voice_data[i, j] = voice.last_below is not voice.voice_below and voice.nv_below is not voice.last_below and voice.nv_below is not voice.voice_below; j += 1
    all_voice_data[i, j] = voice.nv_below is voice.voice_below and voice.nv_below is voice.last_below; j += 1
    all_voice_data[i, j] = voice.nv_below is voice.voice_below and voice.nv_below is not voice.last_below; j += 1
    all_voice_data[i, j] = voice.last_below is not voice.voice_below and voice.nv_below is voice.last_below; j += 1
    all_voice_data[i, j] = voice.last_below is voice.voice_below and voice.nv_below is not voice.last_below; j += 1

    all_voice_data[i, j] = voice.note.index == 0; j += 1
    all_voice_data[i, j] = voice.note.index == 1; j += 1
    all_voice_data[i, j] = voice.note.index == 2; j += 1
    all_voice_data[i, j] = voice.note.index == 3; j += 1
    all_voice_data[i, j] = voice.note.index == 4; j += 1
    all_voice_data[i, j] = voice.note.index == 5; j += 1
    all_voice_data[i, j] = voice.note.index == 6; j += 1
    all_voice_data[i, j] = voice.note.index == 7; j += 1

    all_voice_data[i, j] = voice.subset_index == 0; j += 1
    all_voice_data[i, j] = voice.subset_index == 1; j += 1
    all_voice_data[i, j] = voice.subset_index == 2; j += 1
    all_voice_data[i, j] = voice.subset_index == 3; j += 1
    all_voice_data[i, j] = voice.subset_index == 4; j += 1
    all_voice_data[i, j] = voice.subset_index == 5; j += 1
    all_voice_data[i, j] = voice.subset_index == 6; j += 1
    all_voice_data[i, j] = voice.subset_index == 7; j += 1
    all_voice_data[i, j] = voice.subset_index == 8; j += 1
    all_voice_data[i, j] = voice.subset_index == 9; j += 1
    all_voice_data[i, j] = voice.subset_index == 10; j += 1
    all_voice_data[i, j] = voice.subset_index == 11; j += 1
    all_voice_data[i, j] = voice.subset_index == 12; j += 1
    all_voice_data[i, j] = voice.subset_index == 13; j += 1
    all_voice_data[i, j] = voice.subset_index == 14; j += 1

    all_voice_data[i, j] = voice.last_index == 0; j += 1
    all_voice_data[i, j] = voice.last_index == 0.5; j += 1
    all_voice_data[i, j] = voice.last_index == 1; j += 1
    all_voice_data[i, j] = voice.last_index == 1.5; j += 1
    all_voice_data[i, j] = voice.last_index == 2; j += 1
    all_voice_data[i, j] = voice.last_index == 2.5; j += 1
    all_voice_data[i, j] = voice.last_index == 3; j += 1
    all_voice_data[i, j] = voice.last_index == 3.5; j += 1
    all_voice_data[i, j] = voice.last_index == 4; j += 1
    all_voice_data[i, j] = voice.last_index == 4.5; j += 1
    all_voice_data[i, j] = voice.last_index == 5; j += 1
    all_voice_data[i, j] = voice.last_index == 5.5; j += 1
    all_voice_data[i, j] = voice.last_index == 6; j += 1
    all_voice_data[i, j] = voice.last_index == 6.5; j += 1
    all_voice_data[i, j] = voice.last_index == 7; j += 1
    all_voice_data[i, j] = voice.last_index == 7.5; j += 1
    all_voice_data[i, j] = voice.last_index == 8; j += 1
    all_voice_data[i, j] = voice.last_index == 8.5; j += 1
    all_voice_data[i, j] = voice.last_index == 9; j += 1
    all_voice_data[i, j] = voice.last_index == 9.5; j += 1
    all_voice_data[i, j] = voice.last_index == 10; j += 1

    all_voice_data[i, j] = voice.note.chord_length == 1; j += 1
    all_voice_data[i, j] = voice.note.chord_length == 2; j += 1
    all_voice_data[i, j] = voice.note.chord_length == 3; j += 1
    all_voice_data[i, j] = voice.note.chord_length == 4; j += 1
    all_voice_data[i, j] = voice.note.chord_length == 5; j += 1
    all_voice_data[i, j] = voice.note.chord_length == 6; j += 1
    all_voice_data[i, j] = voice.note.chord_length == 7; j += 1
    all_voice_data[i, j] = voice.note.chord_length == 8; j += 1

    all_voice_data[i, j] = voice.subset_length == 1; j += 1
    all_voice_data[i, j] = voice.subset_length == 2; j += 1
    all_voice_data[i, j] = voice.subset_length == 3; j += 1
    all_voice_data[i, j] = voice.subset_length == 4; j += 1
    all_voice_data[i, j] = voice.subset_length == 5; j += 1
    all_voice_data[i, j] = voice.subset_length == 6; j += 1
    all_voice_data[i, j] = voice.subset_length == 7; j += 1
    all_voice_data[i, j] = voice.subset_length == 8; j += 1
    all_voice_data[i, j] = voice.subset_length == 9; j += 1
    all_voice_data[i, j] = voice.subset_length == 10; j += 1
    all_voice_data[i, j] = voice.subset_length == 11; j += 1
    all_voice_data[i, j] = voice.subset_length == 12; j += 1
    all_voice_data[i, j] = voice.subset_length == 13; j += 1
    all_voice_data[i, j] = voice.subset_length == 14; j += 1
    all_voice_data[i, j] = voice.subset_length == 15; j += 1

    all_voice_data[i, j] = voice.last_length == 1; j += 1
    all_voice_data[i, j] = voice.last_length == 2; j += 1
    all_voice_data[i, j] = voice.last_length == 3; j += 1
    all_voice_data[i, j] = voice.last_length == 4; j += 1
    all_voice_data[i, j] = voice.last_length == 5; j += 1
    all_voice_data[i, j] = voice.last_length == 6; j += 1
    all_voice_data[i, j] = voice.last_length == 7; j += 1
    all_voice_data[i, j] = voice.last_length == 8; j += 1
    all_voice_data[i, j] = voice.last_length == 9; j += 1
    all_voice_data[i, j] = voice.last_length == 10; j += 1
    all_voice_data[i, j] = voice.last_length == 11; j += 1

    all_voice_data[i, j] = prev_voice_top.note.index == 0 if prev_voice_top else 0; j += 1
    all_voice_data[i, j] = prev_voice_top.note.index > 0 and prev_voice_top.note.index < prev_voice_top.note.chord_length - 1 if prev_voice_top else 0; j += 1
    all_voice_data[i, j] = prev_voice_top.note.index == prev_voice_top.note.chord_length - 1 if prev_voice_top else 0; j += 1

    all_voice_data[i, j] = prev_voice_top2.note.index == 0 if prev_voice_top2 else 0; j += 1
    all_voice_data[i, j] = prev_voice_top2.note.index > 0 and prev_voice_top2.note.index < prev_voice_top2.note.chord_length - 1 if prev_voice_top2 else 0; j += 1
    all_voice_data[i, j] = prev_voice_top2.note.index == prev_voice_top2.note.chord_length - 1 if prev_voice_top2 else 0; j += 1

    all_voice_data[i, j] = prev_voice_top3.note.index == 0 if prev_voice_top3 else 0; j += 1
    all_voice_data[i, j] = prev_voice_top3.note.index > 0 and prev_voice_top3.note.index < prev_voice_top3.note.chord_length - 1 if prev_voice_top3 else 0; j += 1
    all_voice_data[i, j] = prev_voice_top3.note.index == prev_voice_top3.note.chord_length - 1 if prev_voice_top3 else 0; j += 1

    all_voice_data[i, j] = prev_voice_bottom.note.index == 0 if prev_voice_bottom else 0; j += 1
    all_voice_data[i, j] = prev_voice_bottom.note.index > 0 and prev_voice_bottom.note.index < prev_voice_bottom.note.chord_length - 1 if prev_voice_bottom else 0; j += 1
    all_voice_data[i, j] = prev_voice_bottom.note.index == prev_voice_bottom.note.chord_length - 1 if prev_voice_bottom else 0; j += 1

    all_voice_data[i, j] = prev_voice_bottom2.note.index == 0 if prev_voice_bottom2 else 0; j += 1
    all_voice_data[i, j] = prev_voice_bottom2.note.index > 0 and prev_voice_bottom2.note.index < prev_voice_bottom2.note.chord_length - 1 if prev_voice_bottom2 else 0; j += 1
    all_voice_data[i, j] = prev_voice_bottom2.note.index == prev_voice_bottom2.note.chord_length - 1 if prev_voice_bottom2 else 0; j += 1

    all_voice_data[i, j] = prev_voice_bottom3.note.index == 0 if prev_voice_bottom3 else 0; j += 1
    all_voice_data[i, j] = prev_voice_bottom3.note.index > 0 and prev_voice_bottom3.note.index < prev_voice_bottom3.note.chord_length - 1 if prev_voice_bottom3 else 0; j += 1
    all_voice_data[i, j] = prev_voice_bottom3.note.index == prev_voice_bottom3.note.chord_length - 1 if prev_voice_bottom3 else 0; j += 1
   
    all_voice_data[i, j] = voice.length_top == 1; j += 1
    all_voice_data[i, j] = voice.length_top == 2; j += 1
    all_voice_data[i, j] = voice.length_top == 3; j += 1
    all_voice_data[i, j] = voice.length_top == 4; j += 1
    all_voice_data[i, j] = voice.length_top == 5; j += 1
    all_voice_data[i, j] = voice.length_top == 6; j += 1
    all_voice_data[i, j] = voice.length_top == 7; j += 1
    all_voice_data[i, j] = voice.length_top == 8; j += 1
    all_voice_data[i, j] = voice.length_top == 9; j += 1
    all_voice_data[i, j] = voice.length_top == 10; j += 1
    
    all_voice_data[i, j] = voice.length_bottom == 1; j += 1
    all_voice_data[i, j] = voice.length_bottom == 2; j += 1
    all_voice_data[i, j] = voice.length_bottom == 3; j += 1
    all_voice_data[i, j] = voice.length_bottom == 4; j += 1
    all_voice_data[i, j] = voice.length_bottom == 5; j += 1
    all_voice_data[i, j] = voice.length_bottom == 6; j += 1
    all_voice_data[i, j] = voice.length_bottom == 7; j += 1
    all_voice_data[i, j] = voice.length_bottom == 8; j += 1
    all_voice_data[i, j] = voice.length_bottom == 9; j += 1
    all_voice_data[i, j] = voice.length_bottom == 10; j += 1

    all_voice_data[i, j] = voice.position == 0; j += 1
    all_voice_data[i, j] = voice.position == 1; j += 1
    all_voice_data[i, j] = voice.position == 2; j += 1
    all_voice_data[i, j] = voice.position == 3; j += 1
    all_voice_data[i, j] = voice.position == 4; j += 1
    all_voice_data[i, j] = voice.position == 5; j += 1
    all_voice_data[i, j] = voice.position == 6; j += 1
    all_voice_data[i, j] = voice.position == 7; j += 1
    all_voice_data[i, j] = voice.position == 8; j += 1
    all_voice_data[i, j] = voice.position > 8; j += 1

    all_voice_data[i, j] = voice.note_count == 1; j += 1
    all_voice_data[i, j] = voice.note_count == 2; j += 1
    all_voice_data[i, j] = voice.note_count == 3; j += 1
    all_voice_data[i, j] = voice.note_count == 4; j += 1
    all_voice_data[i, j] = voice.note_count == 5; j += 1
    all_voice_data[i, j] = voice.note_count == 6; j += 1
    all_voice_data[i, j] = voice.note_count == 7; j += 1
    all_voice_data[i, j] = voice.note_count == 8; j += 1
    all_voice_data[i, j] = voice.note_count == 9; j += 1
    all_voice_data[i, j] = voice.note_count == 10; j += 1
    all_voice_data[i, j] = voice.note_count == 11; j += 1
    all_voice_data[i, j] = voice.note_count == 12; j += 1


    # Tonal
    all_voice_data[i, j] = voice.note.degree == 1; j += 1
    all_voice_data[i, j] = voice.note.degree == 2; j += 1
    all_voice_data[i, j] = voice.note.degree == 3; j += 1
    all_voice_data[i, j] = voice.note.degree == 4; j += 1
    all_voice_data[i, j] = voice.note.degree == 5; j += 1
    all_voice_data[i, j] = voice.note.degree == 6; j += 1
    all_voice_data[i, j] = voice.note.degree == 7; j += 1

    all_voice_data[i, j] = voice.note.chord_step == 1; j += 1
    all_voice_data[i, j] = voice.note.chord_step == 2; j += 1
    all_voice_data[i, j] = voice.note.chord_step == 3; j += 1
    all_voice_data[i, j] = voice.note.chord_step == 4; j += 1
    all_voice_data[i, j] = voice.note.chord_step == 5; j += 1
    all_voice_data[i, j] = voice.note.chord_step == 6; j += 1
    all_voice_data[i, j] = voice.note.chord_step == 7; j += 1

    # Metrical
    all_voice_data[i, j] = voice.note.beat_strength == 1; j += 1
    all_voice_data[i, j] = voice.note.beat_strength >= 0.9 and voice.note.beat_strength < 1; j += 1
    all_voice_data[i, j] = voice.note.beat_strength >= 0.8 and voice.note.beat_strength < 0.9; j += 1
    all_voice_data[i, j] = voice.note.beat_strength >= 0.7 and voice.note.beat_strength < 0.8; j += 1
    all_voice_data[i, j] = voice.note.beat_strength >= 0.6 and voice.note.beat_strength < 0.7; j += 1
    all_voice_data[i, j] = voice.note.beat_strength >= 0.5 and voice.note.beat_strength < 0.6; j += 1
    all_voice_data[i, j] = voice.note.beat_strength >= 0.4 and voice.note.beat_strength < 0.5; j += 1
    all_voice_data[i, j] = voice.note.beat_strength >= 0.3 and voice.note.beat_strength < 0.4; j += 1
    all_voice_data[i, j] = voice.note.beat_strength >= 0.2 and voice.note.beat_strength < 0.3; j += 1
    all_voice_data[i, j] = voice.note.beat_strength >= 0.1 and voice.note.beat_strength < 0.2; j += 1
    all_voice_data[i, j] = voice.note.beat_strength < 0.1; j += 1


  all_voice_data[len_active_subset, :] = 0

  if j > 0:
    assert j == COUNT, j
