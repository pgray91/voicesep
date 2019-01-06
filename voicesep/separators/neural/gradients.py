import numpy as np
import theano
import theano.tensor as T


def sgd(params, cost_var, learning_rate=1.0):

    grads = [T.grad(cost_var, param_var) for param_var in params]

    return [
        (param_var, param_var - learning_rate * grad_var)
        for param_var, grad_var in zip(params, grads)
    ]


def adadelta(params, cost_var, rho=0.95, epsilon=1e-6):

    """
        Zeiler, M. D. 2012.
        ADADELTA: An adaptive learning rate method.
        arXiv:1212.5701.
    """

    grads = [T.grad(cost_var, param_var) for param_var in params]

    updates = []
    for param_var, grad_var in zip(params, grads):

        accu_var = theano.shared(
            np.zeros(
                param_var.get_value(borrow=True).shape,
                dtype=theano.config.floatX
            )
        )

        delta_var = theano.shared(
            np.zeros(
                param_var.get_value(borrow=True).shape,
                dtype=theano.config.floatX
            )
        )

        accu_update_var = (
            rho * accu_var + (1 - rho) * grad_var ** 2
        )
        param_update_var = (
            T.sqrt((delta_var + epsilon) / (accu_update_var + epsilon)) * grad_var
        )
        delta_update_var = (
            rho * delta_var + (1 - rho) * param_update_var ** 2
        )

        updates.extend(
            (accu_var, accu_update_var),
            (delta_var, delta_update_var),
            (param_var, param_var - param_update_var)
        )

    return updates
