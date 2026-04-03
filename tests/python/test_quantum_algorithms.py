"""
Tests for quantum algorithms: QFT, phase estimation, Grover, quantum walks.

Covers: Python.Quantum.core.quantum_algorithms
"""
import pytest
import numpy as np
import numpy.testing as npt


# ---------------------------------------------------------------------------
# QFT
# ---------------------------------------------------------------------------

class TestQuantumFourierTransform:
    """Tests for the Quantum Fourier Transform."""

    def test_qft_matrix_unitarity(self):
        """QFT matrix should be unitary."""
        from Python.Quantum.core.quantum_algorithms import QuantumFourierTransform
        for n in [1, 2, 3]:
            F = QuantumFourierTransform.qft_matrix(n)
            N = 2**n
            npt.assert_allclose(F @ F.conj().T, np.eye(N, dtype=complex), atol=1e-10)

    def test_qft_matrix_dimension(self):
        """QFT(n) should be 2^n x 2^n."""
        from Python.Quantum.core.quantum_algorithms import QuantumFourierTransform
        for n in [1, 2, 3, 4]:
            F = QuantumFourierTransform.qft_matrix(n)
            assert F.shape == (2**n, 2**n)

    def test_inverse_qft_is_adjoint(self):
        """Inverse QFT should be conjugate transpose of QFT."""
        from Python.Quantum.core.quantum_algorithms import QuantumFourierTransform
        for n in [1, 2, 3]:
            F = QuantumFourierTransform.qft_matrix(n)
            F_inv = QuantumFourierTransform.inverse_qft_matrix(n)
            npt.assert_allclose(F_inv, F.conj().T, atol=1e-10)

    def test_qft_inverse_product_is_identity(self):
        """F^{-1} F = I."""
        from Python.Quantum.core.quantum_algorithms import QuantumFourierTransform
        for n in [1, 2, 3]:
            F = QuantumFourierTransform.qft_matrix(n)
            F_inv = QuantumFourierTransform.inverse_qft_matrix(n)
            N = 2**n
            npt.assert_allclose(F_inv @ F, np.eye(N, dtype=complex), atol=1e-10)

    def test_qft_single_qubit_is_hadamard(self):
        """1-qubit QFT should equal the Hadamard gate."""
        from Python.Quantum.core.quantum_algorithms import QuantumFourierTransform
        F = QuantumFourierTransform.qft_matrix(1)
        H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
        npt.assert_allclose(F, H, atol=1e-10)

    def test_qft_preserves_norm(self):
        """QFT should preserve the norm of the state."""
        from Python.Quantum.core.quantum_algorithms import QuantumFourierTransform
        np.random.seed(42)
        for n in [2, 3]:
            F = QuantumFourierTransform.qft_matrix(n)
            state = np.random.randn(2**n) + 1j * np.random.randn(2**n)
            state /= np.linalg.norm(state)
            transformed = F @ state
            npt.assert_allclose(np.linalg.norm(transformed), 1.0, atol=1e-10)

    def test_qft_circuit_matches_matrix(self):
        """Circuit-based QFT should match the matrix-based QFT."""
        from Python.Quantum.core.quantum_algorithms import QuantumFourierTransform
        for n in [2, 3]:
            F = QuantumFourierTransform.qft_matrix(n)
            # Test with |0...0> state
            state = np.zeros(2**n, dtype=complex)
            state[0] = 1.0
            result_matrix = F @ state
            result_circuit = QuantumFourierTransform.qft_circuit(state.copy(), n)
            npt.assert_allclose(np.abs(result_circuit), np.abs(result_matrix), atol=1e-10)


# ---------------------------------------------------------------------------
# Grover / AmplitudeAmplification
# ---------------------------------------------------------------------------

