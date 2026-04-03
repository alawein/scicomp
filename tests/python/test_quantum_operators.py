"""
Tests for quantum operators, gates, Hamiltonians, and time evolution.

Covers: Python.Quantum.core.quantum_operators
"""
import pytest
import numpy as np
import numpy.testing as npt


# ---------------------------------------------------------------------------
# PauliOperators
# ---------------------------------------------------------------------------

class TestPauliOperators:
    """Tests for Pauli matrix algebra."""

    def test_pauli_hermiticity(self):
        """All Pauli matrices should be Hermitian."""
        from Python.Quantum.core.quantum_operators import PauliOperators
        for name, mat in [("X", PauliOperators.X), ("Y", PauliOperators.Y),
                          ("Z", PauliOperators.Z)]:
            npt.assert_allclose(mat, mat.conj().T, atol=1e-12,
                                err_msg=f"Pauli {name} not Hermitian")

    def test_pauli_unitarity(self):
        """Pauli matrices should be unitary (P * P^dag = I)."""
        from Python.Quantum.core.quantum_operators import PauliOperators
        I2 = np.eye(2, dtype=complex)
        for mat in [PauliOperators.X, PauliOperators.Y, PauliOperators.Z]:
            npt.assert_allclose(mat @ mat.conj().T, I2, atol=1e-12)

    def test_pauli_involutory(self):
        """Pauli matrices should square to the identity."""
        from Python.Quantum.core.quantum_operators import PauliOperators
        I2 = np.eye(2, dtype=complex)
        for mat in [PauliOperators.X, PauliOperators.Y, PauliOperators.Z]:
            npt.assert_allclose(mat @ mat, I2, atol=1e-12)

    def test_pauli_commutation_relations(self):
        """[X, Y] = 2iZ and cyclic permutations."""
        from Python.Quantum.core.quantum_operators import PauliOperators
        X, Y, Z = PauliOperators.X, PauliOperators.Y, PauliOperators.Z
        # [X, Y] = 2i Z
        npt.assert_allclose(PauliOperators.commutator(X, Y), 2j * Z, atol=1e-12)
        # [Y, Z] = 2i X
        npt.assert_allclose(PauliOperators.commutator(Y, Z), 2j * X, atol=1e-12)
        # [Z, X] = 2i Y
        npt.assert_allclose(PauliOperators.commutator(Z, X), 2j * Y, atol=1e-12)

    def test_pauli_anticommutation(self):
        """{X, Y} = 0 for distinct Pauli matrices."""
        from Python.Quantum.core.quantum_operators import PauliOperators
        X, Y, Z = PauliOperators.X, PauliOperators.Y, PauliOperators.Z
        zero = np.zeros((2, 2), dtype=complex)
        npt.assert_allclose(PauliOperators.anticommutator(X, Y), zero, atol=1e-12)
        npt.assert_allclose(PauliOperators.anticommutator(Y, Z), zero, atol=1e-12)
        npt.assert_allclose(PauliOperators.anticommutator(Z, X), zero, atol=1e-12)

    def test_pauli_string_single(self):
        """pauli_string('X') should return the X matrix."""
        from Python.Quantum.core.quantum_operators import PauliOperators
        npt.assert_allclose(PauliOperators.pauli_string('X'), PauliOperators.X, atol=1e-12)

    def test_pauli_string_tensor_product(self):
        """pauli_string('XY') should return kron(X, Y)."""
        from Python.Quantum.core.quantum_operators import PauliOperators
        expected = np.kron(PauliOperators.X, PauliOperators.Y)
        npt.assert_allclose(PauliOperators.pauli_string('XY'), expected, atol=1e-12)

    def test_pauli_string_identity(self):
        """pauli_string('II') should return 4x4 identity."""
        from Python.Quantum.core.quantum_operators import PauliOperators
        npt.assert_allclose(PauliOperators.pauli_string('II'),
                            np.eye(4, dtype=complex), atol=1e-12)


# ---------------------------------------------------------------------------
# QuantumGates
# ---------------------------------------------------------------------------

