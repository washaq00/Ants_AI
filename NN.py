from Layers import DenseLayer, ActivationLayer

class NeuralNetwork():
    def __init__(self):
        self.layer1 = DenseLayer(input_size=2, output_size=5)
        self.layer2 = ActivationLayer(activation=relu())
        self.layer3 = DenseLayer(input_size=5, output_size=1)
        self.layer4 = ActivationLayer(#activation= #TODO )

    def calculate(self, input_data):
        return self.layer4(self.layer3(self.layer2(self.layer1(input_data))))