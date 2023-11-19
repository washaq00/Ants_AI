from Layers import DenseLayer, ActivationLayer
from BasicLayer import relu, sigmoid, tanh
import numpy as np



class NeuralNetwork():
    def __init__(self):
        self.layers: list[tuple] = []
        self.layers.append((DenseLayer(input_size=3, output_size=10), False))
        self.layers.append((ActivationLayer(activation=tanh), True))
        self.layers.append((DenseLayer(input_size=10, output_size=3), False))
        self.layers.append((ActivationLayer(activation=tanh), True))

    def calculate(self, *input_data):
        results = input_data
        for layer in self.layers:
            results = layer[0].forward(results)
        return results

    def mutate(self, mutation_chance):
        for layer in self.layers:
            if not layer[1] and mutation_chance > np.random.randint(0,100):
                for neuron in layer[0].input_size:
                    layer[0].weights = np.random.randn(layer[0].input_size, layer[0].output_size)
                    layer[0].bias = np.random.randn(1, layer[0].output_size)
