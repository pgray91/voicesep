import theano.tensor as T


def binary_crossentropy(y_hat_var, y_var):

    return T.nnet.binary_crossentropy(y_hat_var, y_var).mean()
