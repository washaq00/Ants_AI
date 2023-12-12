from Layers import DenseLayer, ActivationLayer
from BasicLayer import relu, sigmoid, tanh
import numpy as np



class NeuralNetwork():

    """
    The more simple the architecture is, the better ant learns
    """

    def __init__(self):
        self.layers: list[tuple] = []
        self.layers.append((DenseLayer(input_size=2, output_size=5), False))
        self.layers.append((ActivationLayer(activation=tanh), True))
        self.layers.append((DenseLayer(input_size=5, output_size=3), False))
        self.layers.append((ActivationLayer(activation=tanh), True))
        # self.layers.append((DenseLayer(input_size=10, output_size=3), False))
        # self.layers.append((ActivationLayer(activation=tanh), True))

    def forward(self, *input_data):
        results = input_data
        for layer in self.layers:
            results = layer[0].forward(results)
        return results

