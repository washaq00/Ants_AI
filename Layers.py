import numpy as np

def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-1 * x))

def relu(x):
    result = x
    result[x < 0] = 0
    return result

class Layer:
    def __init__(self):
        # super init makes it sure to be compiled in parents classes
        super().__init__()
        self.input = None
        self.output = None

    def forward(self, input):
        raise NotImplementedError


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


class NeuralNetwork():
    def __init__(self):
        self.layer1 = DenseLayer(input_size=2, output_size=5)
        self.layer2 = ActivationLayer(activation=relu())
        self.layer3 = DenseLayer(input_size=5, output_size=1)
        self.layer4 = ActivationLayer(#activation= #TODO )

    def calculate(self, input_data):
        return self.layer4(self.layer3(self.layer2(self.layer1(input_data))))