class TestQuantumGates:
    """Tests for standard quantum gates."""

    def test_hadamard_unitarity(self):
        """H * H^dag = I."""
        from Python.Quantum.core.quantum_operators import QuantumGates
        H = QuantumGates.H
        npt.assert_allclose(H @ H.conj().T, np.eye(2, dtype=complex), atol=1e-12)

    def test_hadamard_involutory(self):
        """H^2 = I."""
        from Python.Quantum.core.quantum_operators import QuantumGates
        H = QuantumGates.H
        npt.assert_allclose(H @ H, np.eye(2, dtype=complex), atol=1e-12)

    def test_hadamard_creates_superposition(self):
        """H|0> = |+> = (|0> + |1>) / sqrt(2)."""
        from Python.Quantum.core.quantum_operators import QuantumGates
        zero = np.array([1, 0], dtype=complex)
        result = QuantumGates.H @ zero
        expected = np.array([1, 1], dtype=complex) / np.sqrt(2)
        npt.assert_allclose(result, expected, atol=1e-12)

    def test_rotation_gates_unitarity(self):
        """Rx, Ry, Rz should be unitary for any angle."""
        from Python.Quantum.core.quantum_operators import QuantumGates
        I2 = np.eye(2, dtype=complex)
        for theta in [0, np.pi / 4, np.pi / 2, np.pi, 2 * np.pi]:
            for gate_fn in [QuantumGates.Rx, QuantumGates.Ry, QuantumGates.Rz]:
                G = gate_fn(theta)
                npt.assert_allclose(G @ G.conj().T, I2, atol=1e-12)

    def test_rx_pi_equals_negative_i_x(self):
        """Rx(pi) = -i X (up to global phase)."""
        from Python.Quantum.core.quantum_operators import QuantumGates, PauliOperators
        Rx_pi = QuantumGates.Rx(np.pi)
        expected = -1j * PauliOperators.X
        npt.assert_allclose(Rx_pi, expected, atol=1e-12)

    def test_cnot_unitarity(self):
        """CNOT should be unitary."""
        from Python.Quantum.core.quantum_operators import QuantumGates
        cnot = QuantumGates.CNOT()
        I4 = np.eye(4, dtype=complex)
        npt.assert_allclose(cnot @ cnot.conj().T, I4, atol=1e-12)

    def test_cnot_action_on_basis_states(self):
        """CNOT|00>=|00>, CNOT|01>=|01>, CNOT|10>=|11>, CNOT|11>=|10>."""
        from Python.Quantum.core.quantum_operators import QuantumGates
        cnot = QuantumGates.CNOT()
        basis = np.eye(4, dtype=complex)
        # |00> -> |00>
        npt.assert_allclose(cnot @ basis[:, 0], basis[:, 0], atol=1e-12)
        # |01> -> |01>
        npt.assert_allclose(cnot @ basis[:, 1], basis[:, 1], atol=1e-12)
        # |10> -> |11>
        npt.assert_allclose(cnot @ basis[:, 2], basis[:, 3], atol=1e-12)
        # |11> -> |10>
        npt.assert_allclose(cnot @ basis[:, 3], basis[:, 2], atol=1e-12)

    def test_swap_gate(self):
        """SWAP|01> = |10>."""
        from Python.Quantum.core.quantum_operators import QuantumGates
        swap = QuantumGates.SWAP()
        basis01 = np.array([0, 1, 0, 0], dtype=complex)
        basis10 = np.array([0, 0, 1, 0], dtype=complex)
        npt.assert_allclose(swap @ basis01, basis10, atol=1e-12)

    def test_cz_gate(self):
        """CZ only flips phase of |11>."""
        from Python.Quantum.core.quantum_operators import QuantumGates
        cz = QuantumGates.CZ()
        npt.assert_allclose(cz, np.diag([1, 1, 1, -1]).astype(complex), atol=1e-12)

    def test_toffoli_gate_size(self):
        """Toffoli gate should be 8x8."""
        from Python.Quantum.core.quantum_operators import QuantumGates
        toff = QuantumGates.Toffoli()
        assert toff.shape == (8, 8)

    def test_toffoli_gate_unitarity(self):
        from Python.Quantum.core.quantum_operators import QuantumGates
        toff = QuantumGates.Toffoli()
        npt.assert_allclose(toff @ toff.conj().T, np.eye(8, dtype=complex), atol=1e-12)

    def test_toffoli_action(self):
        """Toffoli flips target only when both controls are |1>."""
        from Python.Quantum.core.quantum_operators import QuantumGates
        toff = QuantumGates.Toffoli()
        # |110> -> |111>
        state_110 = np.zeros(8, dtype=complex)
        state_110[6] = 1
        state_111 = np.zeros(8, dtype=complex)
        state_111[7] = 1
        npt.assert_allclose(toff @ state_110, state_111, atol=1e-12)

    def test_fredkin_gate_unitarity(self):
        from Python.Quantum.core.quantum_operators import QuantumGates
        fred = QuantumGates.Fredkin()
        npt.assert_allclose(fred @ fred.conj().T, np.eye(8, dtype=complex), atol=1e-12)

    def test_u3_gate_unitarity(self):
        """U3 gate should be unitary for arbitrary parameters."""
        from Python.Quantum.core.quantum_operators import QuantumGates
        for _ in range(5):
            theta, phi, lam = np.random.uniform(0, 2 * np.pi, 3)
            U = QuantumGates.U3(theta, phi, lam)
            npt.assert_allclose(U @ U.conj().T, np.eye(2, dtype=complex), atol=1e-12)

    def test_controlled_gate(self):
        """controlled_gate(X) should produce CNOT."""
        from Python.Quantum.core.quantum_operators import QuantumGates, PauliOperators
        controlled_x = QuantumGates.controlled_gate(PauliOperators.X, control_qubits=1)
        cnot = QuantumGates.CNOT()
        npt.assert_allclose(controlled_x, cnot, atol=1e-12)


