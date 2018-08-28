import numpy as np
import theano
import theano.tensor as T

class NeuralNetwork:

  def __init__(
    self, group_counts, ind_count, 
    pad_sizes, field_sizes, conv_activation,
    ind_layer, hidden_dimensions, merge,
    hidden_activations, output_activation,
    update_function, update_args, 
    margin, l2_reg, 
    assign_limit, batch_size, 
    mode
  ):
    # Convolutional Layer
    group_X_vars = [
      T.matrix("group_X_var%i" % i) for i in range(len(group_counts))
    ]

    self.convolutional_layers =  [
      ConvolutionalLayer(
        group_X_vars[i], assign_limit, batch_size, pad_sizes[i],
        field_sizes[i], group_counts[i], conv_activation,
      )
      for i in range(len(group_counts))
    ]

    # Individual Features Layer
    ind_X_var = T.matrix("ind_X_var")
    ind_a = ind_X_var
    concat_count = ind_count
    self.indiv_layers = []
    if ind_layer > 0:
      self.indiv_layers.append(
        NeuralLayer(
          ind_X_var, ind_count, ind_layer, hidden_activations
        )
      )
      ind_a = self.ind_layers[0].a 
      concat_count = ind_layer

    # Neural Layer
    X_var = T.concatenate(
      [ind_a] + [cl.c for cl in self.convolutional_layers],
      axis=1
    )

    dimensions = (sum(field_sizes) + concat_count,) + hidden_dimensions
    merge = (False,) + merge if merge else (False,) * (len(dimensions) - 1)
    assert len(merge) == len(dimensions) - 1

    layers = len(dimensions) - 1
    self.neural_layers = [None] * layers

    prev_a = X_var
    a = X_var

    activations = [hidden_activations] * (layers-1) + [output_activation]

    for l, m in zip(range(layers), merge):
      input_size = dimensions[l]
      output_size = dimensions[l+1]
      if m:
        input_size += dimensions[l-1]
        a = T.concatenate([a, prev_a], axis=1)
      prev_a = a[:, :dimensions[l]]

      self.neural_layers[l] = NeuralLayer(
        a, input_size, output_size, activations[l]
      )
      a = self.neural_layers[l].a

    params = []
    for convolutional_layer in self.convolutional_layers:
      params += [convolutional_layer.W, convolutional_layer.b]

    for indiv_layer in self.indiv_layers:
      params += [indiv_layer.W, indiv_layer.b]

    for neural_layer in self.neural_layers:
      params += [neural_layer.W, neural_layer.b]


    self.predict_model = theano.function(
      inputs=[*group_X_vars, ind_X_var],
      outputs=self.neural_layers[-1].a
    )

    # Cost function
    scores = self.neural_layers[-1].a
    # scores = scores.reshape((batch_size, assign_limit)).T
    scores = scores.reshape((scores.shape[0] // assign_limit, assign_limit)).T

    score_pos = scores[0]
    score_neg = scores[1:][
      # scores[1:].argmax(axis=0), T.arange(batch_size)
      scores[1:].argmax(axis=0), T.arange(scores.shape[1])
    ]
    cost = T.mean(T.maximum(0, margin - score_pos + score_neg))

    cost += l2_reg * (
      sum(
        T.power(convolutional_layer.W, 2).sum()
        for convolutional_layer in self.convolutional_layers
      ) +
      sum(
        T.power(indiv_layer.W, 2).sum()
        for indiv_layer in self.indiv_layers
      ) +
      sum(
        T.power(neural_layer.W, 2).sum()
        for neural_layer in self.neural_layers
      )
    )

    gparams = T.grad(cost, params)

    self.train_model = theano.function(
      inputs=[*group_X_vars, ind_X_var],
      outputs=cost,
      updates=update_function(params, gparams, **update_args),
      mode=mode
    )

  def read(self, network_file):
    with open("%s.npy" % network_file, "rb") as fp:
      for convolutional_layer in self.convolutional_layers:
        W_values = np.load(fp)
        b_values = np.load(fp)
        convolutional_layer.set_weights(W_values, b_values)

      for indiv_layer in self.indiv_layers:
        W_values = np.load(fp)
        b_values = np.load(fp)
        indiv_layer.set_weights(W_values, b_values)

      for neural_layer in self.neural_layers:
        W_values = np.load(fp)
        b_values = np.load(fp)
        neural_layer.set_weights(W_values, b_values)

  def write(self, network_file):
    with open("%s.npy" % network_file, "wb") as fp:
      for convolutional_layer in self.convolutional_layers:
        W_values, b_values = convolutional_layer.get_weights()
        np.save(fp, W_values)
        np.save(fp, b_values)

      for indiv_layer in self.indiv_layers:
        W_values, b_values = indiv_layer.get_weights()
        np.save(fp, W_values)
        np.save(fp, b_values)

      for neural_layer in self.neural_layers:
        W_values, b_values = neural_layer.get_weights()
        np.save(fp, W_values)
        np.save(fp, b_values)

  def predict(self, data):
    return self.predict_model(*data)

  def train(
    self, score_list, active_voices, features, 
    epochs, batch_size, cprint
  ):
    for convolutional_layer in self.convolutional_layers:
      convolutional_layer.random_weights()

    for indiv_layer in self.indiv_layers:
      indiv_layer.random_weights()

    for neural_layer in self.neural_layers:
      neural_layer.random_weights()

    active_voices.voiceid_type = "true"

    batch_index = 0
    for e in range(epochs):
      print("(%d / %d) Epoch" % (e + 1, epochs))

      train_num = 0
      train_total = sum(len(score) for score in score_list) // batch_size
      for i, score in enumerate(score_list):
        active_voices.beat_horizon = score.beat_horizon

        active_voices.update(score[0])

        for j, chord in enumerate(score[1:], start=1):
          active_voices.filter(chord.beat_onset)

          for _ in features.generate(score, chord, active_voices):
            continue

          batch_index += 1
          if (
            batch_index == batch_size or 
            (i + 1 == len(score_list) and j + 1 == len(score))
          ):
            data = features.release()
            # for did, d in enumerate(data):
            #   assert np.max(d) <= 1, "%d %s %f" % (did, str(np.unravel_index(np.argmax(d), d.shape)), np.max(d))
            #   assert np.min(d) >= 0, "%d %s %f" % (did, str(np.unravel_index(np.argmin(d), d.shape)), np.min(d))

            train_cost = self.train_model(*data)

            train_num += 1
            if cprint > 0 and train_num % cprint == 0:
              print(
                "  (%d / %d) Training Cost: %f" % 
                (train_num, train_total, train_cost)
              )

            batch_index = 0

          active_voices.update(chord)

        active_voices.clear()

    print()

class NeuralLayer:
  ACTIVATION_TYPES = {
    "sigmoid" : T.nnet.sigmoid,
    "softmax" : T.nnet.softmax,
    "relu" : T.nnet.relu,
  }

  def __init__(self, X_var, input_size, output_size, activation):
    self.input_size = input_size
    self.output_size = output_size
    self.activation = activation

    W_values = np.zeros((input_size, output_size), dtype=theano.config.floatX)
    self.W = theano.shared(value=W_values, name="W", borrow=True)

    b_values = np.zeros((output_size,), dtype=theano.config.floatX)
    self.b = theano.shared(value=b_values, name="b", borrow=True)

    z = T.dot(X_var, self.W) + self.b

    self.a = NeuralLayer.ACTIVATION_TYPES[activation](z) if activation else z

  def random_weights(self):
    r = np.sqrt(6 / (1 + self.input_size + self.output_size))
    if self.activation == "sigmoid":
      r *= 4

    W_values = np.asarray(
      np.random.uniform(-r, r, (self.input_size, self.output_size)),
      dtype=theano.config.floatX
    )
    b_values = np.zeros((self.output_size,), dtype=theano.config.floatX)

    self.set_weights(W_values, b_values)

  def set_weights(self, W_values, b_values):
    assert W_values.shape == self.W.get_value(borrow=True).shape, W_values.shape
    assert b_values.shape == self.b.get_value(borrow=True).shape 

    self.W.set_value(W_values, borrow=True)
    self.b.set_value(b_values, borrow=True)

  def get_weights(self):
    return self.W.get_value(borrow=True), self.b.get_value(borrow=True)

class ConvolutionalLayer:
  ACTIVATION_TYPES = {
    "sigmoid" : T.nnet.sigmoid,
    "softmax" : T.nnet.softmax,
    "relu" : T.nnet.relu,
  }

  def __init__(
    self, X_var, assign_limit, batch_size, 
    pad, field_size, depth, activation
  ):
    self.field_size = field_size
    self.depth = depth
    self.activation = activation

    W_values = np.zeros((depth, field_size), dtype=theano.config.floatX)
    self.W = theano.shared(value=W_values, name="W", borrow=True)

    b_values = np.zeros((field_size,), dtype=theano.config.floatX)
    self.b = theano.shared(value=b_values, name="b", borrow=True)

    z = T.dot(X_var, self.W) + self.b
    a = ConvolutionalLayer.ACTIVATION_TYPES[activation](z) if activation else z
    # a = a.reshape((batch_size * assign_limit, pad, field_size))
    a = a.reshape((a.shape[0] // pad, pad, field_size))

    # axis0 = T.arange(batch_size * assign_limit).repeat(field_size).reshape(
    #   (batch_size * assign_limit, field_size)
    # )
    axis0 = T.arange(a.shape[0]).repeat(field_size).reshape(
      (a.shape[0], field_size)
    )
    axis1 = a.argmax(axis=1)
    # axis2 = T.arange(field_size).repeat(batch_size * assign_limit).reshape(
    #   (field_size, batch_size * assign_limit)
    # ).T
    axis2 = T.arange(field_size).repeat(a.shape[0]).reshape(
      (field_size, a.shape[0])
    ).T

    self.c = a[axis0, axis1, axis2]

  def random_weights(self):
    r = np.sqrt(6 / (1 + self.field_size + self.depth))
    if self.activation == "sigmoid":
      r *= 4

    W_values = np.asarray(
      np.random.uniform(-r, r, (self.depth, self.field_size)),
      dtype=theano.config.floatX
    )
    b_values = np.zeros((self.field_size,), dtype=theano.config.floatX)

    self.set_weights(W_values, b_values)

  def set_weights(self, W_values, b_values):
    assert W_values.shape == self.W.get_value(borrow=True).shape
    assert b_values.shape == self.b.get_value(borrow=True).shape

    self.W.set_value(W_values, borrow=True)
    self.b.set_value(b_values, borrow=True)

  def get_weights(self):
    return self.W.get_value(borrow=True), self.b.get_value(borrow=True)
