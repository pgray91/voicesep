import numpy as np
import theano
import theano.tensor as T

class NeuralNetwork:
  def __init__(
    self, dimensions, merge,
    hidden_activations, output_activation,
    update_function, update_args, 
    l2_reg, mode
  ):
    merge = (False,) + merge if merge else (False,) * (len(dimensions) - 1)
    assert len(merge) == len(dimensions) - 1

    layers = len(dimensions) - 1
    self.neural_layers = [None] * layers

    X_var = T.matrix("X_var")
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
    for neural_layer in self.neural_layers:
      params += [neural_layer.W, neural_layer.b]

    self.predict_model = theano.function(
      inputs=[X_var],
      outputs=self.neural_layers[-1].a
    )

    # Cost Function
    Y_var = T.wvector("Y_var")
    prob = self.neural_layers[-1].a.flatten(1)

    cost = -(
      (T.dot(T.log(prob), Y_var) + T.dot(T.log(1 - prob), 1 - Y_var)) /
      T.cast(prob.shape[0], theano.config.floatX)
    )

    cost += sum(
      T.power(neural_layer.W, 2).sum()
      for neural_layer in self.neural_layers
    ) * l2_reg

    gparams = T.grad(cost, params)

    self.X = theano.shared(
      value=np.empty((0, dimensions[0]), dtype=theano.config.floatX)
    )
    self.Y = theano.shared(value=np.empty((0,), dtype=theano.config.floatX))
    Y_int16 = T.cast(self.Y, "int16")

    batch_size_var = T.iscalar()
    i_var = T.iscalar()
    self.train_model = theano.function(
      inputs=[i_var, batch_size_var],
      outputs=cost,
      updates=update_function(params, gparams, **update_args),
      givens={
        X_var: self.X[i_var * batch_size_var : (i_var + 1) * batch_size_var],
        Y_var: Y_int16[i_var * batch_size_var : (i_var + 1) * batch_size_var]
      },
      mode=mode
    )

  def read(self, network_file):
    with open("%s.npy" % network_file, "rb") as fp:
      for neural_layer in self.neural_layers:
        W_values = np.load(fp)
        b_values = np.load(fp)
        neural_layer.set_weights(W_values, b_values)

  def write(self, network_file):
    with open("%s.npy" % network_file, "wb") as fp:
      for neural_layer in self.neural_layers:
        W_values, b_values = neural_layer.get_weights()
        np.save(fp, W_values)
        np.save(fp, b_values)

  def predict(self, X):
    return self.predict_model(X)

  def train(self, dataset, epochs, batch_size, cprint):
    for neural_layer in self.neural_layers:
      neural_layer.random_weights()

    data_features = dataset.features[:]
    data_labels = dataset.labels[:]

    self.X.set_value(data_features, borrow=True)
    self.Y.set_value(data_labels, borrow=True)

    batch_total = (len(data_features) - 1) // batch_size + 1
    for e in range(epochs):
      print("(%d / %d) Epoch" % (e + 1, epochs))
      
      for batch_index in range(batch_total):
        train_cost = self.train_model(batch_index, batch_size)

        if cprint > 0 and (batch_index + 1) % cprint == 0:
          print(
            "  (%d / %d) Training Cost: %f" % 
            (batch_index + 1,  batch_total, train_cost)
          )

    print()

class NeuralLayer:
  ACTIVATION_TYPES = {
    "sigmoid" : T.nnet.sigmoid,
    "softmax" : T.nnet.softmax
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
    assert W_values.shape == self.W.get_value(borrow=True).shape
    assert b_values.shape == self.b.get_value(borrow=True).shape

    self.W.set_value(W_values, borrow=True)
    self.b.set_value(b_values, borrow=True)

  def get_weights(self):
    return self.W.get_value(borrow=True), self.b.get_value(borrow=True)
