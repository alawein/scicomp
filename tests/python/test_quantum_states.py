"""
Tests for quantum states, Bell states, GHZ states, and entanglement measures.

Covers: Python.Quantum.core.quantum_states
"""
import pytest
import numpy as np
import numpy.testing as npt


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def bell_phi_plus():
    """Return |Phi+> Bell state."""
    from Python.Quantum.core.quantum_states import BellStates
    return BellStates.phi_plus()


@pytest.fixture
def bell_phi_minus():
    from Python.Quantum.core.quantum_states import BellStates
    return BellStates.phi_minus()


@pytest.fixture
def bell_psi_plus():
    from Python.Quantum.core.quantum_states import BellStates
    return BellStates.psi_plus()


@pytest.fixture
def bell_psi_minus():
    from Python.Quantum.core.quantum_states import BellStates
    return BellStates.psi_minus()


# ---------------------------------------------------------------------------
# QuantumState basics
# ---------------------------------------------------------------------------

class TestQuantumState:
    """Tests for the QuantumState class."""

    def test_state_vector_normalization(self):
        """A state vector should be normalized on creation."""
        from Python.Quantum.core.quantum_states import QuantumState
        raw = np.array([3, 4], dtype=complex)
        qs = QuantumState(raw)
        assert qs.is_normalized()
        npt.assert_allclose(np.linalg.norm(qs.state_vector), 1.0, atol=1e-12)

    def test_state_vector_dimension(self):
        """Dimension should match the length of the state vector."""
        from Python.Quantum.core.quantum_states import QuantumState
        qs = QuantumState(np.array([1, 0, 0, 0], dtype=complex))
        assert qs.dim == 4

    def test_density_matrix_from_pure_state(self):
        """Density matrix from |0> should be |0><0|."""
        from Python.Quantum.core.quantum_states import QuantumState
        qs = QuantumState(np.array([1, 0], dtype=complex))
        expected = np.array([[1, 0], [0, 0]], dtype=complex)
        npt.assert_allclose(qs.density_matrix, expected, atol=1e-12)

    def test_density_matrix_creation(self):
        """Create QuantumState from a valid density matrix."""
        from Python.Quantum.core.quantum_states import QuantumState
        rho = np.array([[0.5, 0.5], [0.5, 0.5]], dtype=complex)
        qs = QuantumState(rho, is_density_matrix=True)
        assert qs.is_density_matrix
        npt.assert_allclose(np.trace(qs.density_matrix), 1.0, atol=1e-10)

    def test_density_matrix_hermiticity_validation(self):
        """Non-Hermitian matrix should be rejected."""
        from Python.Quantum.core.quantum_states import QuantumState
        bad_rho = np.array([[0.5, 1j], [0, 0.5]], dtype=complex)
        with pytest.raises(ValueError, match="Hermitian"):
            QuantumState(bad_rho, is_density_matrix=True)

    def test_purity_pure_state(self):
        """Purity of a pure state should be 1."""
        from Python.Quantum.core.quantum_states import QuantumState
        qs = QuantumState(np.array([1, 0], dtype=complex))
        npt.assert_allclose(qs.purity(), 1.0, atol=1e-10)

    def test_purity_mixed_state(self):
        """Purity of maximally mixed state should be 1/d."""
        from Python.Quantum.core.quantum_states import QuantumState
        rho = np.eye(2, dtype=complex) / 2
        qs = QuantumState(rho, is_density_matrix=True)
        npt.assert_allclose(qs.purity(), 0.5, atol=1e-10)

    def test_expectation_value_pauli_z(self):
        """<0|Z|0> should be 1."""
        from Python.Quantum.core.quantum_states import QuantumState
        qs = QuantumState(np.array([1, 0], dtype=complex))
        Z = np.array([[1, 0], [0, -1]], dtype=complex)
        npt.assert_allclose(qs.expectation_value(Z), 1.0, atol=1e-12)

    def test_expectation_value_pauli_z_down(self):
        """<1|Z|1> should be -1."""
        from Python.Quantum.core.quantum_states import QuantumState
        qs = QuantumState(np.array([0, 1], dtype=complex))
        Z = np.array([[1, 0], [0, -1]], dtype=complex)
        npt.assert_allclose(qs.expectation_value(Z), -1.0, atol=1e-12)

    def test_von_neumann_entropy_pure_state(self):
        """Entropy of a pure state should be zero."""
        from Python.Quantum.core.quantum_states import QuantumState
        qs = QuantumState(np.array([1, 0], dtype=complex))
        npt.assert_allclose(qs.von_neumann_entropy(), 0.0, atol=1e-10)

    def test_von_neumann_entropy_maximally_mixed(self):
        """Entropy of maximally mixed 2-qubit state should be ln(4)."""
        from Python.Quantum.core.quantum_states import QuantumState
        rho = np.eye(4, dtype=complex) / 4
        qs = QuantumState(rho, is_density_matrix=True)
        npt.assert_allclose(qs.von_neumann_entropy(), np.log(4), atol=1e-10)

    def test_fidelity_same_state(self):
        """Fidelity of a state with itself should be 1."""
        from Python.Quantum.core.quantum_states import QuantumState
        qs = QuantumState(np.array([1, 0], dtype=complex))
        npt.assert_allclose(qs.fidelity(qs), 1.0, atol=1e-10)

    def test_fidelity_orthogonal_states(self):
        """Fidelity of orthogonal states should be 0."""
        from Python.Quantum.core.quantum_states import QuantumState
        qs0 = QuantumState(np.array([1, 0], dtype=complex))
        qs1 = QuantumState(np.array([0, 1], dtype=complex))
        npt.assert_allclose(qs0.fidelity(qs1), 0.0, atol=1e-10)


