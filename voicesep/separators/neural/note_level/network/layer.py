import logging

logger = logging.getLogger(__name__)

class Layer:

    def __init__(self, X_var, dimensions):

        assert len(dimensions) == 2

        self.dimensions = dimensions

        W = np.empty(dimensions, dtype=theano.config.floatX)
        b = np.empty(dimensions[1:], dtype=theano.config.floatX)

        self.W_var = theano.shared(value=W, name="W", borrow=True)
        self.b_var = theano.shared(value=b, name="b", borrow=True)

        self.params = [self.W_var, self.b_var]

        self.y_hat_var = activation(T.dot(X_var, self.W_var) + self.b_var)

    def random_weights(self):

        random_num = np.sqrt(6 / sum(dimensions))

        W = np.asarray(
            np.random.uniform(
                -random_num, random_num, self.dimensions
            ),
            dtype=theano.config.floatX
        )
        b = np.zeros(self.dimensions[1:], dtype=theano.config.floatX)

        self.set_weights(W, b)

    def set_weights(self, W, b):

        assert W.shape == self.W_var.get_value(borrow=True).shape
        assert b.shape == self.b_var.get_value(borrow=True).shape

        self.W_var.set_value(W, borrow=True)
        self.b_var.set_value(b, borrow=True)

    def get_weights(self):

        return self.W_var.get_value(borrow=True), self.b_var.get_value(borrow=True)
