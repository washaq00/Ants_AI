import numpy as np
from BasicLayer import Layer


class DenseLayer(Layer):
    def __init__(self, input_size, output_size):
        super().__init__()
        self.input_size = input_size
        self.output_size = output_size
        self.weights = np.random.randn(input_size, output_size) - 0.5
        self.bias = np.random.randn(1, output_size) - 0.5

    def forward(self, input_data):
        return np.dot(input_data, self.weights) + self.bias


class ActivationLayer(Layer):
    def __init__(self, activation):
        super().__init__()
        self.activation = activation

    def forward(self, input_data):
        return self.activation(input_data)




