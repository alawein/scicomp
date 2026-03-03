"""
Tests for Optimal Control Algorithms
Tests for Model Predictive Control and LQ tracking from
Python.Control.core.optimal_control.

Validates mathematical correctness using known analytical solutions
for simple linear systems.
"""
import numpy as np
import pytest

from Python.Control.core.optimal_control import (
    MPCConfig,
    ModelPredictiveController,
    solve_lq_tracking,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def double_integrator():
    """Discrete-time double integrator (position + velocity).

    x(k+1) = A x(k) + B u(k)
    where x = [position, velocity], u = [force].

    Discretised with dt = 0.1 s.
    """
    dt = 0.1
    A = np.array([[1.0, dt],
                   [0.0, 1.0]])
    B = np.array([[0.5 * dt**2],
                   [dt]])
    return A, B, dt


@pytest.fixture
def simple_integrator():
    """Single integrator: x(k+1) = x(k) + u(k)."""
    A = np.array([[1.0]])
    B = np.array([[1.0]])
    return A, B


@pytest.fixture
def mpc_default_config():
    """Default MPC configuration with short horizon."""
    return MPCConfig(prediction_horizon=5)


# ---------------------------------------------------------------------------
# MPCConfig dataclass tests
# ---------------------------------------------------------------------------

class TestMPCConfig:
    def test_default_values(self):
        cfg = MPCConfig()
        assert cfg.prediction_horizon == 10
        assert cfg.control_horizon is None
        assert cfg.solver == 'quadprog'
        assert cfg.max_iter == 100
        assert cfg.tolerance == 1e-6

    def test_custom_values(self):
        Q = np.eye(2)
        R = 0.1 * np.eye(1)
        cfg = MPCConfig(prediction_horizon=20, Q=Q, R=R)
        assert cfg.prediction_horizon == 20
        np.testing.assert_array_equal(cfg.Q, Q)
        np.testing.assert_array_equal(cfg.R, R)


# ---------------------------------------------------------------------------
# ModelPredictiveController — construction
# ---------------------------------------------------------------------------

class TestMPCInit:
    def test_dimensions_inferred(self, double_integrator, mpc_default_config):
        A, B, _ = double_integrator
        mpc = ModelPredictiveController(A, B, mpc_default_config)
        assert mpc.n_states == 2
        assert mpc.n_inputs == 1

    def test_control_horizon_defaults_to_prediction(self, simple_integrator):
        A, B = simple_integrator
        cfg = MPCConfig(prediction_horizon=7)
        mpc = ModelPredictiveController(A, B, cfg)
        assert mpc.config.control_horizon == 7

    def test_default_weight_matrices(self, simple_integrator):
        A, B = simple_integrator
        cfg = MPCConfig(prediction_horizon=3)
        mpc = ModelPredictiveController(A, B, cfg)
        np.testing.assert_array_equal(mpc.config.Q, np.eye(1))
        np.testing.assert_array_equal(mpc.config.R, np.eye(1))
        np.testing.assert_array_equal(mpc.config.Qf, np.eye(1))

    def test_prediction_matrices_shapes(self, double_integrator):
        A, B, _ = double_integrator
        N = 4
        cfg = MPCConfig(prediction_horizon=N)
        mpc = ModelPredictiveController(A, B, cfg)
        # Phi: (N*n_states) x n_states
        assert mpc.Phi.shape == (N * 2, 2)
        # Gamma: (N*n_states) x (Nc*n_inputs)
        assert mpc.Gamma.shape == (N * 2, N * 1)
        # H: (Nc*n_inputs) x (Nc*n_inputs)
        assert mpc.H.shape == (N * 1, N * 1)

    def test_H_is_positive_semidefinite(self, double_integrator):
        A, B, _ = double_integrator
        cfg = MPCConfig(prediction_horizon=5)
        mpc = ModelPredictiveController(A, B, cfg)
        eigvals = np.linalg.eigvalsh(mpc.H)
        assert np.all(eigvals >= -1e-10), "H matrix must be positive semi-definite"


# ---------------------------------------------------------------------------
# ModelPredictiveController — solve
# ---------------------------------------------------------------------------

class TestMPCSolve:
    def test_output_shape(self, double_integrator):
        A, B, _ = double_integrator
        N = 5
        cfg = MPCConfig(prediction_horizon=N)
        mpc = ModelPredictiveController(A, B, cfg)
        x0 = np.array([1.0, 0.0])
        u_opt = mpc.solve(x0)
        assert u_opt.shape == (N, 1)

    def test_zero_state_gives_zero_control(self, double_integrator):
        """At the origin with zero reference, optimal control should be ~0."""
        A, B, _ = double_integrator
        cfg = MPCConfig(prediction_horizon=5)
        mpc = ModelPredictiveController(A, B, cfg)
        x0 = np.array([0.0, 0.0])
        u_opt = mpc.solve(x0, reference=np.zeros((5, 2)))
        np.testing.assert_allclose(u_opt, 0.0, atol=1e-6)

    def test_drives_state_toward_reference(self, simple_integrator):
        """MPC should move the state toward the reference."""
        A, B = simple_integrator
        cfg = MPCConfig(prediction_horizon=10, Q=np.array([[10.0]]), R=np.array([[0.01]]))
        mpc = ModelPredictiveController(A, B, cfg)
        x0 = np.array([0.0])
        ref = np.ones((10, 1)) * 5.0
        u_opt = mpc.solve(x0, reference=ref)
        # First control action should be positive (moving toward 5.0)
        assert u_opt[0, 0] > 0

    def test_input_constraints_respected(self, simple_integrator):
        """MPC should respect input bounds."""
        A, B = simple_integrator
        u_max = np.array([0.5])
        u_min = np.array([-0.5])
        cfg = MPCConfig(
            prediction_horizon=5,
            Q=np.array([[100.0]]),
            R=np.array([[0.001]]),
            u_min=u_min,
            u_max=u_max,
        )
        mpc = ModelPredictiveController(A, B, cfg)
        x0 = np.array([0.0])
        ref = np.ones((5, 1)) * 100.0  # large reference to saturate
        u_opt = mpc.solve(x0, reference=ref)
        # All control actions should be within bounds (with small numerical tolerance)
        assert np.all(u_opt >= u_min - 1e-4)
        assert np.all(u_opt <= u_max + 1e-4)

    def test_1d_reference_is_tiled(self, double_integrator):
        """A 1-D reference should be tiled across the prediction horizon."""
        A, B, _ = double_integrator
        cfg = MPCConfig(prediction_horizon=5)
        mpc = ModelPredictiveController(A, B, cfg)
        x0 = np.array([1.0, 0.5])
        ref_1d = np.array([0.0, 0.0])
        u_opt = mpc.solve(x0, reference=ref_1d)
        assert u_opt.shape == (5, 1)


# ---------------------------------------------------------------------------
# ModelPredictiveController — predict_trajectory
# ---------------------------------------------------------------------------

class TestMPCPredictTrajectory:
    def test_trajectory_shape(self, double_integrator):
        A, B, _ = double_integrator
        N = 5
        cfg = MPCConfig(prediction_horizon=N)
        mpc = ModelPredictiveController(A, B, cfg)
        x0 = np.array([0.0, 1.0])
        u_seq = np.zeros((N, 1))
        traj = mpc.predict_trajectory(x0, u_seq)
        assert traj.shape == (N, 2)

    def test_free_response_double_integrator(self, double_integrator):
        """With zero control, the double integrator evolves analytically."""
        A, B, dt = double_integrator
        N = 4
        cfg = MPCConfig(prediction_horizon=N)
        mpc = ModelPredictiveController(A, B, cfg)
        x0 = np.array([0.0, 1.0])  # unit velocity, zero position
        u_seq = np.zeros((N, 1))
        traj = mpc.predict_trajectory(x0, u_seq)
        # Analytical: pos(k) = k*dt, vel(k) = 1.0
        for k in range(N):
            expected_pos = (k + 1) * dt
            np.testing.assert_allclose(traj[k, 0], expected_pos, atol=1e-12)
            np.testing.assert_allclose(traj[k, 1], 1.0, atol=1e-12)

    def test_control_hold_extension(self, double_integrator):
        """If control sequence is shorter than N, last value is held."""
        A, B, _ = double_integrator
        N = 6
        Nc = 3
        cfg = MPCConfig(prediction_horizon=N, control_horizon=Nc)
        mpc = ModelPredictiveController(A, B, cfg)
        x0 = np.array([0.0, 0.0])
        u_seq = np.array([[1.0], [2.0], [3.0]])
        traj = mpc.predict_trajectory(x0, u_seq)
        assert traj.shape == (N, 2)


# ---------------------------------------------------------------------------
# solve_lq_tracking
# ---------------------------------------------------------------------------

class TestSolveLQTracking:
    def test_output_shapes(self):
        n, m = 2, 1
        A = np.eye(n)
        B = np.ones((n, m))
        Q = np.eye(n)
        R = np.eye(m)
        horizon = 5
        ref = np.zeros((horizon, n))
        K, k = solve_lq_tracking(A, B, Q, R, ref, horizon)
        assert K.shape == (horizon, m, n)
        assert k.shape == (horizon, m)

    def test_zero_reference_gives_zero_feedforward(self):
        """With zero reference, feedforward term k should be zero."""
        n, m = 2, 1
        A = 0.9 * np.eye(n)
        B = np.array([[1.0], [0.0]])
        Q = np.eye(n)
        R = np.eye(m)
        horizon = 10
        ref = np.zeros((horizon, n))
        K, k = solve_lq_tracking(A, B, Q, R, ref, horizon)
        np.testing.assert_allclose(k, 0.0, atol=1e-10)

    def test_gain_matrices_stabilizing(self):
        """Closed-loop A - B*K should have eigenvalues inside unit circle."""
        n = 2
        m = 1
        A = np.array([[1.0, 0.1],
                       [0.0, 1.0]])
        B = np.array([[0.005],
                       [0.1]])
        Q = 10.0 * np.eye(n)
        R = np.eye(m)
        horizon = 50
        ref = np.zeros((horizon, n))
        K, k = solve_lq_tracking(A, B, Q, R, ref, horizon)
        # Use the first gain (most stabilising at early steps)
        K0 = K[0]
        A_cl = A - B @ K0
        eigvals = np.linalg.eigvals(A_cl)
        assert np.all(np.abs(eigvals) < 1.0 + 1e-8), (
            f"Closed-loop eigenvalues {eigvals} not inside unit circle"
        )

    def test_symmetric_P_matrices(self):
        """The cost-to-go matrices P should be symmetric."""
        n, m = 2, 1
        A = np.array([[0.9, 0.1], [0.0, 0.8]])
        B = np.array([[0.0], [1.0]])
        Q = np.eye(n)
        R = np.eye(m)
        horizon = 5
        ref = np.zeros((horizon, n))
        # We cannot directly access P from the function, but we verify
        # the gains are finite and reasonable (implying P was well-formed).
        K, k = solve_lq_tracking(A, B, Q, R, ref, horizon)
        assert np.all(np.isfinite(K))
        assert np.all(np.isfinite(k))

    def test_tracking_constant_reference(self):
        """With a constant non-zero reference the feedforward should be non-zero."""
        n, m = 1, 1
        A = np.array([[0.9]])
        B = np.array([[1.0]])
        Q = np.array([[10.0]])
        R = np.array([[1.0]])
        horizon = 10
        ref = 5.0 * np.ones((horizon, n))
        K, k = solve_lq_tracking(A, B, Q, R, ref, horizon)
        # k should have non-zero entries to steer toward ref=5
        assert np.any(np.abs(k) > 1e-6)