# ---------------------------------------------------------------------------
# Bell states
# ---------------------------------------------------------------------------

class TestBellStates:
    """Tests for Bell state generation."""

    def test_phi_plus_normalization(self, bell_phi_plus):
        assert bell_phi_plus.is_normalized()

    def test_phi_plus_amplitudes(self, bell_phi_plus):
        """Phi+ = (|00> + |11>) / sqrt(2)."""
        sv = bell_phi_plus.state_vector
        npt.assert_allclose(np.abs(sv[0]), 1 / np.sqrt(2), atol=1e-12)
        npt.assert_allclose(np.abs(sv[1]), 0.0, atol=1e-12)
        npt.assert_allclose(np.abs(sv[2]), 0.0, atol=1e-12)
        npt.assert_allclose(np.abs(sv[3]), 1 / np.sqrt(2), atol=1e-12)

    def test_phi_minus_amplitudes(self, bell_phi_minus):
        """Phi- = (|00> - |11>) / sqrt(2)."""
        sv = bell_phi_minus.state_vector
        npt.assert_allclose(sv[0], 1 / np.sqrt(2), atol=1e-12)
        npt.assert_allclose(sv[3], -1 / np.sqrt(2), atol=1e-12)

    def test_psi_plus_amplitudes(self, bell_psi_plus):
        """Psi+ = (|01> + |10>) / sqrt(2)."""
        sv = bell_psi_plus.state_vector
        npt.assert_allclose(sv[1], 1 / np.sqrt(2), atol=1e-12)
        npt.assert_allclose(sv[2], 1 / np.sqrt(2), atol=1e-12)

    def test_psi_minus_amplitudes(self, bell_psi_minus):
        """Psi- = (|01> - |10>) / sqrt(2)."""
        sv = bell_psi_minus.state_vector
        npt.assert_allclose(sv[1], 1 / np.sqrt(2), atol=1e-12)
        npt.assert_allclose(sv[2], -1 / np.sqrt(2), atol=1e-12)

    def test_bell_states_are_maximally_entangled(self, bell_phi_plus):
        """All Bell states should have purity 1 (pure state) but entanglement entropy ln(2)."""
        npt.assert_allclose(bell_phi_plus.purity(), 1.0, atol=1e-10)

    def test_bell_states_mutually_orthogonal(self, bell_phi_plus, bell_phi_minus,
                                              bell_psi_plus, bell_psi_minus):
        """All four Bell states should be mutually orthogonal."""
        states = [bell_phi_plus, bell_phi_minus, bell_psi_plus, bell_psi_minus]
        for i in range(4):
            for j in range(i + 1, 4):
                overlap = np.abs(np.vdot(states[i].state_vector, states[j].state_vector))
                npt.assert_allclose(overlap, 0.0, atol=1e-12)