# ---------------------------------------------------------------------------
# HamiltonianOperators
# ---------------------------------------------------------------------------

class TestHamiltonianOperators:
    """Tests for spin-chain Hamiltonians."""

    def test_ising_hermiticity(self):
        """Ising Hamiltonian should be Hermitian."""
        from Python.Quantum.core.quantum_operators import HamiltonianOperators
        H = HamiltonianOperators.ising_1d(3, J=1.0, h=0.5)
        npt.assert_allclose(H, H.conj().T, atol=1e-12)

    def test_ising_dimension(self):
        """Ising H for n sites should be 2^n x 2^n."""
        from Python.Quantum.core.quantum_operators import HamiltonianOperators
        for n in [2, 3, 4]:
            H = HamiltonianOperators.ising_1d(n)
            assert H.shape == (2**n, 2**n)

    def test_heisenberg_hermiticity(self):
        """Heisenberg Hamiltonian should be Hermitian."""
        from Python.Quantum.core.quantum_operators import HamiltonianOperators
        H = HamiltonianOperators.heisenberg_1d(3, J=1.0)
        npt.assert_allclose(H, H.conj().T, atol=1e-12)

    def test_heisenberg_anisotropic(self):
        """Anisotropic Heisenberg with [Jx, Jy, Jz] should still be Hermitian."""
        from Python.Quantum.core.quantum_operators import HamiltonianOperators
        H = HamiltonianOperators.heisenberg_1d(3, J=[1.0, 0.5, 0.8])
        npt.assert_allclose(H, H.conj().T, atol=1e-12)

    def test_hubbard_hermiticity(self):
        """Hubbard Hamiltonian should be Hermitian."""
        from Python.Quantum.core.quantum_operators import HamiltonianOperators
        H = HamiltonianOperators.hubbard_1d(2, t=1.0, U=2.0)
        npt.assert_allclose(H, H.conj().T, atol=1e-10)

    def test_ising_ground_state_trivial(self):
        """2-site Ising with h=0: ground state should be ferromagnetic."""
        from Python.Quantum.core.quantum_operators import HamiltonianOperators
        H = HamiltonianOperators.ising_1d(2, J=1.0, h=0)
        eigenvalues = np.linalg.eigvalsh(H)
        # Ground state energy of -J for 2-site Ising with no field
        npt.assert_allclose(np.min(eigenvalues), -1.0, atol=1e-10)


# ---------------------------------------------------------------------------
# TimeEvolution
# ---------------------------------------------------------------------------

