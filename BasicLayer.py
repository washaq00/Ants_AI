import numpy as np


class Layer:
    def __init__(self):
        # super init makes it sure to be compiled in parents classes
        self.input_size = None
        self.output_size = None

    def forward(self, input):
        raise NotImplementedError


def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-1 * x))


def relu(x):
    return np.maximum(0,x)


def tanh(x):
    return np.tanh(x)