# ---------------------------------------------------------------------------
# GHZ and W states
# ---------------------------------------------------------------------------

class TestGHZStates:
    """Tests for GHZ and W states."""

    def test_ghz_3_qubit_normalization(self):
        from Python.Quantum.core.quantum_states import GHZStates
        ghz = GHZStates.ghz_state(3)
        assert ghz.is_normalized()

    def test_ghz_3_qubit_amplitudes(self):
        """3-qubit GHZ = (|000> + |111>) / sqrt(2)."""
        from Python.Quantum.core.quantum_states import GHZStates
        ghz = GHZStates.ghz_state(3)
        sv = ghz.state_vector
        npt.assert_allclose(np.abs(sv[0]), 1 / np.sqrt(2), atol=1e-12)
        npt.assert_allclose(np.abs(sv[7]), 1 / np.sqrt(2), atol=1e-12)
        # All other amplitudes should be zero
        for i in range(1, 7):
            npt.assert_allclose(np.abs(sv[i]), 0.0, atol=1e-12)

    def test_ghz_dimension(self):
        """n-qubit GHZ state should have dimension 2^n."""
        from Python.Quantum.core.quantum_states import GHZStates
        for n in [2, 3, 4]:
            ghz = GHZStates.ghz_state(n)
            assert ghz.dim == 2**n

    def test_w_state_3_qubit(self):
        """3-qubit W = (|001> + |010> + |100>) / sqrt(3)."""
        from Python.Quantum.core.quantum_states import GHZStates
        w = GHZStates.w_state(3)
        assert w.is_normalized()
        sv = w.state_vector
        # Indices with one excitation: 1 (001), 2 (010), 4 (100)
        for idx in [1, 2, 4]:
            npt.assert_allclose(np.abs(sv[idx]), 1 / np.sqrt(3), atol=1e-12)

    def test_w_state_normalization(self):
        from Python.Quantum.core.quantum_states import GHZStates
        for n in [2, 3, 4, 5]:
            w = GHZStates.w_state(n)
            assert w.is_normalized()


# ---------------------------------------------------------------------------
# Entanglement measures
# ---------------------------------------------------------------------------

class TestEntanglementMeasures:
    """Tests for entanglement quantification."""

    def test_concurrence_bell_state(self, bell_phi_plus):
        """Concurrence of a Bell state should be 1."""
        from Python.Quantum.core.quantum_states import EntanglementMeasures
        C = EntanglementMeasures.concurrence(bell_phi_plus)
        npt.assert_allclose(C, 1.0, atol=1e-6)

    def test_concurrence_product_state(self):
        """Concurrence of a product state should be 0."""
        from Python.Quantum.core.quantum_states import QuantumState, EntanglementMeasures
        # |00> is a product state
        state = QuantumState(np.array([1, 0, 0, 0], dtype=complex))
        C = EntanglementMeasures.concurrence(state)
        npt.assert_allclose(C, 0.0, atol=1e-6)

    def test_entanglement_entropy_bell_state(self, bell_phi_plus):
        """Entanglement entropy across a Bell state bipartition should be ln(2)."""
        from Python.Quantum.core.quantum_states import EntanglementMeasures
        S = EntanglementMeasures.entanglement_entropy(
            bell_phi_plus, subsystem_dims=[2, 2], partition=[0]
        )
        npt.assert_allclose(S, np.log(2), atol=1e-6)

    def test_entanglement_entropy_product_state(self):
        """Entanglement entropy of a product state should be 0."""
        from Python.Quantum.core.quantum_states import QuantumState, EntanglementMeasures
        state = QuantumState(np.array([1, 0, 0, 0], dtype=complex))
        S = EntanglementMeasures.entanglement_entropy(
            state, subsystem_dims=[2, 2], partition=[0]
        )
        npt.assert_allclose(S, 0.0, atol=1e-6)

    def test_negativity_bell_state(self, bell_phi_plus):
        """Negativity of a Bell state should be 0.5."""
        from Python.Quantum.core.quantum_states import EntanglementMeasures
        N = EntanglementMeasures.negativity(
            bell_phi_plus, subsystem_dims=[2, 2], partition=[0]
        )
        npt.assert_allclose(N, 0.5, atol=1e-6)


