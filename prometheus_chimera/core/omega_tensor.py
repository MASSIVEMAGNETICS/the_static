import numpy as np

class OmegaTensor:
    """The core data structure of the PROMETHEUS-CHIMERA system."""
    def __init__(self, data, requires_grad=False, _children=(), _op=''):
        self.data = np.array(data, dtype=np.float32)
        self.requires_grad = requires_grad
        self._prev = set(_children)
        self._op = _op
        self.grad = np.zeros_like(self.data, dtype=np.float32)
        self._backward = lambda: None

    def __repr__(self):
        return f"OmegaTensor(data={self.data}, requires_grad={self.requires_grad})"

    def __add__(self, other):
        other = other if isinstance(other, OmegaTensor) else OmegaTensor(other)
        out = OmegaTensor(self.data + other.data, _children=(self, other), _op='+')

        def _backward():
            self.grad += out.grad
            other.grad += out.grad
        out._backward = _backward
        return out

    def __mul__(self, other):
        other = other if isinstance(other, OmegaTensor) else OmegaTensor(other)
        out = OmegaTensor(self.data * other.data, _children=(self, other), _op='*')

        def _backward():
            self.grad += other.data * out.grad
            other.grad += self.data * out.grad
        out._backward = _backward
        return out

    def backward(self):
        topo = []
        visited = set()
        def build_topo(v):
            if v not in visited:
                visited.add(v)
                for child in v._prev:
                    build_topo(child)
                topo.append(v)
        build_topo(self)

        self.grad = np.ones_like(self.data)
        for v in reversed(topo):
            v._backward()
