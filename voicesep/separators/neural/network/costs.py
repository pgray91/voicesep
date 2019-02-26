import theano.tensor as T


def binary_crossentropy(y_hat_var):

    y_var = T.vector("y_var", dtype=theano.config.floatX)
    cost_var = T.nnet.binary_crossentropy(y_hat_var, y_var).mean()

    return cost_var, y_var

def max(y_hat_var, assignment_limit):

    scores = y_hat_var.reshape((y_hat_var.shape[0] // assignment_limit, assignment_limit)).T

    pass
