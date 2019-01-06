import logging
import numpy as np
import theano
import theano.tensor as T
import time

from voicesep.separators.neural import activations
from voicesep.separators.neural import costs
from voicesep.separators.neural import gradients
from voicesep.separators.neural.note_level.network.layer import Layer

logger = logging.getLogger(__name__)

class Network:

    def __init__(self):
        self.X_var = T.matrix("X", dtype=theano.config.floatX)
        self.y_var = T.matrix("y", dtype=theano.config.floatX)
        self.neural_layers = []
        self.params = []

    def build(self, dimensions, hidden_activations, output_activation):

        next_input = self.X_var
        for i in range(len(dimensions) - 2):
            self.neural_layers.append(
                NeuralLayer(
                    next_input,
                    dimensions[i:i+2],
                    getattr(activations, hidden_activations)
                )
            )
            self.params.extend(self.neural_layers[-1].params)
            next_input = self.neural_layers[-1].y_hat_var

        self.neural_layers.append(
            NeuralLayer(
                next_input,
                dimensions[-2:],
                getattr(activations, output_activation)
            )
        )

    def compile(self, cost_type, L2_reg, gradient_type, gradient_args):

        cost_type, L2_reg = cost
        gradient_type, gradient_args = gradient

        y_hat_var = self.neural_layers[-1].y_hat_var

        cost_function = getattr(costs, cost_type)
        cost_var = cost_function(self.y_var, y_hat_var)
        cost_var += L2_reg * sum(
            T.sum(T.pow(neural_layer.W_var, 2))
            for neural_layer in self.neural_layers
        )

        gradient_function = getattr(gradients, gradient_type)
        gradients = gradient_function(self.params, cost_var, *gradient_args)

        self.train_function = theano.function(
            inputs=[self.X_var, self.y_var],
            outputs=cost_var,
            updates=gradients
        )

        self.predict_function = theano.function(
          inputs=[self.X_var],
          outputs=y_hat_var
        )

    def train(self, X, y, epochs, batch_size, verbosity=0):

        for neural_layer in self.neural_layers:
            neural_layer.random_weights()

        batch_count = (len(X) - 1) // batch_size + 1

        checkpoint = time.time()
        for epoch in range(1, epochs + 1):
            cost = 0
            for i in range(batch_count):
                X_batch = X[i * batch_size: (i + 1) * batch_size]
                y_batch = y[i * batch_size: (i + 1) * batch_size]

                cost += self.train_function(X_batch, y_batch)

            if verbose and int(time.time() - checkpoint) > verbosity:
                logger.info(
                    "epoch {}/{} | cost={}".format(epoch, epochs, cost / batch_count)
                )
                checkpoint = time.time()

    def predict(self, X):

        return self.predict_function(X)

    def read(self, network):

        with open("{}.npy".format(network), "rb") as fp:
            for neural_layer in self.neural_layers:
                W = np.load(fp)
                b = np.load(fp)
                neural_layer.set_weights(W, b)

    def write(self, network):

        with open("{}.npy".format(network), "wb") as fp:
            for neural_layer in self.neural_layers:
                W, b = neural_layer.get_weights()
                np.save(fp, W)
                np.save(fp, b)
