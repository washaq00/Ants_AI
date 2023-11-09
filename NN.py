from Layers import DenseLayer, ActivationLayer
from BasicLayer import relu, sigmoid

class NeuralNetwork():
    def __init__(self):
        self.layer1 = DenseLayer(input_size=2, output_size=5)
        # self.layer2 = ActivationLayer(activation=relu)
        self.layer3 = DenseLayer(input_size=5, output_size=2)
        # self.layer4 = ActivationLayer(activation=relu)

    def calculate(self, *input_data):
        # results = self.layer4.forward_prop(self.layer3.forward_prop(self.layer2.forward_prop(self.layer1.forward_prop(input_data))))
        results = self.layer3.forward_prop(self.layer1.forward_prop(input_data))

        # print(results)
        return results

# Test NN

# if __name__ == '__main__':
#     NN = NeuralNetwork()
#     NN.calculate()