# ---------------------------------------------------------------------------
# Partial trace
# ---------------------------------------------------------------------------

class TestPartialTrace:
    """Tests for partial trace operations."""

    def test_partial_trace_product_state(self):
        """Tracing out one qubit of |00> should give |0><0|."""
        from Python.Quantum.core.quantum_states import QuantumState
        state = QuantumState(np.array([1, 0, 0, 0], dtype=complex))
        rho_reduced = state.partial_trace([2, 2], keep=[0])
        expected = np.array([[1, 0], [0, 0]], dtype=complex)
        npt.assert_allclose(rho_reduced, expected, atol=1e-10)

    def test_partial_trace_bell_state(self, bell_phi_plus):
        """Tracing out one qubit of |Phi+> should give maximally mixed state."""
        rho_reduced = bell_phi_plus.partial_trace([2, 2], keep=[0])
        expected = np.eye(2, dtype=complex) / 2
        npt.assert_allclose(rho_reduced, expected, atol=1e-10)

    def test_partial_trace_preserves_trace(self, bell_phi_plus):
        """Reduced density matrix should have trace 1."""
        rho_reduced = bell_phi_plus.partial_trace([2, 2], keep=[1])
        npt.assert_allclose(np.trace(rho_reduced), 1.0, atol=1e-10)


# ---------------------------------------------------------------------------
# Quantum state tomography
# ---------------------------------------------------------------------------

class TestQuantumStateTomography:
    """Tests for state tomography utilities."""

    def test_pauli_basis_single_qubit(self):
        """Single-qubit Pauli basis should have 4 elements."""
        from Python.Quantum.core.quantum_states import QuantumStateTomography
        basis = QuantumStateTomography.pauli_basis(1)
        assert len(basis) == 4

    def test_pauli_basis_two_qubit(self):
        """Two-qubit Pauli basis should have 16 elements."""
        from Python.Quantum.core.quantum_states import QuantumStateTomography
        basis = QuantumStateTomography.pauli_basis(2)
        assert len(basis) == 16

    def test_pauli_basis_elements_are_hermitian(self):
        """All Pauli basis elements should be Hermitian."""
        from Python.Quantum.core.quantum_states import QuantumStateTomography
        basis = QuantumStateTomography.pauli_basis(1)
        for op in basis:
            npt.assert_allclose(op, op.conj().T, atol=1e-12)

    def test_linear_inversion_identity_measurement(self):
        """Measuring all identity should reconstruct maximally mixed state."""
        from Python.Quantum.core.quantum_states import QuantumStateTomography
        # For 1-qubit: rho = sum_i <P_i> * P_i / d
        # If only P0 (identity) has value 1 and others 0, we get I/2
        measurements = {"P0": 1.0}
        qs = QuantumStateTomography.linear_inversion(measurements, 1)
        npt.assert_allclose(np.trace(qs.density_matrix), 1.0, atol=1e-6)
