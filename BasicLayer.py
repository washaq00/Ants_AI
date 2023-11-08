import numpy as np


class Layer:
    def __init__(self):
        # super init makes it sure to be compiled in parents classes
        super().__init__()
        self.input = None
        self.output = None

    def forward(self, input):
        raise NotImplementedError


def sigmoid(x):
        return 1.0 / (1.0 + np.exp(-1 * x))


def relu(x):
        result = x
        result[x < 0] = 0
        return result