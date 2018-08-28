import numpy as np
import theano
import theano.tensor as T

def sgd(params, gparams, lr=1.0):
  return [(p, p - lr * gp) for p, gp in zip(params, gparams)]

def adadelta(params, gparams, rho=0.95, epsilon=1e-6):
  gparams_sq = [
    theano.shared(
      value=np.zeros(p.get_value(borrow=True).shape, dtype=theano.config.floatX),
      borrow=True
    )
    for p in params
  ]
  deltas_sq = [
    theano.shared(
      value=np.zeros(p.get_value(borrow=True).shape, dtype=theano.config.floatX),
      borrow=True
    )
    for p in params
  ]

  gparams_sq_next = [
    rho * gpsq + (1 - rho) * gp ** 2 
    for gpsq, gp in zip(gparams_sq, gparams)
  ]

  deltas = [
    (T.sqrt(dsq + epsilon) / T.sqrt(gpsqn + epsilon)) * gp 
    for dsq, gpsqn, gp in zip(deltas_sq, gparams_sq_next, gparams)
  ]
  deltas_sq_next = [
    rho * dsq + (1 - rho) * d ** 2 
    for dsq, d in zip(deltas_sq, deltas)
  ]

  gparam_sq_updates = list(zip(gparams_sq, gparams_sq_next))
  delta_sq_updates = list(zip(deltas_sq, deltas_sq_next))
  param_updates = [(p, p - d) for p, d in zip(params, deltas)]
  return gparam_sq_updates + delta_sq_updates + param_updates

def adam(params, gparams, lr=1e-3, beta1=0.9, beta2=0.999, epsilon=1e-8):
  t_prev = theano.shared(np.asarray(0, dtype=theano.config.floatX))
  t = t_prev + 1

  m_t_prev = [
    theano.shared(
      value=np.zeros(p.get_value(borrow=True).shape, dtype=theano.config.floatX),
      borrow=True
    )
    for p in params
  ]
  v_t_prev = [
    theano.shared(
      value=np.zeros(p.get_value(borrow=True).shape, dtype=theano.config.floatX),
      borrow=True
    )
    for p in params
  ]

  m_t = [
    beta1 * mtp + (1 - beta1) * gp 
    for mtp, gp in zip(m_t_prev, gparams)
  ]
  v_t = [
    beta2 * vtp + (1 - beta2) * gp**2 
    for vtp, gp in zip(v_t_prev, gparams)
  ]

  bias_correct = [
    lr * T.sqrt(1 - beta2 ** t) / (1 - beta1 ** t) * 
    mt / (T.sqrt(vt) + epsilon)
    for mt, vt in zip(m_t, v_t)
  ]

  t_update = [(t_prev, t)]
  m_updates = list(zip(m_t_prev, m_t))
  v_updates = list(zip(v_t_prev, v_t))
  param_updates = [(p, p - bc) for p, bc in zip(params, bias_correct)]
  return t_update + m_updates + v_updates + param_updates

def adamax(params, gparams, lr=2e-3, beta1=0.9, beta2=0.999, epsilon=1e-8):
  t_prev = theano.shared(np.asarray(0, dtype=theano.config.floatX))
  t = t_prev + 1

  m_t_prev = [
    theano.shared(
      value=np.zeros(p.get_value(borrow=True).shape, dtype=theano.config.floatX),
      borrow=True
    )
    for p in params
  ]
  u_t_prev = [
    theano.shared(
      value=np.zeros(p.get_value(borrow=True).shape, dtype=theano.config.floatX),
      borrow=True
    )
    for p in params
  ]

  m_t = [
    beta1 * mtp + (1 - beta1) * gp 
    for mtp, gp in zip(m_t_prev, gparams)
  ]
  u_t = [
    T.maximum(beta2 * utp, abs(gp))
    for utp, gp in zip(u_t_prev, gparams)
  ]

  bias_correct = [
    (lr / (1 - beta1 ** t)) * 
    mt / (ut - epsilon)
    for mt, ut in zip(m_t, u_t)
  ]

  t_update = [(t_prev, t)]
  m_updates = list(zip(m_t_prev, m_t))
  u_updates = list(zip(u_t_prev, u_t))
  param_updates = [(p, p - bc) for p, bc in zip(params, bias_correct)]
  return t_update + m_updates + u_updates + param_updates
