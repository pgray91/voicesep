import numpy as np
import theano

from voicesep.separators.neural.note_level.features import Features
from voicesep.separators.neural.note_level.dataset import Dataset
from voicesep.separators.neural.note_level.neural_network import (
  NeuralNetwork
)

def separate(
  score, active_voices, features, network,
  conv_limit, div_limit, allow_cross, assignment_threshold
):
  active_voices.voiceid_type = "neural"
  active_voices.beat_horizon = score.beat_horizon

  active_voices.update(score[0])
  for chord in score[1:]:
    active_voices.filter(chord.beat_onset)

    data, active_subset = features.generate(
      chord, active_voices, get_labels=False
    )
    voice_count = len(active_subset) + 1

    ranks = network.predict(data).reshape(len(chord), voice_count)
    voice_mask = np.ones((ranks.shape))

    voice_limits = [div_limit - voice.div_count for voice in active_subset]
    note_count = len(chord)

    # Pseudo polyphony
    for note_index, note in enumerate(chord):
      if note.repeat_behind and note.repeat_count > 4:
        for voice_index, voice in enumerate(active_subset):
          if voice.note is note.repeat_behind:
            voice_mask[note_index, :-1] = 0
            voice_mask[:, voice_index] = 0
            voice_mask[note_index, voice_index] = 1
            ranks[note_index, voice_index] = 1
            break

      else:
        for voice_index, voice in enumerate(active_subset):
          if voice.note.repeat_ahead and voice.note.repeat_count > 4:
            if voice.note.pitch_space < note.pitch_space:
              voice_mask[note_index, voice_index:-1] = 0
            else:
              voice_mask[note_index, 0:voice_index+1] = 0
            break


    while note_count:
      max_flat_i = np.argmax(np.multiply(ranks, voice_mask))
      note_index, voice_index = np.unravel_index(max_flat_i, ranks.shape)

      max_prob = ranks[note_index, voice_index]
      assert max_prob != 0

      if voice_index < voice_count - 1 and max_prob > assignment_threshold:
        note = chord[note_index]
        voice = active_subset[voice_index]

        note.neural_pairs.left.append(voice.note)
        voice.note.neural_pairs.right.append(note)
        voice_mask[note_index, voice_index] = 0

        if conv_limit > 0 and len(note.neural_pairs.left) == conv_limit:
          voice_mask[note_index, :] = 0
          note_count -= 1

        if div_limit > 0:
          assert voice_limits[voice_index] != 0
          voice_limits[voice_index] -= 1
          if voice_limits[voice_index] == 0:
            voice_mask[:, voice_index] = 0

        if not allow_cross:
          for i in range(len(chord)):
            if i < note_index:
              voice_mask[i, voice_index + 1:-1] = 0
            elif i > note_index:
              voice_mask[i, :voice_index] = 0

      else:
        voice_mask[note_index, :] = 0
        note_count -= 1

    active_voices.update(chord)

  active_voices.clear()
