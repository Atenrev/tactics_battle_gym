import numpy as np


def relu(x):
    return max(0.0, x)


v_relu = np.vectorize(relu)


def sigmoid(v):
    return 1 / (1+np.exp(-v))


v_sigmoid = np.vectorize(sigmoid)