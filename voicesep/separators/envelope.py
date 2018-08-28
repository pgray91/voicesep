def separate(score, active_voices):
  active_voices.voiceid_type = "envelope"
  active_voices.beat_horizon = score.beat_horizon

  active_voices.update(score[0])
  for chord in score[1:]:
    active_voices.filter(chord.beat_onset)

    active_subset = active_voices.subset(chord)

    sub_chord = []
    for note in chord:
      if note.repeat_behind and note.repeat_count > 4:
        for voice in active_subset:
          if voice.note is note.repeat_behind:
            note.envelope_pairs.left.append(voice.note)
            voice.note.envelope_pairs.right.append(note)
            break
      else:
        sub_chord.append(note)

    sub_active_subset = []
    for voice in active_subset:
      if not voice.note.envelope_pairs.right:
        sub_active_subset.append(voice)

    for note, voice in zip(sub_chord, sub_active_subset):
      note.envelope_pairs.left.append(voice.note)
      voice.note.envelope_pairs.right.append(note)

    active_voices.update(chord)

  active_voices.clear()
