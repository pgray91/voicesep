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
        self.layers = []

        self.train_function = None
        self.predict_function = None

    def build_convolution(self, count, dimensions, vector_count, activation):

        X_conv_vars = [T.matrix("X_conv{}".format(i + 1) for i in range(count))]
        convolution_layers = [
            layers.Convolutional(
                X_conv_vars[i], *dimensions, vector_count, activation
            )
            for i in range(count)
        ]

    def build(
        self,
        dimensions,
        hidden_activations,
        output_activation
    ):

        self.dimensions = dimensions
        self.hidden_activations = hidden_activations
        self.output_activation = output_activation
        self.convolutional_layers = []
        self.simple_layers = []

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

    def compile(self, cost_type, L2_reg, gradient_type, gradient_args):

        y_hat_var = self.layers[-1].y_hat_var.flatten()

        cost_function = getattr(costs, cost_type)
        cost_var = cost_function(self.y_var, y_hat_var)
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
            inputs=[self.X_var, self.y_var],
            outputs=cost_var,
            updates=updates
        )

        self.predict_function = theano.function(
          inputs=[self.X_var],
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
                X_batch, y_batch = dataset[i * batch_size: (i + 1) * batch_size]

                cost += self.train_function(X_batch, y_batch)

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
