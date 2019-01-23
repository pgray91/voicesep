import logging
import numpy as np
import theano
import theano.tensor as T
import time

from voicesep.separators.neural.network import activations
from voicesep.separators.neural.network import costs
from voicesep.separators.neural.network import features
from voicesep.separators.neural.network import gradients

from voicesep.separators.neural.network.layer import Layer

logger = logging.getLogger(__name__)


class Network:

    def __init__(self):

        logger.debug("initializing")

        self.X_var = T.matrix("X", dtype=theano.config.floatX)
        self.y_var = T.vector("y", dtype=theano.config.floatX)

        self.dimensions = ()
        self.hidden_activations = None
        self.output_activation = None
        self.convolutional_layers = []
        self.simple_layers = []

        self.train_function = None
        self.predict_function = None

    def build(
        self,
        convolutional_dimensions,
        convolutional_counts,
        dimensions,
        hidden_activations,
        output_activation
    ):
        self.X_var = T.matrix("X", dtype=theano.config.floatX)
        self.y_var = T.vector("y", dtype=theano.config.floatX)

        self.X_conv_vars = []
        # just use self.layers
        self.convolutional_layers = []
        for i, convolutional_dimension, convolutional_count in enumerate(zip(convolutional_dimensions, convolutional_counts)):

            self.X_conv_vars.append(T.matrix("X_conv{}".format(i + 1)))

            self.convolutional_layers.append(
                Layer(
                    X_conv_vars[i], *convolutional_dimension, hidden_activations
                )
            )

            y_hat_var = self.convolutional_layers[-1].y_hat_var
            y_hat_var = (
                y_hat_var.reshape(
                    (y_hat_var.shape[0] // convolutional_count, convolutional_count, output_size)
                )
                .argmax(axis=1)
            )

            dimensions[0] += convolutional_dimension[1]
            self.X_var = T.concatenate([self.X_var, y_hat_var], axis=1)

        self.dimensions = dimensions
        self.hidden_activations = hidden_activations
        self.output_activation = output_activation

        next_input = self.X_var
        for i in range(len(dimensions) - 2):
            self.layers.append(
                Layer(
                    next_input,
                    dimensions[i],
                    dimensions[i+1],
                    hidden_activations
                )
            )
            next_input = self.layers[-1].y_hat_var

        self.layers.append(
            Layer(
                next_input,
                dimensions[-2],
                dimensions[-1],
                output_activation
            )
        )

    def compile(self, cost_type, cost_args, L2_reg, gradient_type, gradient_args):

        y_hat_var = self.layers[-1].y_hat_var.flatten()

        cost_function = getattr(costs, cost_type)
        cost_var = cost_function(y_hat_var, *cost_args)
        cost_var += L2_reg * sum(
            T.sum(T.pow(layer.W_var, 2))
            for layer in self.layers
        )

        gradient_function = getattr(gradients, gradient_type)

        params = []
        for layer in self.layers:
            params.extend(layer.params)

        updates = gradient_function(params, cost_var, *gradient_args)

        self.train_function = theano.function(
            inputs=self.X_vars,
            outputs=cost_var,
            updates=updates
        )

        self.predict_function = theano.function(
          inputs=self.X_vars,
          outputs=y_hat_var
        )

    def train(self, dataset, epochs, batch_size, verbosity=0):

        for layer in self.layers:
            layer.random_weights()

        batch_count = (len(dataset) - 1) // batch_size + 1

        checkpoint = time.time()
        for epoch in range(1, epochs + 1):
            cost = 0
            for i in range(batch_count):
                batches = dataset[i * batch_size: (i + 1) * batch_size]

                cost += self.train_function(*batches)

            if verbosity and int(time.time() - checkpoint) > verbosity:
                logger.info(
                    "epoch {}/{} | cost={}".format(epoch, epochs, cost / batch_count)
                )
                checkpoint = time.time()

    def predict(self, X):

        return self.predict_function(X)

    def read(self, name):

        with open(name, "rb") as fp:
            dimensions = tuple(np.load(fp))
            hidden_activations = str(np.load(fp))
            output_activation = str(np.load(fp))

            self.build(dimensions, hidden_activations, output_activation)

            for layer in self.layers:
                W = np.load(fp)
                b = np.load(fp)
                layer.set_weights(W, b)

    def write(self, name):

        with open(name, "wb") as fp:
            np.save(fp, self.dimensions)
            np.save(fp, self.hidden_activations)
            np.save(fp, self.output_activation)

            for layer in self.layers:
                W, b = layer.get_weights()
                np.save(fp, W)
                np.save(fp, b)

__all__ = [
    "activations",
    "costs",
    "features",
    "gradients",
    
    "layer"
]