class TestTimeEvolution:
    """Tests for time evolution operators."""

    def test_unitary_evolution_preserves_norm(self):
        """Time evolution should preserve state norm."""
        from Python.Quantum.core.quantum_operators import TimeEvolution
        H = np.array([[1, 0], [0, -1]], dtype=complex)  # Pauli Z
        state = np.array([1, 1], dtype=complex) / np.sqrt(2)
        for t in [0.1, 1.0, 5.0]:
            U = TimeEvolution.unitary_evolution(H, t)
            evolved = U @ state
            npt.assert_allclose(np.linalg.norm(evolved), 1.0, atol=1e-12)

    def test_unitary_evolution_at_zero_time(self):
        """U(t=0) = I."""
        from Python.Quantum.core.quantum_operators import TimeEvolution
        H = np.array([[1, 0.5], [0.5, -1]], dtype=complex)
        U = TimeEvolution.unitary_evolution(H, 0.0)
        npt.assert_allclose(U, np.eye(2, dtype=complex), atol=1e-12)

    def test_unitary_is_actually_unitary(self):
        """U^dag U = I."""
        from Python.Quantum.core.quantum_operators import TimeEvolution
        H = np.array([[0, 1], [1, 0]], dtype=complex)  # Pauli X
        U = TimeEvolution.unitary_evolution(H, 1.0)
        npt.assert_allclose(U @ U.conj().T, np.eye(2, dtype=complex), atol=1e-12)

    def test_trotter_converges_to_exact(self):
        """Trotter decomposition should converge to exact evolution with many steps."""
        from Python.Quantum.core.quantum_operators import TimeEvolution, PauliOperators
        # H = X + Z
        H_list = [PauliOperators.X, PauliOperators.Z]
        H_total = PauliOperators.X + PauliOperators.Z
        t = 0.5
        U_exact = TimeEvolution.unitary_evolution(H_total, t)
        U_trotter = TimeEvolution.trotter_suzuki(H_list, t, n_steps=200, order=2)
        npt.assert_allclose(U_trotter, U_exact, atol=1e-4)


# ---------------------------------------------------------------------------
# OperatorMeasurements
# ---------------------------------------------------------------------------

class TestOperatorMeasurements:
    """Tests for measurement operations."""

    def test_measure_pauli_z_up(self):
        """<0|Z|0> = 1."""
        from Python.Quantum.core.quantum_operators import OperatorMeasurements
        state = np.array([1, 0], dtype=complex)
        result = OperatorMeasurements.measure_pauli(state, 'Z')
        npt.assert_allclose(result, 1.0, atol=1e-12)

    def test_measure_pauli_z_down(self):
        """<1|Z|1> = -1."""
        from Python.Quantum.core.quantum_operators import OperatorMeasurements
        state = np.array([0, 1], dtype=complex)
        result = OperatorMeasurements.measure_pauli(state, 'Z')
        npt.assert_allclose(result, -1.0, atol=1e-12)

    def test_measure_pauli_x_plus(self):
        """<+|X|+> = 1 where |+> = (|0>+|1>)/sqrt(2)."""
        from Python.Quantum.core.quantum_operators import OperatorMeasurements
        state = np.array([1, 1], dtype=complex) / np.sqrt(2)
        result = OperatorMeasurements.measure_pauli(state, 'X')
        npt.assert_allclose(result, 1.0, atol=1e-12)

    def test_projective_measurement_collapses_state(self):
        """Projective measurement should collapse to one of the basis states."""
        from Python.Quantum.core.quantum_operators import OperatorMeasurements
        np.random.seed(42)
        state = np.array([1, 1], dtype=complex) / np.sqrt(2)
        basis = [np.array([1, 0], dtype=complex), np.array([0, 1], dtype=complex)]
        outcome, collapsed = OperatorMeasurements.projective_measurement(state, basis)
        assert outcome in [0, 1]
        npt.assert_allclose(np.linalg.norm(collapsed), 1.0, atol=1e-12)
        # Collapsed state should be one of the basis vectors
        npt.assert_allclose(np.abs(np.vdot(collapsed, basis[outcome])), 1.0, atol=1e-12)
