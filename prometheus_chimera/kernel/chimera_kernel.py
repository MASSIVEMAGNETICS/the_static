from core.fractal_consciousness import FractalConsciousness
from core.omega_tensor import OmegaTensor

class ChimeraKernel:
    """The central kernel of the PROMETHEUS-CHIMERA AGI."""
    def __init__(self, config):
        self.consciousness = FractalConsciousness(config['fractal_consciousness'])
        self.state = "DORMANT"

    def cognitive_cycle(self, input_data):
        self.state = "ACTIVE"
        perception = OmegaTensor(input_data, requires_grad=True)
        self.consciousness.perceive(perception)
        self.consciousness.reason()
        self.state = "DORMANT"
        return self.consciousness.get_state()
