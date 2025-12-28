import numpy as np

class OmegaTensor:
    def __init__(self, data, requires_grad=False):
        self.data = np.array(data)
        self.requires_grad = requires_grad
        self.grad = None

    @property
    def shape(self):
        return self.data.shape

    def __repr__(self):
        return f"OmegaTensor(shape={self.shape}, requires_grad={self.requires_grad})"
