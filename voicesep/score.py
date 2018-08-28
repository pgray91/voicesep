import music21 as m21
import random
from fractions import Fraction as F
import decimal
from decimal import Decimal as D
import numpy as np
import voicesep as vs

# Require rule to change tempo every time meter changes
# Use a boolean value to indicate that the pedal is pressed
# Make sure lyrics aren't messed up on rewrite
# Check fermata
# Allow black

class Score:

  HS_PER_8VA = 12

  MAX_PITCH_SPACE = 120
  MIN_PITCH_SPACE = 0
  MAX_DURATION = 10

  def __init__(
    self, score_file, beat_horizon, is_one_to_many, mark_true=True
  ):
    # Read in musicxml
    self.score = m21.converter.parse(score_file)
    self.beat_horizon = beat_horizon
    self.name = score_file.split("/")[-1].split(".")[0]
    self.chords = []

    timesig = self.score.flat.getElementsByClass("TimeSignature")[0]
    tempo = self.score.flat.getElementsByClass("MetronomeMark")[0]
    keysig = self.score.flat.getElementsByClass("KeySignature")[0]
    scale = keysig.getScale()

    tie_dictionary = {}

    decimal.getcontext().prec = 12
    beat_onset_start = F(0)
    beat_onset_ql_ref = F(0)
    sec_onset_start = D(0)
    sec_onset_ql_ref = F(0)

    chord_index = 0

    # Iterate measure by measure
    measures = self.score.semiFlat.getElementsByClass("Measure").stream()
    measure_groups = [
      m21.stream.Stream(measure_group) 
      for measure_group in measures.groupElementsByOffset()
    ]
    for measure_index, measure_group in enumerate(measure_groups):
      # Check if timesignature changed
      if len(measure_group[0].getElementsByClass("TimeSignature")):
        beat_onset_start += (
          (F(measure_group[0].offset) - beat_onset_ql_ref) /
          F(4 / timesig.denominator)
        )
        beat_onset_ql_ref = F(measure_group[0].offset)

        timesig = measure_group[0].getElementsByClass("TimeSignature")[0]

      # Check if tempo changed
      if len(measure_group[0].getElementsByClass("MetronomeMark")):
        sec_onset_start += D(tempo.durationToSeconds(
          (F(measure_group[0].offset) - sec_onset_ql_ref)
        ))
        sec_onset_ql_ref = F(measure_group[0].offset)

        tempo = measure_group[0].getElementsByClass("MetronomeMark")[0]

      # Check if key signature changed
      if len(measure_group[0].getElementsByClass("KeySignature")):
        keysig = measure_group[0].getElementsByClass("KeySignature")[0]
        scale = keysig.getScale()

      # Mark the part index
      for part_index, measure_part in enumerate(measure_group):
        for chord_part in measure_part.flat.notes:
          notes = chord_part if chord_part.isChord else [chord_part]
          for note in notes:
            note.part_index_ = part_index

      # Iterate over chords in measure
      chords = measure_group.flat.notes.stream()
      for mc_index, chord_group in enumerate(chords.groupElementsByOffset()):
        ql_onset = F(chord_group[0].offset)
        beat = chord_group[0].beat
        beat_strength = chord_group[0].beatStrength

        # Iterate over chord parts in chord
        note_list = [] # Converted to vs chord
        for chord_part in chord_group:
          if chord_part.duration.isGrace:
            continue

          # Check for staccato
          has_staccato = False
          end_notes = [chord_part]
          if chord_part.isChord:
            end_notes = [chord_part[0], chord_part[-1]]
          for note in end_notes:
            for articulation in note.articulations:
              if articulation.name == "staccato":
                has_staccato = True
                break
            if has_staccato:
              break
      
          # Chord degrees
          chord_stepper = m21.chord.Chord(
            chord_part if chord_part.isChord else [chord_part]
          )

          # Iterate over notes in chord part
          notes = chord_part if chord_part.isChord else [chord_part]
          for note_index, note in enumerate(sorted(notes, reverse=True)):

            # Convert note to enharmonic of scale
            for scale_pitch in scale.pitches:
              if (
                int(note.pitch.ps) % Score.HS_PER_8VA != 
                int(scale_pitch.ps) % Score.HS_PER_8VA
              ):
                continue
              if note.pitch.name == scale_pitch.name:
                break

              prev_ps = int(note.pitch.ps)
              note.pitch.name = scale_pitch.name
              if int(note.pitch.ps) < prev_ps:
                note.pitch.octave += 1
              elif int(note.pitch.ps) > prev_ps:
                note.pitch.octave -= 1
              break

            # Set durations, onsets, and offsets
            note.has_staccato_ = has_staccato

            note.ql_duration_ = F(note.duration.quarterLength)
            if has_staccato:
              note.ql_duration_ *= F(1,2)
            note.ql_onset_ = ql_onset
            note.ql_offset_ = note.ql_onset_ + note.ql_duration_

            note.beat_duration_ = (
              note.ql_duration_ / F(4 / timesig.denominator)
            )

            note.beat_onset_ = beat_onset_start + (
              (note.ql_onset_ - beat_onset_ql_ref) / 
              F(4 / timesig.denominator)
            )
            note.beat_offset_ = note.beat_onset_ + note.beat_duration_

            note.sec_duration_ = D(tempo.durationToSeconds(note.ql_duration_))
            note.sec_onset_ = sec_onset_start + D(tempo.durationToSeconds(
              note.ql_onset_ - sec_onset_ql_ref
            ))
            note.sec_offset_ = note.sec_onset_ + note.sec_duration_

            # Get colors and lyrics
            note.true_color_ = note.color
            note.true_lyric_ = ""
            if len(chord_part.lyrics):
              note.true_lyric_ = chord_part.lyrics[note_index].text
            
            # Adjust durations and offsets of tied notes 
            if note.tie and note.tie.type != "start":
              vs_note = tie_dictionary[int(note.pitch.ps)]

              vs_note.ql_duration += note.ql_duration_
              vs_note.ql_offset += note.ql_duration_

              vs_note.beat_duration += note.beat_duration_
              vs_note.beat_offset += note.beat_duration_

              vs_note.sec_duration += note.sec_duration_
              vs_note.sec_offset += note.sec_duration_
              continue

            # Get degree, beat, beat strength, and chord step
            note.degree_ = scale.getScaleDegreeFromPitch(
              note.name, comparisonAttribute="step"
            )
            assert note.degree_ != 0

            note.beat_ = beat
            note.beat_strength_ = beat_strength

            note.chord_step_ = 0
            for cs in range(1,8):
              if chord_stepper.getChordStep(cs) is not None:
                if chord_stepper.getChordStep(cs).step == note.step:
                  note.chord_step_ = cs
                  break
            assert note.chord_step_ != 0

            note_list.append(note)

        # Create vs_note_list
        vs_note_list = [None] * len(note_list)
        for i, note in enumerate(sorted(note_list, reverse=True)):
          vs_note = Note(
            m21_note = note,
            name = note.name, 
            octave = note.octave,
            pitch_space = int(note.pitch.ps),

            ql_duration = note.ql_duration_, 
            ql_onset = note.ql_onset_,
            ql_offset = note.ql_offset_,

            beat_duration = note.beat_duration_, 
            beat_onset = note.beat_onset_,
            beat_offset = note.beat_offset_,

            sec_duration = note.sec_duration_,
            sec_onset = note.sec_onset_,
            sec_offset = note.sec_offset_,

            has_staccato = note.has_staccato_,

            beat = note.beat_,
            beat_strength = note.beat_strength_,

            all_index = {},
            index = i,
            chord_index = chord_index,
            mc_index = mc_index,
            measure_index = measure_index,
            part_index = note.part_index_,

            chord_length = len(note_list),
            all_length = {},
            
            degree = note.degree_,
            chord_step = note.chord_step_,

            note_above = None,
            note_below = None,

            note_right = None,
            note_left = None,
            poly_right = None,
            poly_left = None,
            repeat_right = None,
            repeat_left = None,

            poly_left_count = 0,
            poly_right_count = 0,
            poly_repeat_left = 0,
            poly_repeat_right = 0,
            zig_zag = 0,
            
            repeat_count = 0,
            repeat_ahead = None,
            repeat_behind = None,
            note_ahead = None,
            note_behind = None,

            true_pairs = Pairs(),
            neural_pairs = Pairs(),
            envelope_pairs = Pairs(),
            proximity_pairs = Pairs(),
            poly_pairs = Pairs(),

            true_lyric = note.true_lyric_.split(",")if note.true_lyric_ else [],
            pred_lyric = [],
            true_color = note.color,
            pred_color = "",

            right_repeat = 0,
            left_repeat = 0,
          )

          vs_note_list[i] = vs_note

          if note.tie:
            tie_dictionary[int(note.pitch.ps)] = vs_note

        # Create vs_chord
        if len(vs_note_list):
          vs_chord = Chord(
            notes = vs_note_list,
            all_notes = [],

            beat_onset = vs_note_list[0].beat_onset,

            index = chord_index,
            mc_index = mc_index,
            measure_index = measure_index,
          )
          self.chords.append(vs_chord)
          chord_index += 1

    # Mark true voices
    if mark_true:
      voice_dictionary = {}
      voiceid_dictionary = {}
      for chord in self.chords:
        for note in chord:
          voiceids = [note.true_color]
          if is_one_to_many:
            if len(note.true_lyric) > 0:
              voiceid_dictionary[note.true_color] = note.true_lyric
              voiceids = note.true_lyric
            else:
              voiceids = voiceid_dictionary[note.true_color]

          for voiceid in voiceids:
            if voiceid in voice_dictionary:
              left_pair = voice_dictionary[voiceid]
              if left_pair not in note.true_pairs.left:
                if (
                  note.beat_onset - 
                  left_pair.beat_offset <=
                  beat_horizon
                ):
                  note.true_pairs.left.append(left_pair)
                  left_pair.true_pairs.right.append(note)

            voice_dictionary[voiceid] = note

    # Chordify
    chord = self.chords[0]
    chord.all_notes = chord.notes
    for i, note in enumerate(chord.all_notes):
      note.all_index[chord.index] = i
      note.all_length[chord.index] = len(chord.all_notes)

    for i, chord in enumerate(self.chords[1:], start=1):
      chord.all_notes = chord.notes + self.chords[i-1].all_notes
      chord.all_notes = [
        n for n in chord.all_notes if n.beat_offset > chord.beat_onset
      ]

      chord.all_notes.sort(key=lambda n: n.beat_onset, reverse=True)
      chord.all_notes.sort(key=lambda n: n.pitch_space, reverse=True)

      for j, note in enumerate(chord.all_notes):
        note.all_index[chord.index] = j
        note.all_length[chord.index] = len(chord.all_notes)

    # Link to notes ahead
    for chord in self.chords:
      for note in chord:
        if note.ql_duration > 0.5:
          continue

        ahead = False
        chord_index = chord.index + 1
        while chord_index < len(self.chords):
          if self.chords[chord_index].beat_onset == note.beat_offset:
            ahead = True
            break

          if self.chords[chord_index].beat_onset > note.beat_offset:
            break

          chord_index += 1

        if ahead:
          note1 = self.chords[chord_index][0]
          pd = abs(note.pitch_space - note1.pitch_space)
          for note2 in self.chords[chord_index][1:]:
            if abs(note.pitch_space - note2.pitch_space) < pd:
              pd = abs(note.pitch_space - note2.pitch_space)
              note1 = note2

          note.note_ahead = note1

          for note1 in self.chords[chord_index]:
            if note1.note_behind is None:
              note1.note_behind = note
              continue

            pd = abs(note1.note_behind.pitch_space - note1.pitch_space)
            if abs(note1.pitch_space - note.pitch_space) < pd:
              note1.note_behind = note

        repeated = False
        chord_index = chord.index + 1
        while chord_index < len(self.chords):
          if self.chords[chord_index].beat_onset == note.beat_offset + note.beat_duration:
            repeated = True
            break

          if self.chords[chord_index].beat_onset > note.beat_offset + note.beat_duration:
            break

          chord_index += 1

        if repeated:
          for note1 in self.chords[chord_index]:
            if note1.pitch_space == note.pitch_space:
              note.repeat_ahead = note1
              note1.repeat_behind = note
              break

    for chord in self.chords:
      for note in chord:
        if note.note_ahead and note.note_behind:
          if note.note_ahead.pitch_space == note.note_behind.pitch_space:
            continue

          if (
            note.note_ahead.note_behind is note and note.note_behind.note_ahead is note and
            (
              (note.note_ahead.pitch_space < note.pitch_space) != 
              (note.note_behind.pitch_space < note.pitch_space)
            )
          ):
            continue

        if note.repeat_behind:
          if note.repeat_behind.repeat_count == 0:
            continue

        repeat_count = 0

        repeat_ahead = note.repeat_ahead
        while repeat_ahead:
          if repeat_ahead.note_behind:
            if abs(repeat_ahead.pitch_space - repeat_ahead.note_behind.pitch_space) <= 1:
              break

            if repeat_ahead.note_ahead:
              if repeat_ahead.note_behind.pitch_space == repeat_ahead.note_ahead.pitch_space:
                break

          repeat_count += 1
          repeat_ahead = repeat_ahead.repeat_ahead

        repeat_behind = note.repeat_behind
        while repeat_behind:
          if repeat_behind.note_ahead:
            if abs(repeat_behind.pitch_space - repeat_behind.note_ahead.pitch_space) <= 1:
              break

            if repeat_behind.note_behind:
              if repeat_behind.note_ahead.pitch_space == repeat_behind.note_behind.pitch_space:
                break

          repeat_count += 1
          repeat_behind = repeat_behind.repeat_behind

        note.repeat_count = repeat_count

        # note.note_right = self.chords[chord_index][0]
        # for note1 in self.chords[chord_index][1:]:
        #   if (
        #     abs(note1.pitch_space - note.pitch_space) <
        #     abs(note.note_right.pitch_space - note.pitch_space)
        #   ):
        #     note.note_right = note1
        #
        # note.note_right.note_left = note
        #
        # if self.chords[chord_index].beat_onset != note.beat_offset:
        #   continue
        #
        # # Maybe only set poly right if poly right has same
        # # duration
        # poly_right = self.chords[chord_index][0]
        # for note1 in self.chords[chord_index][1:]:
        #   if (
        #     abs(note1.pitch_space - note.pitch_space) <
        #     abs(poly_right.pitch_space - note.pitch_space)
        #   ):
        #     poly_right = note1
        #
        # if poly_right.pitch_space == note.pitch_space:
        #   continue
        #
        # note.poly_right = poly_right
        # note.poly_right.poly_left = note

    # active_voices = vs.ActiveVoices(
    #   div_limit=1, lookback_inc=1, lookback_proxs=(-1,), allow_overlap=False
    # )
    # active_voices.voiceid_type = "poly"
    # for chord in self.chords:
    #   active_voices.filter(chord.beat_onset)
    #   active_subset = active_voices.subset(chord)
    #
    #   voice_mask = np.ones((len(chord), len(active_subset)))
    #   note_count = len(chord)
    #   while note_count > 0:
    #     pitch_min = Score.MAX_PITCH_SPACE
    #     note_index = -1
    #     voice_index = -1
    #     for i, note in enumerate(chord):
    #       for j, voice in enumerate(active_subset):
    #         if not voice_mask[i, j]:
    #           continue
    #
    #         if note.beat_onset != voice.beat_offset:
    #           continue
    #
    #         if note.beat_duration != voice.note.beat_duration:
    #           continue
    #
    #         if note.pitch_space == voice.pitch_space:
    #           continue
    #
    #         if abs(note.pitch_space - voice.pitch_space) < pitch_min:
    #           pitch_min = abs(note.pitch_space - voice.pitch_space)
    #           note_index = i
    #           voice_index = j
    #
    #     if note_index != -1:
    #       note = chord[note_index]
    #       voice = active_subset[voice_index]
    #
    #       note.poly_pairs.left.append(voice.note)
    #       voice.note.poly_pairs.right.append(note)
    #
    #       voice_mask[note_index, :] = 0
    #
    #       for i in range(len(chord)):
    #         if i < note_index:
    #           voice_mask[i, voice_index:] = 0
    #         elif i > note_index:
    #           voice_mask[i, :voice_index + 1] = 0
    #
    #     note_count -= 1
    #
    #   active_voices.update(chord)
    # active_voices.clear()
    #
    # for chord in self.chords:
    #   for note in chord:
    #     poly_left = (
    #       note.poly_pairs.left[0] if len(note.poly_pairs.left) > 0 else None
    #     )
    #     poly_right = (
    #       note.poly_pairs.right[0] if len(note.poly_pairs.right) > 0 else None
    #     )
    #     if poly_left and poly_right:
    #       if (
    #         poly_left.pitch_space > note.pitch_space and 
    #         poly_right.pitch_space > note.pitch_space
    #       ):
    #         note.zig_zag = 1
    #       elif (
    #         poly_left.pitch_space < note.pitch_space and 
    #         poly_right.pitch_space < note.pitch_space
    #       ):
    #         note.zig_zag = 2
    #
    #     if poly_left:
    #       poly_left_count = 1
    #       zig = poly_left.pitch_space > note.pitch_space
    #       while True:
    #         next_poly = (
    #           poly_left.poly_pairs.left[0] 
    #           if len(poly_left.poly_pairs.left) > 0 else None
    #         )
    #         if next_poly is None:
    #           break
    #
    #         if zig == (next_poly.pitch_space > poly_left.pitch_space):
    #           break
    #
    #         poly_left_count += 1
    #         if poly_left_count > 5:
    #           break
    #
    #         zig = not zig
    #         poly_left = next_poly
    #
    #       note.poly_left_count = poly_left_count
    #
    #       poly_left = note.poly_pairs.left[0]
    #       poly_repeat_left = 0
    #       zig = poly_left.pitch_space > note.pitch_space
    #       while True:
    #         next_poly = (
    #           poly_left.poly_pairs.left[0] 
    #           if len(poly_left.poly_pairs.left) > 0 else None
    #         )
    #         if next_poly is None:
    #           break
    #
    #         if zig != (next_poly.pitch_space > poly_left.pitch_space):
    #           if next_poly.pitch_space == note.pitch_space:
    #             poly_repeat_left += 1
    #           else:
    #             break
    #
    #         if poly_repeat_left > 2:
    #           break
    #
    #         poly_left = next_poly
    #
    #       note.poly_repeat_left = poly_repeat_left
    #
    #     if poly_right:
    #       poly_right_count = 1
    #       zig = poly_right.pitch_space > note.pitch_space
    #       while True:
    #         next_poly = (
    #           poly_right.poly_pairs.right[0]
    #           if len(poly_right.poly_pairs.right) > 0 else None
    #         )
    #         if next_poly is None:
    #           break
    #
    #         if zig == (next_poly.pitch_space > poly_right.pitch_space):
    #           break
    #
    #         poly_right_count += 1
    #         if poly_right_count > 5:
    #           break
    #
    #         zig = not zig
    #         poly_right = next_poly
    #
    #       note.poly_right_count = poly_right_count
    #
    #       poly_right = note.poly_pairs.right[0]
    #       poly_repeat_right = 0
    #       zig = poly_right.pitch_space > note.pitch_space
    #       while True:
    #         next_poly = (
    #           poly_right.poly_pairs.right[0] 
    #           if len(poly_right.poly_pairs.right) > 0 else None
    #         )
    #         if next_poly is None:
    #           break
    #
    #         if zig != (next_poly.pitch_space > poly_right.pitch_space):
    #           if next_poly.pitch_space == note.pitch_space:
    #             poly_repeat_right += 1
    #           else:
    #             break
    #
    #         if poly_repeat_right > 2:
    #           break
    #
    #         poly_right = next_poly
    #
    #       note.poly_repeat_right = poly_repeat_right

  def write(self, fp, voiceid_type):
    if voiceid_type != "true":
      for chord in self.chords:
        for note in chord:
          note.m21_note.show_lyric_ = False

      random.seed(501)
      rint1 = lambda: random.randint(0,255)
      random.seed(20342)
      rint2 = lambda: random.randint(0,255)
      random.seed(16)
      rint3 = lambda: random.randint(0,255)

      lyric_dictionary = {}
      lyric_count = 1
      for chord in self.chords:
        for note in chord:

          note.pred_lyric = []

          pairs = note.pairs(voiceid_type)

          if len(pairs.left) == 0:
            note.pred_lyric.append(str(lyric_count))
            lyric_count += 1

          for left_pair in pairs.left:
            lefts_pairs = left_pair.pairs(voiceid_type)
            i = lefts_pairs.right.index(note)
            note.pred_lyric.append(left_pair.pred_lyric[i])

          while len(pairs.right) > len(note.pred_lyric):
            note.pred_lyric.append(str(lyric_count))
            lyric_count += 1

          if note.pred_lyric[0] not in lyric_dictionary:
            note.m21_note.color = ("#%02X%02X%02X"%(rint1(), rint2(), rint3()))
            lyric_dictionary[note.pred_lyric[0]] = note.m21_note.color
          else:
            note.m21_note.color = lyric_dictionary[note.pred_lyric[0]]

          if len(pairs.left) != 1:
            note.m21_note.show_lyric_ = True
            for left_pair in pairs.left:
              left_pair.m21_note.show_lyric_ = True

          if len(pairs.right) > 1:
            note.m21_note.show_lyric_ = True
            for right_pair in pairs.right:
              right_pair.m21_note.show_lyric_ = True

          note.m21_note.pred_lyric_ = ",".join(l for l in note.pred_lyric)

      chords = self.score.flat.notes.stream()
      for chord_group in chords.groupElementsByOffset():
        for chord_part in chord_group:
          if chord_part.duration.isGrace:
            continue

          chord_part.lyrics = []

          notes = chord_part if chord_part.isChord else [chord_part]

          print_lyrics = False
          for note in notes:
            if hasattr(note, "show_lyric_") and note.show_lyric_:
              print_lyrics = True
              break

          if print_lyrics:
            lyrics = []
            for note in sorted(notes, reverse=True):
              if hasattr(note, "pred_lyric_"):
                lyrics.append(note.pred_lyric_)
              else:
                lyrics.append("X")

            for lyric in lyrics:
              chord_part.addLyric(lyric)

    else:
      chords = self.score.flat.notes.stream()
      for chord_group in chords.groupElementsByOffset():
        for chord_part in chord_group:
          if chord_part.duration.isGrace:
            continue

          chord_part.lyrics = []

          notes = chord_part if chord_part.isChord else [chord_part]

          print_lyrics = False
          for note in notes:
            note.color = note.true_color_
            if hasattr(note, "true_lyric_"):
              print_lyrics = True

          if print_lyrics:
            lyrics = []
            for note in sorted(notes, reverse=True):
              lyrics.append(note.true_lyric_)

            for lyric in lyrics:
              chord_part.addLyric(lyric)

    self.score.write(fp=fp)

  def __len__(self):
    return len(self.chords)

  def __getitem__(self, index):
    return self.chords[index]

  def __iter__(self):
    return iter(self.chords)

