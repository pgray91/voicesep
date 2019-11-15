import theano
import theano.tensor as T


def binary_crossentropy(y_hat_var):

    y_var = T.matrix("y", dtype=theano.config.floatX)
    cost_var = T.nnet.binary_crossentropy(y_hat_var, y_var).mean()

    return cost_var, [y_var]


def max(y_hat_var, assignment_limit, margin):

    scores = y_hat_var.reshape(
        (
            y_hat_var.shape[0] // assignment_limit,
            assignment_limit
        )
    ).T

    score_positive = scores[0]
    score_negative = scores[1:][scores[1:].argmax(axis=0), T.arange(scores.shape[1])]

    return T.mean(T.maximum(0, margin - score_positive + score_negative)), []
