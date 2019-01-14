import logging
import numpy as np
import theano
import theano.tensor as T

from voicesep.separators.neural.network import activations

logger = logging.getLogger(__name__)


class Layer(abc.ABC):

    @abs.abstractmethod
    def random_weights(self):

        pass

    @abs.abstractmethod
    def set_weights(self, W, b):

        pass

    @abs.abstractmethod
    def get_weights(self):

        pass