class Chord(object):
  def __init__(self, **kwargs):
    for key, value in kwargs.items():
      setattr(self, key, value)

    for i, note in enumerate(self.notes[1:], start=1):
      note.note_above = self.notes[i-1]

    for i, note in enumerate(self.notes[:-1], start=0):
      note.note_below = self.notes[i+1]

  def __len__(self):
    return len(self.notes)

  def __getitem__(self, index):
    return self.notes[index]

  def __iter__(self):
    return iter(self.notes)

class Note(object):
  def __init__(self, **kwargs):
    for key, value in kwargs.items():
      setattr(self, key, value)

  def pairs(self, voiceid_type):
    if voiceid_type == "true":
      return self.true_pairs
    elif voiceid_type == "neural":
      return self.neural_pairs
    elif voiceid_type == "envelope":
      return self.envelope_pairs
    elif voiceid_type == "proximity":
      return self.proximity_pairs
    elif voiceid_type == "poly":
      return self.poly_pairs
    elif voiceid_type == "test":
      return self.true_pairs

class Pairs():
  def __init__(self):
    self.left = []
    self.right = []

      # for note in chord:
      #   note.right_repeat = 0
      #   note.left_repeat = 0
      #
      #   chord_index = chord.index + 1
      #   while note.right_repeat < 4 and chord_index < len(self.chords):
      #     chord_ahead = self.chords[chord_index]
      #     chord_index += 1
      #
      #     if chord_ahead.beat_onset > note.beat_onset + beat_horizon:
      #       break
      #
      #     for n in chord_ahead:
      #       if n.pitch_space == note.pitch_space:
      #         note.right_repeat += 1
      #         break
      #
      #   chord_index = chord.index - 1
      #   while note.left_repeat < 4 and chord_index >= 0:
      #     chord_behind = self.chords[chord_index]
      #     chord_index -= 1
      #
      #     if chord_behind.beat_onset < note.beat_onset - beat_horizon:
      #       break
      #
      #     for n in chord_behind:
      #       if n.pitch_space == note.pitch_space:
      #         note.left_repeat += 1
      #         break

      # for note in chord:
      #   chord_index = chord.index + 1
      #   while chord_index < len(self.chords):
      #     for note1 in self.chords[chord_index]:
      #       if note.pitch_space == note1.pitch_space:
      #         note.repeat_right = note1
      #         note1.repeat_left = note
      #         break
      #     else:
      #       if (
      #         self.chords[chord_index].beat_onset - note.beat_offset > 
      #         beat_horizon
      #       ):
      #         break
      #
      #       chord_index += 1
      #       continue
      #
      #     break
