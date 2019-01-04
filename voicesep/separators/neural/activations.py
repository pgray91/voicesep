import theano
import theano.tensor as T

linear = lambda X: X
sigmoid = T.nnet.sigmoid
relu = T.nnet.relu
softmax = T.nnet.softmax