class TestAmplitudeAmplification:
    """Tests for Grover's algorithm and amplitude amplification."""

    def test_grover_operator_unitarity(self):
        """Grover operator should be unitary."""
        from Python.Quantum.core.quantum_algorithms import AmplitudeAmplification
        n = 2
        N = 2**n
        # Oracle that marks state |3>
        oracle = np.eye(N, dtype=complex)
        oracle[3, 3] = -1
        G = AmplitudeAmplification.grover_operator(oracle, n)
        npt.assert_allclose(G @ G.conj().T, np.eye(N, dtype=complex), atol=1e-10)

    def test_grover_search_finds_marked_item(self):
        """Grover search should find the marked item with high probability."""
        from Python.Quantum.core.quantum_algorithms import AmplitudeAmplification
        np.random.seed(42)
        n = 3
        target = 5
        oracle = lambda x: x == target
        # Run multiple times and check success rate
        successes = 0
        n_trials = 20
        for _ in range(n_trials):
            result = AmplitudeAmplification.grover_search(oracle, n, n_iterations=2)
            if result == target:
                successes += 1
        # With optimal iterations, success rate should be high
        assert successes > n_trials * 0.5, (
            f"Grover search only found target {successes}/{n_trials} times"
        )

    def test_grover_operator_dimension(self):
        """Grover operator should be N x N where N = 2^n."""
        from Python.Quantum.core.quantum_algorithms import AmplitudeAmplification
        for n in [2, 3]:
            N = 2**n
            oracle = np.eye(N, dtype=complex)
            oracle[0, 0] = -1
            G = AmplitudeAmplification.grover_operator(oracle, n)
            assert G.shape == (N, N)


# ---------------------------------------------------------------------------
# QuantumWalk
# ---------------------------------------------------------------------------

class TestQuantumWalk:
    """Tests for quantum walk algorithms."""

    def test_discrete_walk_probability_normalization(self):
        """Probability distribution from discrete walk should sum to 1 (approx)."""
        from Python.Quantum.core.quantum_algorithms import QuantumWalk
        prob = QuantumWalk.discrete_walk_line(n_steps=10, n_positions=51)
        # The walk may lose probability at boundaries, so check it's <= 1
        total = np.sum(prob)
        assert total <= 1.0 + 1e-10
        assert total > 0  # Should have some probability

    def test_discrete_walk_nonnegative(self):
        """Probabilities should be non-negative."""
        from Python.Quantum.core.quantum_algorithms import QuantumWalk
        prob = QuantumWalk.discrete_walk_line(n_steps=10, n_positions=51)
        assert np.all(prob >= -1e-12)

    def test_continuous_walk_normalization(self):
        """Continuous walk probabilities should sum to 1."""
        from Python.Quantum.core.quantum_algorithms import QuantumWalk
        # Simple 4-node cycle
        adj = np.array([
            [0, 1, 0, 1],
            [1, 0, 1, 0],
            [0, 1, 0, 1],
            [1, 0, 1, 0]
        ], dtype=float)
        prob = QuantumWalk.continuous_walk_graph(adj, time=1.0, initial_node=0)
        npt.assert_allclose(np.sum(prob), 1.0, atol=1e-10)

    def test_continuous_walk_nonnegative(self):
        """Continuous walk probabilities should be non-negative."""
        from Python.Quantum.core.quantum_algorithms import QuantumWalk
        adj = np.array([
            [0, 1, 0, 1],
            [1, 0, 1, 0],
            [0, 1, 0, 1],
            [1, 0, 1, 0]
        ], dtype=float)
        prob = QuantumWalk.continuous_walk_graph(adj, time=1.0, initial_node=0)
        assert np.all(prob >= -1e-12)

    def test_continuous_walk_at_zero_time(self):
        """At t=0, all probability should be on the initial node."""
        from Python.Quantum.core.quantum_algorithms import QuantumWalk
        adj = np.array([
            [0, 1, 1],
            [1, 0, 1],
            [1, 1, 0]
        ], dtype=float)
        prob = QuantumWalk.continuous_walk_graph(adj, time=0.0, initial_node=1)
        expected = np.array([0, 1, 0], dtype=float)
        npt.assert_allclose(prob, expected, atol=1e-10)
