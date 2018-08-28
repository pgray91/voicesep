import unittest
import numpy as np
import theano
import voicesep as vs
import voicesep.score
import voicesep.active_voices
import voicesep.separators.maximum_margin.features
import voicesep.separators.maximum_margin.neural_network
import voicesep.utils.gradients as grad

# Run experiments for all the main update functions
class TestNetwork(unittest.TestCase):
  def setUp(self):
    self.score1 = vs.score.Score(
      "test_score1.xml", beat_horizon=4, is_one_to_many=True
    )
    self.score2 = vs.score.Score(
      "test_score2.xml", beat_horizon=4, is_one_to_many=True
    )
    self.score3 = vs.score.Score(
      "test_score3.xml", beat_horizon=4, is_one_to_many=True
    )
    self.train_scores = [self.score1, self.score3]

    self.features = vs.neural.note_level.Features()
    #   max_rows=64, assign_limit=64, random_limit=1000,
    #   conv_limit=1, div_limit=1, pp_limit=0, 
    #   lookback=True, allow_cross=False, batch_size=2
    # )
    self.active_voices = vs.active_voices.ActiveVoices(
      div_limit=1,
      lookback_inc=1, lookback_proxs=(20, -1), allow_overlap=True
    )

  def test_00_1H(self):
    expected_voices = [
      (0,0), (0,1), (0,2)   
    ]

    network = vs.separators.neural.note_level.neural_network.NeuralNetwork(
      (vs.neural.note_level.Features.COUNT, 20, 1), (False,),
      "sigmoid", "sigmoid",
      grad.sgd, {"lr" : 0.1}, 
      l2_reg=0.001, mode="FAST_RUN"
    )

    network.train(self.dataset, epochs=2, batch_size=2, cprint=1)

    self.active_voices.voiceid_type = "neural"
    self.active_voices.update(self.score2[0])

    features_generator = self.features.generate(
      self.score2, self.score2[1], self.active_voices
    )

    assignments = next(features_generator)
    data = self.features.release()

    row = np.argmax(network.predict(data))
    max_assignment = assignments[row]

    i = 0
    for voices in max_assignment:
      for voice in voices:
        with self.subTest(test_id="Voices %d" % i):
          self.assertEqual(
            (voice.note.chord_index, voice.note.index), expected_voices[i]
          )
          i += 1


  def test_01_2H(self):
    expected_voices = [
      (0,0), (0,1), (0,2)   
    ]

    network = vs.separators.neural.note_level.neural_network.NeuralNetwork(
      (vs.neural.note_level.Features.COUNT, 20, 1), (False,),
      "sigmoid", "sigmoid",
      grad.sgd, {"lr" : 0.1}, 
      l2_reg=0.001, mode="FAST_RUN"
    )

    network.train(self.dataset, epochs=2, batch_size=2, cprint=1)

    self.active_voices.voiceid_type = "neural"
    self.active_voices.update(self.score2[0])

    features_generator = self.features.generate(
      self.score2, self.score2[1], self.active_voices
    )

    assignments = next(features_generator)
    data = self.features.release()

    row = np.argmax(network.predict(data))
    max_assignment = assignments[row]

    i = 0
    for voices in max_assignment:
      for voice in voices:
        with self.subTest(test_id="Voices %d" % i):
          self.assertEqual(
            (voice.note.chord_index, voice.note.index), expected_voices[i]
          )
          i += 1

  def test_02_2H_2C(self):
    expected_voices = [
      (0,0), (0,1), (0,2)   
    ]

    network = vs.separators.neural.note_level.neural_network.NeuralNetwork(
      (vs.neural.note_level.Features.COUNT, 20, 1), (False,),
      "sigmoid", "sigmoid",
      grad.sgd, {"lr" : 0.1}, 
      l2_reg=0.001, mode="FAST_RUN"
    )

    network.train(self.dataset, epochs=2, batch_size=2, cprint=1)

    self.active_voices.voiceid_type = "neural"
    self.active_voices.update(self.score2[0])

    features_generator = self.features.generate(
      self.score2, self.score2[1], self.active_voices
    )

    assignments = next(features_generator)
    data = self.features.release()

    row = np.argmax(network.predict(data))
    max_assignment = assignments[row]

    i = 0
    for voices in max_assignment:
      for voice in voices:
        with self.subTest(test_id="Voices %d" % i):
          self.assertEqual(
            (voice.note.chord_index, voice.note.index), expected_voices[i]
          )
          i += 1

  def test_03_2H_2C(self):
    expected_voices = [
      (0,0), (0,1), (0,2)   
    ]

    network = vs.separators.neural.note_level.neural_network.NeuralNetwork(
      (vs.neural.note_level.Features.COUNT, 20, 1), (False,),
      "sigmoid", "sigmoid",
      grad.sgd, {"lr" : 0.1}, 
      l2_reg=0.001, mode="FAST_RUN"
    )

    network.train(self.dataset, epochs=2, batch_size=2, cprint=1)

    self.active_voices.voiceid_type = "neural"
    self.active_voices.update(self.score2[0])

    features_generator = self.features.generate(
      self.score2, self.score2[1], self.active_voices
    )

    assignments = next(features_generator)
    data = self.features.release()

    row = np.argmax(network.predict(data))
    max_assignment = assignments[row]

    i = 0
    for voices in max_assignment:
      for voice in voices:
        with self.subTest(test_id="Voices %d" % i):
          self.assertEqual(
            (voice.note.chord_index, voice.note.index), expected_voices[i]
          )
          i += 1

  def test_04_1H_1I(self):
    expected_voices = [
      (0,0), (0,1), (0,2)   
    ]

    network = vs.separators.neural.note_level.neural_network.NeuralNetwork(
      (vs.neural.note_level.Features.COUNT, 20, 1), (False,),
      "sigmoid", "sigmoid",
      grad.sgd, {"lr" : 0.1}, 
      l2_reg=0.001, mode="FAST_RUN"
    )

    network.train(self.dataset, epochs=2, batch_size=2, cprint=1)

    self.active_voices.voiceid_type = "neural"
    self.active_voices.update(self.score2[0])

    features_generator = self.features.generate(
      self.score2, self.score2[1], self.active_voices
    )

    assignments = next(features_generator)
    data = self.features.release()

    row = np.argmax(network.predict(data))
    max_assignment = assignments[row]

    i = 0
    for voices in max_assignment:
      for voice in voices:
        with self.subTest(test_id="Voices %d" % i):
          self.assertEqual(
            (voice.note.chord_index, voice.note.index), expected_voices[i]
          )
          i += 1

  def test_05_sizes(self):
    expected_sizes = [
      (45,20), (65,10), (30,6), (6, 1)  
    ]

    network = vs.separators.neural.note_level.neural_network.NeuralNetwork(
      (vs.neural.note_level.Features.COUNT, 20, 1), (False,),
      "sigmoid", "sigmoid",
      grad.sgd, {"lr" : 0.1}, 
      l2_reg=0.001, mode="FAST_RUN"
    )

    for i, neural_layer in enumerate(network.neural_layers):
      with self.subTest(test_id="Layer %d" % i):
        self.assertEqual(
          (neural_layer.input_size, neural_layer.output_size),
          expected_sizes[i]
        )


if __name__ == "__main__":
  unittest.main()
