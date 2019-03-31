import logging
import numpy as np
import theano
import theano.tensor as T
import time

from voicesep.separators.neural.network import activations
from voicesep.separators.neural.network import costs
from voicesep.separators.neural.network import features
from voicesep.separators.neural.network import gradients

from voicesep.separators.neural.network.dataset import Dataset
from voicesep.separators.neural.network.features import Features
from voicesep.separators.neural.network.layer import Layer

logger = logging.getLogger(__name__)


class Network:

    def __init__(self):

        logger.debug("initializing")

        self.X_vars = []

        self.dimensions = ()
        self.hidden_activations = None
        self.output_activation = None
        self.layers = []

        self.train_function = None
        self.predict_function = None

    def build(self, dimensions, hidden_activations, output_activation):

        self.X_vars = []

        self.dimensions = dimensions
        self.hidden_activations = hidden_activations
        self.output_activation = output_activation
        self.layers = []

        self.train_function = None
        self.predict_function = None

        convolutional_inputs = []
        convolutional_size = 0
        for i, convolution in enumerate(dimensions):

            if not isinstance(convolution, tuple):
                break

            input_size, output_size, depth = convolution

            self.X_vars.append(
                T.matrix("X_var{}".format(i + 1), dtype=theano.config.floatX)
            )

            self.layers.append(
                Layer(
                    self.X_vars[-1],
                    input_size,
                    output_size,
                    hidden_activations
                )
            )

            y_hat_var = self.layers[-1].y_hat_var
            y_hat_var = (
                y_hat_var.reshape(
                    (
                        y_hat_var.shape[0] // depth,
                        depth,
                        output_size
                    )
                )
                .argmax(axis=1)
            )

            convolutional_inputs.append(y_hat_var)
            convolutional_size += output_size

        dimensions = list(dimensions[i:])
        dimensions[0] += convolutional_size

        activations = [hidden_activations] * (len(dimensions) - 2) + [output_activation]

        self.X_vars.append(
            T.matrix("X_var{}".format(i + 1), dtype=theano.config.floatX)
        )
        next_input = T.concatenate([*convolutional_inputs, self.X_vars[-1]], axis=1)
        for i in range(len(dimensions) - 1):
            self.layers.append(
                Layer(
                    next_input,
                    dimensions[i],
                    dimensions[i+1],
                    activations[i]
                )
            )
            next_input = self.layers[-1].y_hat_var

    def compile(self, cost_type, cost_args, gradient_type, gradient_args, L2_reg):

        y_hat_var = self.layers[-1].y_hat_var

        cost_function = getattr(costs, cost_type)
        cost_var, cost_inputs = cost_function(y_hat_var, *cost_args)
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
            inputs=[*self.X_vars, *cost_inputs],
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
                cost += self.train_function(
                    *dataset[i * batch_size: (i + 1) * batch_size]
                )

            if verbosity and int(time.time() - checkpoint) > verbosity:
                logger.info(
                    "epoch {}/{} | cost={}".format(epoch, epochs, cost / batch_count)
                )
                checkpoint = time.time()

    def predict(self, X):

        return self.predict_function(*X)

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

        y_hat_var = self.layers[-1].y_hat_var

        self.predict_function = theano.function(
            inputs=self.X_vars,
            outputs=y_hat_var
        )

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

    "Dataset",
    "Features",
    "Layer",
    "Network"
]
