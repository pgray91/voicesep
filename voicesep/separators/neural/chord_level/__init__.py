import numpy as np

from voicesep.separators.neural.chord_level.features import Features
from voicesep.separators.neural.chord_level.neural_network import (
  NeuralNetwork
)

def separate(score, active_voices, features, network, cprint):
  active_voices.voiceid_type = "neural"
  active_voices.beat_horizon = score.beat_horizon

  active_voices.update(score[0])
  chord_num = 0
  for chord in score[1:]:
    active_voices.filter(chord.beat_onset)

    max_data = []
    max_assignments = []
    for assignments in features.generate(score, chord, active_voices):
      data = features.release()
      result = network.predict(data)
      row = np.argmax(result)

      max_data.append(result[row])
      max_assignments.append(assignments[row])

    max_value = max(max_data)
    row = max_data.index(max_value)
    max_assignment = max_assignments[row]
    for note, voices in zip(chord, max_assignment):
      for voice in voices:
        if voice:
          note.neural_pairs.left.append(voice.note)
          voice.note.neural_pairs.right.append(note)

    active_voices.update(chord)

    chord_num += 1
    if cprint > 0 and chord_num % cprint == 0:
      print("  (%d / %d) Chord" % (chord_num, len(score)))

  active_voices.clear()
