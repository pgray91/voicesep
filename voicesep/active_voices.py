import math
import voicesep.utils.constants as const

# Record pitch_space index
# How many overall voices

class ActiveVoices:
  def __init__(self, div_limit, lookback_inc, lookback_proxs, allow_overlap):
    self.active_voices = []
    self.beat_horizon = 4
    self.voiceid_type = "true"

    self.div_limit = div_limit
    self.lookback_inc = lookback_inc
    self.lookback_proxs = lookback_proxs
    self.allow_overlap = allow_overlap

  def clear(self):
    self.active_voices = []

  def subset(self, chord):
    remove = [False] * len(self.active_voices)
    for i, active_voice in enumerate(self.active_voices):
      active_voice.subset_index == -1
      active_voice.subset_length == 0

      if active_voice.position > 0:
        if self.lookback_inc > 0:
          beat_difference = max(0, chord.beat_onset - active_voice.beat_offset)

          lookback_index = (
            int(beat_difference // self.lookback_inc) - 
            (
              0 if beat_difference == 0
              else beat_difference % self.lookback_inc == 0
            )
          )
          prox = self.lookback_proxs[-1]
          if lookback_index < len(self.lookback_proxs):
            prox = self.lookback_proxs[lookback_index]

          active_voice.lookback_prox = prox

      if (
        self.voiceid_type == "true" and 
        any(p.beat_onset == chord.beat_onset for p in active_voice.pairs.right)
      ):
        continue

      # Remove if overlapping
      if (not self.allow_overlap) and active_voice.beat_offset > chord.beat_onset:
        remove[i] = True
        continue

      # Remove if div_limit exceeded
      if self.div_limit > 0 and active_voice.div_count >= self.div_limit:
        # assert active_voice.div_count <= self.div_limit
        remove[i] = True
        continue

      if active_voice.position > 0:
        # Remove if divergent voice blocked
        if active_voice.blocked:
          remove[i] = True
          continue

        # Remove if chord does not have note within proximity of 
        # divergent voice
        if self.lookback_inc == 0:
          continue

        remove[i] = not any(
          abs(n.pitch_space - active_voice.pitch_space) <= 
          active_voice.lookback_prox
          for n in chord
        )

    active_subset = [v for v, r in zip(self.active_voices, remove) if not r]
    last_index = 0
    last_above = None
    for i, active_voice in enumerate(active_subset):
      active_voice.voice_above = active_subset[i-1] if i > 0 else None
      active_voice.voice_below = (
        active_subset[i+1] if i < len(active_subset) - 1 else None
      )

      active_voice.subset_index = i
      active_voice.subset_length = len(active_subset)

      active_voice.last_above = last_above
      if active_voice.position > 0:
        active_voice.last_index = last_index + 0.5
        continue
      active_voice.last_index = last_index

      last_index += 1
      last_above = active_voice

    last_below = None
    for active_voice in reversed(active_subset):
      active_voice.last_length = last_index

      active_voice.last_below = last_below
      if active_voice.position == 0:
        last_below = active_voice

    return active_subset

  def filter(self, beat_onset):
    remove = [False] * len(self.active_voices)
    for i, active_voice in enumerate(self.active_voices):
      if beat_onset - active_voice.beat_offset > self.beat_horizon:
        remove[i] = True

      else:
        # Remove if blocking voice is removed
        blocking_voice = active_voice.blocker
        while blocking_voice is not None:
          if beat_onset - blocking_voice.beat_offset > self.beat_horizon:
            remove[i] = True
            break

          blocking_voice = blocking_voice.blocker

      # if remove[i]:
      #   for crossing_voice in active_voice.crossers:
      #     crossing_voice.crossers.remove(active_voice)

    self.active_voices = [
      v for v, r in zip(self.active_voices, remove) if not r
    ]

    # Update indices
    for i, active_voice in enumerate(self.active_voices):
      active_voice.active_index = i

  def update(self, chord):
    voices = [Voice(n, self.voiceid_type) for n in chord]

    # Sort the pairs
    for voice in voices:
      voice.pairs.left.sort(key=lambda p : self.active_voices.index(p))

    # Mark crossing voices
    paired = [True] * len(voices)
    for i, voice1 in enumerate(voices):
      if len(voice1.pairs.left) == 0:
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

    # Attach paired voices
    for voice in paired_voices:
      for left_pair in voice.pairs.left:
        i = self.active_voices.index(left_pair)
        voice.left.append(self.active_voices[i])
        self.active_voices[i].right.append(voice)
        self.active_voices[i].div_count += 1

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
    for active_voice in self.active_voices:
      active_voice.right.sort(key=lambda v : v.pitch_space, reverse=True)

    # Update indices
    for i, active_voice in enumerate(self.active_voices):
      active_voice.active_index = i

      visited = set()
      voice_stack = [active_voice]
      depth_stack = [0]
      max_depth = 0
      while len(voice_stack) > 0:
        voice = voice_stack.pop()
        depth = depth_stack.pop()

        if voice in visited:
          continue
        visited.add(voice)

        max_depth = max(max_depth, depth)
        voice_stack.extend(voice.right)
        depth_stack.extend([depth + 1] * len(voice.right))

        active_voice.all_right.extend(voice.right)

      active_voice.position = max_depth

    # Create stats, conv and div list
    for active_voice in voices:
      active_voice.nv_above = (
        None if active_voice.note.note_above is None else 
        self.active_voices[self.active_voices.index(active_voice.note.note_above)]
      )
      active_voice.nv_below = (
        None if active_voice.note.note_below is None else 
        self.active_voices[self.active_voices.index(active_voice.note.note_below)]
      )

    for active_voice in paired_voices:
      pitch_spaces = []
      div_notes = []
      conv_notes = []

      visited = set()
      voice_stack = [active_voice]
      length_stack = [1]
      max_length = 0
      while len(voice_stack) > 0:
        voice = voice_stack.pop()
        length = length_stack.pop()
        if (
          voice not in visited and 
          chord.beat_onset - voice.beat_offset <= self.beat_horizon
        ):
          visited.add(voice)

          pitch_spaces.append(voice.pitch_space)

          if voice.div_count > 1:
            div_notes.append(voice.note)

          if len(conv_notes) == 0 and len(voice.left) > 1:
            conv_notes = voice.pairs.left

          max_length = max(max_length, length)

          voice_stack += voice.left
          length_stack += [length + 1] * len(voice.left)

      active_voice.length = max_length
      active_voice.note_count = len(pitch_spaces)
      active_voice.avg_pitch_space = sum(pitch_spaces) / len(pitch_spaces)
      active_voice.std_pitch_space = math.sqrt(
        sum(
          (ps - active_voice.avg_pitch_space) ** 2
          for ps in pitch_spaces
        ) / len(pitch_spaces)
      )
      active_voice.max_pitch_space = max(pitch_spaces)
      active_voice.min_pitch_space = min(pitch_spaces)

      active_voice.div_notes = div_notes
      active_voice.conv_notes = conv_notes

      cons_repeat = 0
      voice = active_voice
      while chord.beat_onset - voice.beat_offset <= self.beat_horizon:
        eq_pair = None
        for left_voice in voice.left:
          if left_voice.pitch_space == voice.pitch_space:
            eq_pair = left_voice
            break

        if eq_pair is None:
          break

        cons_repeat += 1
        voice = eq_pair

      active_voice.cons_repeat = cons_repeat

      length_top = 0
      avg_pitch_dis_above = 0
      rest_count_top = 0
      avg_onset_dis_top = 0
      avg_onset_offset_top = 0
      dur_diff_count_above = 0
      voice = active_voice
      while chord.beat_onset - voice.beat_offset <= self.beat_horizon:
        avg_pitch_dis_above += (
          abs(voice.note.pitch_space - voice.note.note_above.pitch_space) 
          if voice.note.note_above else const.MAX_PITCH_DISTANCE
        )
        dur_diff_count_above += (
          voice.note.beat_duration != voice.note.note_above.beat_duration
          if voice.note.note_above else 1
        )
        length_top += 1
        if len(voice.left) == 0:
          break

        avg_onset_dis_top += (
          max(voice.note.beat_onset - voice.left[0].note.beat_onset, 0) 
        )
        avg_onset_offset_top += (
          max(voice.note.beat_onset - voice.left[0].note.beat_offset, 0) 
        )
        rest_count_top += voice.note.beat_onset - voice.left[0].note.beat_offset > 0

        voice = voice.left[0]

      active_voice.length_top = length_top
      active_voice.avg_pitch_dis_above = avg_pitch_dis_above / length_top
      active_voice.avg_onset_dis_top = avg_onset_dis_top / length_top
      active_voice.avg_onset_offset_top = avg_onset_offset_top / length_top
      active_voice.rest_count_top = rest_count_top
      active_voice.dur_diff_count_above = dur_diff_count_above

      length_bottom = 0
      avg_pitch_dis_below = 0
      rest_count_bottom = 0
      avg_onset_dis_bottom = 0
      avg_onset_offset_bottom = 0
      dur_diff_count_below = 0
      voice = active_voice
      while chord.beat_onset - voice.beat_offset <= self.beat_horizon:
        avg_pitch_dis_below += (
          abs(voice.note.pitch_space - voice.note.note_below.pitch_space) 
          if voice.note.note_below else const.MAX_PITCH_DISTANCE
        )
        dur_diff_count_below += (
          voice.note.beat_duration != voice.note.note_below.beat_duration
          if voice.note.note_below else 1
        )
        length_bottom += 1
        if len(voice.left) == 0:
          break

        avg_onset_dis_bottom += (
          max(voice.note.beat_onset - voice.left[0].note.beat_onset, 0) 
        )
        avg_onset_offset_bottom += (
          max(voice.note.beat_onset - voice.left[0].note.beat_offset, 0) 
        )
        rest_count_bottom += voice.note.beat_onset - voice.left[-1].note.beat_offset > 0

        voice = voice.left[-1]

      active_voice.length_bottom = length_bottom
      active_voice.avg_pitch_dis_below = avg_pitch_dis_below / length_bottom
      active_voice.avg_onset_dis_bottom = avg_onset_dis_bottom / length_bottom
      active_voice.avg_onset_offset_bottom = avg_onset_offset_bottom / length_bottom
      active_voice.dur_diff_count_below = dur_diff_count_below
      active_voice.rest_count_bottom = rest_count_bottom

  def index(self, note):
    return self.active_voices.index(note)

  def __len__(self):
    return len(self.active_voices)

  def __getitem__(self, index):
    return self.active_voices[index]

  def __iter__(self):
    return iter(self.active_voices)

class Voice():
  def __init__(self, note, voiceid_type):
    self.note = note

    self.pitch_space = note.pitch_space
    self.beat_onset = note.beat_onset
    self.beat_offset = note.beat_offset

    self.pairs = note.pairs(voiceid_type)
    self.voiceid_type = voiceid_type
    self.left = []
    self.right = []

    self.active_index = 0
    self.position = 0

    self.last_index = -1
    self.last_length = 0

    self.subset_index = -1
    self.subset_length = 0

    self.length = 1
    self.note_count = 1
    self.avg_pitch_space = self.pitch_space
    self.std_pitch_space = 0
    self.max_pitch_space = self.pitch_space
    self.min_pitch_space = self.pitch_space

    self.crossers = []
    self.blocker = None
    self.blocked = False

    self.voice_above = None
    self.voice_below = None
    self.last_above = None
    self.last_below = None

    self.div_notes = []
    self.conv_notes = []

    self.div_count = 0
    self.lookback_prox = 120

    self.rest_count_top = 0
    self.rest_count_bottom = 0
    self.avg_onset_dist_top = 0
    self.avg_onset_dist_bottom = 0
    self.avg_onset_offset_top = 0
    self.avg_onset_offset_bottom = 0

    self.length_top = 0
    self.length_bottom = 0

    self.cons_repeat = 0

    self.avg_pitch_dis_above = (
      abs(
        self.pitch_space - 
        self.note.note_above.pitch_space
      )
      if self.note.note_above else const.MAX_PITCH_DISTANCE
    )
    self.avg_pitch_dis_below = (
      abs(
        self.pitch_space - 
        self.note.note_below.pitch_space
      )
      if self.note.note_below else const.MAX_PITCH_DISTANCE
    )
    self.dur_diff_count_above = (
      self.note.beat_duration != 
      self.note.note_above.beat_duration
      if self.note.note_above else 1
    )
    self.dur_diff_count_below = (
      self.note.beat_duration != 
      self.note.note_below.beat_duration
      if self.note.note_below else 1
    )

    self.all_right = []

  def __eq__(self, other):
    return self.note is other

  def __hash__(self):
    return self.note.__hash__()
