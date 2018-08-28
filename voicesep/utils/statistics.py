class Statistics:
  def __init__(self, stats_file, header, voiceid_type):
    self.fp = open("%s.dat" % stats_file, "a")
    self.fp.write("%s\n" % header)
    # self.fp.write(
    #   "\n Score, # Notes, # Onsets, Synchronicity, # Voices, # N/V, # Pairs, "
    #   "# o2o, # o2m\n"
    #   # "# pairs0, # rests0, # pairs1, # rests1, # pairsn, # restsn, "
    #   # "# cross\n"
    # )
    self.fp.write(
      "\n Score, Lookback, Beat Horizon, Conv,  Div, Cross\n"
    )

    self.voiceid_type = voiceid_type
    self.score_results = []

  def __del__(self):
    self.fp.close()

  def close(self):
    self.fp.close()

  def update(self, score, active_voices):
    # num_notes = sum(len(chord) for chord in score)
    # num_onsets = len(score)
    # color_dict = {}
    # for chord in score:
    #   for note in chord:
    #     if note.true_color in color_dict:
    #       color_dict[note.true_color] += 1
    #     else:
    #       color_dict[note.true_color] = 1
    #
    # num_log_voices = len(color_dict)
    # notes_per_voice = num_notes / len(color_dict)
    # max_notes_per_voice = max(count for _, count in color_dict.items())
    # min_notes_per_voice = min(count for _, count in color_dict.items())
    #
    #
    for chord in score:
      for note in chord:
        if len(note.pairs(self.voiceid_type).left) > 1:
          remove = [False] * len(note.pairs(self.voiceid_type).left)
          for i, pair in enumerate(note.pairs(self.voiceid_type).left):
            if note.beat_onset - pair.beat_offset > 4:
              remove[i] = True
              pair.pairs(self.voiceid_type).right.remove(note)

          note.pairs(self.voiceid_type).left = [p for p, r in zip(note.pairs(self.voiceid_type).left, remove) if not r]

        if len(note.pairs(self.voiceid_type).right) > 1:
          remove = [False] * len(note.pairs(self.voiceid_type).right)
          for i, pair in enumerate(note.pairs(self.voiceid_type).right):
            if pair.beat_onset - note.beat_offset > 4:
              remove[i] = True
              pair.pairs(self.voiceid_type).left.remove(note)

          note.pairs(self.voiceid_type).right = [p for p, r in zip(note.pairs(self.voiceid_type).right, remove) if not r]


    # num_pairs = 0
    # num_o2os = 0
    # num_o2ms = 0
    # for chord in score:
    #   num_pairs += sum(len(note.pairs(self.voiceid_type).left) for note in chord)
    #   num_o2os += sum(
    #     len(note.pairs(self.voiceid_type).left) == 1 and
    #     len(note.pairs(self.voiceid_type).left[0].pairs(self.voiceid_type).right) == 1
    #     for note in chord
    #   )
    #   num_o2ms += sum(
    #     len(note.pairs(self.voiceid_type).left) for note in chord
    #     if len(note.pairs(self.voiceid_type).left) > 1 or
    #     (len(note.pairs(self.voiceid_type).left) == 1 and len(note.pairs(self.voiceid_type).left[0].pairs(self.voiceid_type).right) > 1)
    #   )
    # # num_o2ms = num_pairs - num_o2os
    #
    # synchronicity = num_notes/ num_onsets
    #
    # num_pairs0 = sum(len(chord[0].pairs(self.voiceid_type).left) > 0 for chord in score)
    # num_pairs1 = sum(
    #   len(chord[1].pairs(self.voiceid_type).left) > 0 for chord in score
    #   if len(chord) > 1
    # )
    # num_pairsn = sum(len(chord[-1].pairs(self.voiceid_type).left) > 0 for chord in score)
    # num_rests0 = sum(
    #   chord[0].beat_onset > chord[0].pairs(self.voiceid_type).left[0].beat_offset
    #   for chord in score if len(chord[0].pairs(self.voiceid_type).left) > 0
    # )
    # num_rests1 = sum(
    #   chord[1].beat_onset > chord[1].pairs(self.voiceid_type).left[0].beat_offset
    #   for chord in score if len(chord) > 1 and len(chord[1].pairs(self.voiceid_type).left) > 0
    # )
    # num_restsn = sum(
    #   chord[-1].beat_onset > chord[-1].pairs(self.voiceid_type).left[0].beat_offset
    #   for chord in score if len(chord[-1].pairs(self.voiceid_type).left) > 0
    # )

    lookback_histo = [[0 for _ in range(6)] for _ in range(6)]
    bh_histo = {"[0,1)": 0, "[1,2)": 0, "[2,3)": 0, "[3,4)": 0, "[4,5)": 0, "[5,inf)": 0}
    conv_histo = {}
    div_histo = {}
    cross_count = 0
    # active_voices.voiceid_type = "true"
    # active_voices.beat_horizon = score.beat_horizon
    # active_voices.update(score[0])
    for chord in score:
      # active_voices.filter(chord.beat_onset)
      for iii, note in enumerate(chord):
        right_pairs = note.pairs(self.voiceid_type).right
        pairs = note.pairs(self.voiceid_type).left

        if len(pairs) in conv_histo:
          conv_histo[len(pairs)] += 1
        else:
          conv_histo[len(pairs)] = 1

        if len(right_pairs) in div_histo:
          div_histo[len(right_pairs)] += 1
        else:
          div_histo[len(right_pairs)] = 1

        for pair in pairs:
          bh = max(note.beat_onset - pair.beat_offset, 0)
          if bh >= 0 and bh < 1:
            bh_histo["[0,1)"] += 1
          elif bh >= 1 and bh < 2:
            bh_histo["[1,2)"] += 1
          elif bh >= 2 and bh < 3:
            bh_histo["[2,3)"] += 1
          elif bh >= 3 and bh < 4:
            bh_histo["[3,4)"] += 1
          elif bh >= 4 and bh < 5:
            bh_histo["[4,5)"] += 1
          elif bh >= 5:
            bh_histo["[5,inf)"] += 1

        if len(right_pairs) > 1:
          for pair in right_pairs:
            bh = max(pair.beat_onset - note.beat_offset, 0)
            i = 0
            if bh > 0: # and bh < 2:
              i = 1
            # elif bh >= 2 and bh < 3:
            #   i = 2
            # elif bh >= 3 and bh < 4:
            #   i = 3
            # elif bh >= 4 and bh < 5:
            #   i = 4
            # elif bh >= 5:
            #   i = 5

            pd = abs(pair.pitch_space - note.pitch_space)
            j = 0
            if pd >= 3 and pd < 6:
              j = 1
            elif pd >= 6 and pd < 9:
              j = 2
            elif pd >= 9 and pd < 12:
              j = 3
            elif pd >= 12 and pd < 15:
              j = 4
            elif pd >= 15:
              j = 5

            lookback_histo[i][j] += 1

    #     if len(pairs) == 0:
    #       continue
    #     pairs.sort(key=lambda n: active_voices.index(n))
    #     for note1 in chord[iii+1:]:
    #       pairs1 = note1.pairs(self.voiceid_type).left
    #       if len(pairs1) == 0:
    #         continue
    #       pairs1.sort(key=lambda n: active_voices.index(n))
    #
    #       av = active_voices.index(pairs[-1])
    #       av1 = active_voices.index(pairs1[0])
    #
    #       if av > av1:
    #         cross_count += 1
    #         break
    #     else:
    #       continue
    #
    #     break
    #
    #   active_voices.update(chord)
    #
    # active_voices.clear()

    # lookback
    # beat horizon
    # conv limit
    # div limit
    # cross

    # Density -> Average difference between av and len(chord)
    #         -> histogram of chord sizes

    # le4 = sum(v for k, v in bh_dict.items() if k <= 4)
    # g4 = sum(v for k, v in bh_dict.items() if k > 4)


    # self.fp.write(
    #   "%s, %d, %d, %f, %d, %d, %d, %d, %f, %d, %d, %d, %d, %d, %d, %d, %d, %d\n" % (
    #     score.name, num_notes, num_log_voices, notes_per_voice,
    #     num_pairs, num_o2os, num_o2ms, num_onsets, 
    #     synchronicity, num_pairs0, num_rests0, num_pairs1, num_rests1,
    #     num_pairsn, num_restsn, cross_count, le4, g4
    #   )
    # )

    # self.fp.write(
    #   "%s, %d, %d, %f, %d, %f, %d, %d, %d\n" % ( #, %d, %d, %d, %d, %d, %d, %d, %d, %d\n" % (
    #     score.name, num_notes, num_onsets, synchronicity, num_log_voices, notes_per_voice,
    #     num_pairs, num_o2os, num_o2ms
    #     # num_pairs0, num_rests0, num_pairs1, num_rests1,
    #     # num_pairsn, num_restsn, cross_count, le4, g4
    #   )
    # )

    # self.fp.write(
    #   "\n%s\n %s\n %s\n %s\n %s\n %d\n" % ( #, %d, %d, %d, %d, %d, %d, %d, %d, %d\n" % (
    #     score.name, lookback_histo, bh_histo, conv_histo, div_histo, cross_count
    #   )
    # )

    self.score_results.append(
      ScoreResult(
        name = score.name, 
        # num_notes = num_notes,
        # num_log_voices = num_log_voices,
        # notes_per_voice = notes_per_voice,
        # num_pairs = num_pairs,
        # num_o2os = num_o2os,
        # num_o2ms = num_o2ms,
        # num_onsets = num_onsets,
        # synchronicity = synchronicity,
        # num_pairs0 = num_pairs0,
        # num_pairs1 = num_pairs1,
        # num_pairsn = num_pairsn,
        # num_rests0 = num_rests0,
        # num_rests1 = num_rests1,
        # num_restsn = num_restsn,
        lookback_histo = lookback_histo,
        bh_histo = bh_histo,
        conv_histo = conv_histo,
        div_histo = div_histo,
        cross_count = cross_count
      )
    )

  def total(self):
    # tot_notes = sum(sr.num_notes for sr in self.score_results)
    # tot_voices = sum(sr.num_log_voices for sr in self.score_results)
    # tot_notes_per_voice = sum(sr.notes_per_voice for sr in self.score_results)
    # tot_pairs = sum(sr.num_pairs for sr in self.score_results)
    # tot_o2os = sum(sr.num_o2os for sr in self.score_results)
    # tot_o2ms = sum(sr.num_o2ms for sr in self.score_results)
    # tot_onsets = sum(sr.num_onsets for sr in self.score_results)
    # tot_synchronicity = sum(sr.synchronicity for sr in self.score_results)
    # tot_pairs0 = sum(sr.num_pairs0 for sr in self.score_results)
    # tot_pairs1 = sum(sr.num_pairs1 for sr in self.score_results)
    # tot_pairsn = sum(sr.num_pairsn for sr in self.score_results)
    # tot_rests0 = sum(sr.num_rests0 for sr in self.score_results)
    # tot_rests1 = sum(sr.num_rests1 for sr in self.score_results)
    # tot_restsn = sum(sr.num_restsn for sr in self.score_results)
    cross_count = sum(sr.cross_count for sr in self.score_results)

    tot_lookback_histo = [[0] * 6 for _ in range(6)]
    for sr in self.score_results:
      for i in range(len(sr.lookback_histo)):
        for j in range(len(sr.lookback_histo)):
          tot_lookback_histo[i][j] += sr.lookback_histo[i][j]

    tot_bh_histo = {}
    for sr in self.score_results:
      for k, v in sr.bh_histo.items():
        if k in tot_bh_histo:
          tot_bh_histo[k] += v
        else:
          tot_bh_histo[k] = v

    tot_conv_histo = {}
    for sr in self.score_results:
      for k, v in sr.conv_histo.items():
        if k in tot_conv_histo:
          tot_conv_histo[k] += v
        else:
          tot_conv_histo[k] = v

    tot_div_histo = {}
    for sr in self.score_results:
      for k, v in sr.div_histo.items():
        if k in tot_div_histo:
          tot_div_histo[k] += v
        else:
          tot_div_histo[k] = v

    # le4 = sum(v for k, v in tot_bh_dict.items() if k <= 4)
    # g4 = sum(v for k, v in tot_bh_dict.items() if k > 4)

    # self.fp.write(
    #   "\n Score, # Notes, # Onsets, Avg. Synchronicity, Avg. # Voices, Avg. # N/V, # Pairs, "
    #   "# o2o, # o2m\n"
    #   # "# pairs0, # rests0, # pairs1, # rests1, # pairsn, # restsn, "
    #   # "# cross, tot_bh_dict\n"
    # )

    num_scores = len(self.score_results)

    # print(le4, g4)

    # self.fp.write(
    #   "%d, %d, %f, %f, %f, %d, %d, %d\n" % (#, %d, %d, %d, %d, %d, %d, %d, %d, %d\n" % (
    #     tot_notes, tot_onsets, tot_synchronicity / num_scores,
    #     tot_voices / num_scores, tot_notes_per_voice / num_scores,
    #     tot_pairs, tot_o2os, tot_o2ms
    #     # tot_pairs0, tot_rests0, tot_pairs1, tot_rests1,
    #     # tot_pairsn, tot_restsn, cross_count, le4, g4
    #   )
    # )


    self.fp.write(
      "\n Score, Lookback, Beat Horizon, Conv,  Div, Cross\n"
    )
    self.fp.write(
      "%s\n %s\n %s\n %s\n %d\n" % ( #, %d, %d, %d, %d, %d, %d, %d, %d, %d\n" % (
        tot_lookback_histo, tot_bh_histo, tot_conv_histo, tot_div_histo, cross_count
      )
    )

class ScoreResult():
  def __init__(self, **kwargs):
    for key, value in kwargs.items():
      setattr(self, key, value)
