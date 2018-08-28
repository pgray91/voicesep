def separate(score, active_voices):
  active_voices.voiceid_type = "proximity"
  active_voices.beat_horizon = score.beat_horizon

  active_voices.update(score[0])
  for chord in score[1:]:
    active_voices.filter(chord.beat_onset)

    active_subset = active_voices.subset(chord)

    i = 0
    for note in chord:
      while i < len(active_subset):
        i += 1

        if active_subset[i-1].blocked:
          continue

        if (
          i == len(active_subset) or
          abs(note.pitch_space - active_subset[i-1].note.pitch_space) <=
          abs(note.pitch_space - active_subset[i].note.pitch_space)
        ):
          note.proximity_pairs.left.append(active_subset[i-1].note)
          active_subset[i-1].note.proximity_pairs.right.append(note)
          break

    active_voices.update(chord)

  active_voices.clear()
