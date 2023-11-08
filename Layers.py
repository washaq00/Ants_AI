import numpy as np
from BasicLayer import Layer, relu, sigmoid


class DenseLayer(Layer):
    def __init__(self, input_size, output_size):
        super().__init__()
        self.weights = np.random.rand(input_size, output_size)
        self.bias = np.random.rand(input_size, output_size)

    def forward_prop(self, input_data):
        self.input = input_data
        self.output = np.dot(input_data, self.weights) + self.bias
        return self.output


class ActivationLayer(Layer):
    def __init__(self, activation):
        super().__init__()
        self.activation = activation

    def forward_prop(self, input_data):
        self.input = input_data
        self.output = self.activation(self.input)
        return self.output





