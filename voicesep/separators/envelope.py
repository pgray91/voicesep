def separate(score, active_voices):
  assignments = []

  active_voices.update([Voice(note) for note in score[0]])
  for chord in score[1:]:
    active_voices.filter(chord.beat_onset)

    nonoverlap = [
      voice for voice in active_voices
      if voice.beat_offset <= chord.beat_onset
    ]

    assignment = [
      Voice(note, [voice]) for note, voice in zip(chord, nonoverlap)
    ]
    assignment.extend([
      Voice(note, []) for note in chord[len(nonoverlap):]
    ])

    assignments.append(assignment)

    active_voices.update(assignment)
