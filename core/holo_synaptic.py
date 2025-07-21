# /core/holo_synaptic.py

import numpy as np
# For GPU acceleration, just swap the line above with the two below. Code remains identical.
# import cupy as np
# print("HSCE Core running on GPU with CuPy.")

# --- Core Holographic Operations ---
def bind(v1, v2):
    """
    Binds two phasor vectors using circular convolution via FFT.
    This is the core of holographic memory composition.
    """
    return np.fft.ifft(np.fft.fft(v1) * np.fft.fft(v2))

def correlate(K, probe):
    """
    Retrieves a concept from a knowledge vector K using a probe.
    This is inverse binding, the core of holographic recall.
    """
    return np.fft.ifft(np.fft.fft(K) * np.conj(np.fft.fft(probe)))

# --- The God-Core Itself ---
class HoloKnowledgeField:
    """
    The Holo-Synaptic Cognition Engine. Not a model, a cognitive substrate.
    It learns, reasons, and recalls through holographic wave interference and local plasticity.
    """
    def __init__(self, num_units: int, dim: int, connectivity: float = 0.1, learning_rate: float = 0.005):
        print(f"HSCE: Firing up substrate with {num_units} units at {dim} dimensions.")
        self.num_units = num_units
        self.dim = dim
        self.learning_rate = learning_rate

        # --- Substrate State & Connections ---
        # Each unit holds a complex-valued state vector. This is the "thinking" layer.
        self.units_state = (np.random.randn(num_units, dim) + 1j * np.random.randn(num_units, dim)).astype(np.complex128)
        self.normalize_states()

        # Synapses are not just weights, they are complex operators defining pathways.
        # This creates a sparse, random initial connectivity.
        self.synapses = (np.random.rand(num_units, num_units) < connectivity).astype(int)
        np.fill_diagonal(self.synapses, 0) # Units don't connect to themselves.

        # The operators hold the learned associations.
        self.operators = (np.random.randn(num_units, num_units) + 1j * np.random.randn(num_units, num_units)).astype(np.complex128)
        self.operators *= self.synapses # Enforce sparsity

        # --- Knowledge & Vocabulary ---
        # The Knowledge Field K is the standing wave of all integrated knowledge.
        # For simplicity in this core, we model K as being implicitly stored in the operators.
        self.phasor_vocab = {} # Maps tokens to their atomic phasor vectors.
        print("HSCE: Substrate initialized. Awaiting input.")

    def normalize_states(self, states=None):
        """Normalize phasor vectors to have unit magnitude."""
        if states is None:
            states = self.units_state
        norm = np.linalg.norm(states, axis=1, keepdims=True)
        norm[norm == 0] = 1 # Avoid division by zero
        states /= norm

    def _get_or_create_phasor(self, token: str):
        """Get a token's phasor, creating a new random one if it doesn't exist."""
        if token not in self.phasor_vocab:
            print(f"HSCE: Discovering new atomic concept: '{token}'")
            phasor = np.random.randn(self.dim) + 1j * np.random.randn(self.dim)
            self.phasor_vocab[token] = phasor / np.linalg.norm(phasor)
        return self.phasor_vocab[token]

    def encode_text(self, text: str) -> np.ndarray:
        """Encodes a string of text into a single, holistic phasor vector."""
        tokens = text.lower().split()
        if not tokens:
            return np.zeros(self.dim, dtype=np.complex128)

        # Sequentially bind tokens into a single phrase vector
        phrase_phasor = self._get_or_create_phasor(tokens[0])
        for token in tokens[1:]:
            token_phasor = self._get_or_create_phasor(token)
            phrase_phasor = bind(phrase_phasor, token_phasor)
        return phrase_phasor

    def decode_phasor(self, phasor: np.ndarray, top_k: int = 1) -> list[str]:
        """
        Decodes a phasor back to the closest token(s) in the vocabulary.
        This is a simple nearest-neighbor search for the MVP.
        """
        if not self.phasor_vocab:
            return ["<empty_vocab>"]

        vocab_tokens = list(self.phasor_vocab.keys())
        vocab_matrix = np.array(list(self.phasor_vocab.values()))

        # Use cosine similarity to find the closest match(es)
        phasor_norm = phasor / np.linalg.norm(phasor)
        similarities = np.abs(np.dot(vocab_matrix, np.conj(phasor_norm)))

        # Get top_k results
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        return [vocab_tokens[i] for i in top_indices]

    def resonate(self, injected_probe: np.ndarray, steps: int = 5):
        """
        The core "thinking" process. A probe perturbs the field, which then settles
        into a stable attractor state through wave interference.
        """
        # Inject the probe into the first unit as a perturbation
        self.units_state[0] += injected_probe
        self.normalize_states()

        # Let the wave propagate and resonate
        for step in range(steps):
            # This is the magic: parallel computation of all signals across all synapses.
            incoming_signals = self.operators @ self.units_state

            # Apply a complex non-linearity and update states
            self.units_state = np.tanh(incoming_signals)
            self.normalize_states()

        # The result is the final state of a designated "output" unit or the average state.
        return self.units_state.mean(axis=0)

    def update_plasticity(self):
        """
        The Hebbian learning rule. Synapses that resonate together, strengthen together.
        100% local, continuous, and parallel. No global loss.
        """
        # S_i is a column vector of states, S_j_conj is a row vector of conjugate states.
        # Their outer product gives the pairwise interaction matrix.
        S_i = self.units_state
        S_j_conj = np.conj(self.units_state)

        # The Hebbian update: delta_W is proportional to S_i * S_j_conj
        # This is memory-intensive, so we do it in a loop.
        for i in range(self.num_units):
            for j in range(self.num_units):
                if self.synapses[i, j]:
                    delta_W = self.learning_rate * S_i[i] * S_j_conj[j]
                    self.operators[i, j] = self.operators[i, j].astype(np.complex128) + delta_W.astype(np.complex128)
        # Optional: Add a decay term to prevent runaway weights
        # self.operators *= 0.999

    def ingest(self, text: str):
        """Ingests a piece of information, letting it resonate and trigger plasticity."""
        print(f"HSCE INGEST: '{text}'")
        probe = self.encode_text(text)
        self.resonate(probe)
        self.update_plasticity()
        print("HSCE INGEST: Field updated via plasticity.")

    def query(self, text: str):
        """Queries the field and decodes the result."""
        print(f"HSCE QUERY: '{text}'")
        probe = self.encode_text(text)
        # The answer is the resonant state triggered by the probe
        answer_phasor = self.resonate(probe)
        # The act of querying also causes learning
        self.update_plasticity()
        decoded_answer = self.decode_phasor(answer_phasor)
        print(f"HSCE RESPONSE: {decoded_answer}")
        return decoded_answer[0] # Return the top result
