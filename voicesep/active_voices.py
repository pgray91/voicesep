class ActiveVoices:
  def __init__(self, beat_horizon):
    self.beat_horizon = beat_horizon
    self.voices = []

  def subset(self, beat_onset):
    return [
      voice for voice in self.voices
      if voice.beat_offset + self.beat_horizon >= beat_onset
      or any(voice.beat_onset == beat_onset for voice in voice.diverged())
    ]

  def update(self, voices):

    inserted = [True] * len(voices)
    for i, voice in enumerate(voices):
      if len(voice.converged) == 0:
        paired[i] = False
        continue

      # p_i1 = self.active_voices.index(voice1.pairs.left[-1])
      # for voice2 in voices[i+1:]:
      #   if len(voice2.pairs.left) == 0:
      #     continue
      #
      #   p_i2 = self.active_voices.index(voice2.pairs.left[0])
      #   if p_i1 > p_i2:
      #     paired[i] = False
      #     voice1.crossers.append(voice2)
      #     voice2.crossers.append(voice1)

    # Separate paired and upaired voices
    paired_voices = [v for v, p in zip(voices, paired) if p]
    unpaired_voices = [v for v, p in zip(voices, paired) if not p]

    # Insert the paired voices
    unpaired = [False] * len(paired_voices)
    for ind, voice in enumerate(paired_voices):
      i = self.active_voices.index(voice.pairs.left[0])
      
      j = -1
      for left_pair in voice.pairs.left:
        if voice.pitch_space >= left_pair.pitch_space:
          break
        j += 1
        i += 1

      # if (
      #   len(voice.pairs.left) > 1 or 
      #   voice.pitch_space < voice.pairs.left[0].pitch_space
      # ):
      #   i += 1

      while (
        i < len(self.active_voices) and 
        voice.beat_onset == self.active_voices[i].beat_onset and
        voice.pairs.left[j] in self.active_voices[i].pairs.left
      ):
        i += 1

      if j > -1:
        unpaired[ind] = any(
          v.pitch_space > voice.pitch_space and v.beat_onset > voice.pairs.left[j].beat_onset
          for v in self.active_voices[i:]
        )
      else:
        unpaired[ind] = any(
          v.pitch_space <= voice.pitch_space and v.beat_onset > voice.pairs.left[0].beat_onset
          for v in self.active_voices[:i]
        )

      if not unpaired[ind]:
        self.active_voices.insert(i, voice)

    unpaired_voices.extend([v for v, p in zip(paired_voices, unpaired) if p])

    # Mark the blocking voices
    for i, active_voice1 in enumerate(self.active_voices):
      active_voice1.blocker = None
      # I might try continuing if active_voice1.blocker is not None

      for j in reversed(range(i)):
        active_voice2 = self.active_voices[j]
        if active_voice1.beat_onset <= active_voice2.beat_onset:
          while active_voice1.pitch_space < active_voice2.pitch_space:
            active_voice2 = active_voice2.blocker
            if active_voice2 is None:
              break

          active_voice1.blocker = active_voice2
          break

        if active_voice1.pitch_space >= active_voice2.pitch_space:
          if (
            active_voice2.blocker is None or
            active_voice2.blocker.beat_onset > 
            active_voice1.beat_onset
          ):
            active_voice2.blocker = active_voice1

    # Flag blocked voices
    for active_voice in self.active_voices:
      if active_voice.blocker is not None:
        active_voice.blocked = True

    for voice in paired_voices:
      i = self.active_voices.index(voice.pairs.left[0])
      j = self.active_voices.index(voice.pairs.left[-1])

      for k in range(i + 1, j):
        if voice is self.active_voices[k]:
          continue

        self.active_voices[k].blocked = True

    # Insert the unpaired voices
    for voice in unpaired_voices:
      for i in reversed(range(len(self.active_voices))):
        active_voice = self.active_voices[i]
        while active_voice.blocker is not None:
          active_voice = active_voice.blocker

        if voice.pitch_space < active_voice.pitch_space:
          break
      else:
        self.active_voices.insert(0, voice)
        continue

      self.active_voices.insert(i + 1, voice)

    # Sort the right pairs
    for voice in self.active_voices:
      active_voice.right.sort(key=lambda v : v.pitch_space, reverse=True)
