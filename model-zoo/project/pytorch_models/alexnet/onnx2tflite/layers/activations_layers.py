import tensorflow as tf
from tensorflow import keras

from .shape_axis_utils import Torch2TFAxis
from . import OPERATOR

@OPERATOR.register_operator("Relu")
class TFRelu():
    def __init__(self, *args, **kwargs) -> None:
        super().__init__()

    def __call__(self, inputs):
        return keras.activations.relu(inputs)

@OPERATOR.register_operator("HardSigmoid")
class TFHardSigmoid():
    def __init__(self, tensor_grap, node_weights, node_inputs, node_attribute, *args, **kwargs) -> None:
        super().__init__()
        self.alpha = node_attribute.get("alpha", 0.2)
        self.beta = node_attribute.get("beta", 0.5)

    def __call__(self, inputs):
        return tf.clip_by_value(self.alpha*inputs+self.beta, 0, 1)

@OPERATOR.register_operator("Sigmoid")
class TFSigmoid():
    def __init__(self, *args, **kwargs) -> None:
        super().__init__()

    def __call__(self, inputs):
        return keras.activations.sigmoid(inputs)

@OPERATOR.register_operator("LeakyRelu")
class TFLeakyRelu():
    def __init__(self, tensor_grap, node_weights, node_inputs, node_attribute, *args, **kwargs) -> None:
        super().__init__()
        self.alpha = node_attribute.get('alpha', 0.01)

    def __call__(self, inputs):
        return keras.activations.relu(inputs, alpha=self.alpha)

@OPERATOR.register_operator("PRelu")
class TFPRelu():
    def __init__(self, tensor_grap, node_weights, node_inputs, node_attribute, *args, **kwargs) -> None:
        super().__init__()
        if 'slope' in node_attribute:
            self.slope = node_attribute['slope'].transpose(1, 2, 0)
        elif node_inputs[1] in node_weights:
            self.slope = node_weights[node_inputs[1]].transpose(1, 2, 0)
        else:
            self.slope = tensor_grap[node_inputs[1]]
        self.PRelu = tf.keras.layers.PReLU(weights=[self.slope], shared_axes = [1, 2])

    def __call__(self, inputs):
        return self.PRelu(inputs)

@OPERATOR.register_operator("Sin")
class TFSin():
    def __init__(self, *args, **kwargs) -> None:
        super().__init__()

    def __call__(self, inputs):
        return tf.sin(inputs)

@OPERATOR.register_operator("Cos")
class TFCos():
    def __init__(self, *args, **kwargs) -> None:
        super().__init__()

    def __call__(self, inputs):
        return tf.cos(inputs)

@OPERATOR.register_operator("Tanh")
class TFTanh():
    def __init__(self, *args, **kwargs) -> None:
        super().__init__()

    def __call__(self, inputs):
        return keras.activations.tanh(inputs)

@OPERATOR.register_operator("Softmax")
class TFSoftmax():
    def __init__(self, tensor_grap, node_weights, node_inputs, node_attribute, *args, **kwargs) -> None:
        super().__init__()
        self.axis = Torch2TFAxis(node_attribute.get('axis', -1))

    def __call__(self, inputs):
        return keras.activations.softmax(inputs, axis=self.axis)

@OPERATOR.register_operator("Softplus")
class TFSoftplus():
    def __init__(self, tensor_grap, node_weights, node_inputs, node_attribute, *args, **kwargs) -> None:
        super().__init__()

    def __call__(self, inputs):
        return tf.math.log(tf.exp(inputs) + 1)

@OPERATOR.register_operator("Selu")
class TFSelu():
    def __init__(self, tensor_grap, node_weights, node_inputs, node_attribute, *args, **kwargs) -> None:
        super().__init__()

    def __call__(self, inputs):
        return keras.activations.selu(inputs)