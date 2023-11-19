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

    def forward(self, *input_data):
        results = input_data
        for layer in self.layers:
            results = layer[0].forward(results)
        return results

    def mutate(self, mutation_chance=60):
        for layer, _ in self.layers:
            if not _:
                for i in range(layer.input_size):
                    for j in range(layer.output_size):
                        if mutation_chance > np.random.randint(0, 100):
                            layer.weights[i,j] = np.random.randn(1, 1)
                            layer.bias[0, j] = np.random.randn(1, 1)

    def copy(self, previous_Bot):
        self.layers.clear()
        self.layers = previous_Bot.copy()
        self.mutate()

