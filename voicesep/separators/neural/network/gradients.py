import numpy as np
import theano
import theano.tensor as T

def sgd(params, cost_var, learning_rate=1):

    return [
        (param_var, param_var - learning_rate * T.grad(cost_var, param_var))
        for param_var in params
    ]

def adadelta(params, cost_var, rho=0.95, epsilon=1e-6):

    updates = []
    for param_var in params:

        gparam_var = T.grad(cost_var, param_var)

        param_sq = theano.shared(
            value=np.zeros(
                param_var.get_value(borrow=True).shape,
                dtype=theano.config.floatX
            ),
            borrow=True
        )

        delta_sq = theano.shared(
            value=np.zeros(
                param_var.get_value(borrow=True).shape,
                dtype=theano.config.floatX
            ),
            borrow=True
        )


        agrad = rho * param_sq + (1 - rho) * gparam_var ** 2
        delta = T.sqrt((delta_sq + epsilon) / (agrad + epsilon)) * gparam_var
        accudelta = rho * delta_sq + (1 - rho) * delta ** 2

        updates.append((param_var, param_var - delta))
        updates.append((gparam_var, param_var - delta))
        updates.append((gparam_var, param_var - delta))




  deltas_sq_next = [
    rho * dsq + (1 - rho) * d ** 2 
    for dsq, d in zip(deltas_sq, deltas)
  ]

  gparam_sq_updates = list(zip(gparams_sq, gparams_sq_next))
  delta_sq_updates = list(zip(deltas_sq, deltas_sq_next))
  param_updates = [(p, p - d) for p, d in zip(params, deltas)]
  return gparam_sq_updates + delta_sq_updates + param_updates
