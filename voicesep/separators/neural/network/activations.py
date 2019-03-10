import theano.tensor as T


def linear(X):

    return X


def sigmoid(X):

    return T.nnet.sigmoid(X)


def relu(X):

    return T.nnet.relu(X)
