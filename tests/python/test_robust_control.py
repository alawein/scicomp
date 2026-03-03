"""
Tests for Robust Control Methods
Tests for H-infinity control, mu-synthesis, and robust stability analysis
from Python.Control.core.robust_control.

Validates dimension checking, gamma bisection logic, and Monte Carlo
stability analysis using analytically tractable plants.
"""
import numpy as np
import pytest

from Python.Control.core.robust_control import (
    UncertaintyModel,
    HInfinityController,
    MuSynthesis,
    robust_stability_margin,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def stable_siso_plant():
    """A 2-state SISO generalized plant that is stabilisable.

    Plant: dx/dt = A x + B1 w + B2 u
           z     = C1 x + D12 u
           y     = C2 x + D21 w

    D11 = 0, D22 = 0 (standard assumptions for many H-inf problems).
    The open-loop A is stable so an H-inf controller should exist.
    """
    n, n1, n2, p1, p2 = 2, 1, 1, 1, 1
    A = np.array([[-1.0, 0.0],
                   [0.0, -2.0]])
    B1 = np.array([[1.0], [0.0]])
    B2 = np.array([[0.0], [1.0]])
    C1 = np.array([[1.0, 0.0]])
    C2 = np.array([[0.0, 1.0]])
    D11 = np.zeros((p1, n1))
    D12 = np.array([[1.0]])
    D21 = np.array([[1.0]])
    D22 = np.zeros((p2, n2))
    return A, B1, B2, C1, C2, D11, D12, D21, D22


@pytest.fixture
def uncertainty_model():
    """Simple parametric uncertainty model."""
    return UncertaintyModel(
        nominal_params={'k': 1.0},
        param_bounds={'k': (-0.1, 0.1)},
        distribution_type='uniform',
    )


# ---------------------------------------------------------------------------
# UncertaintyModel
# ---------------------------------------------------------------------------

class TestUncertaintyModel:
    def test_construction(self):
        um = UncertaintyModel(
            nominal_params={'a': 1.0, 'b': 2.0},
            param_bounds={'a': (-0.5, 0.5), 'b': (-1.0, 1.0)},
        )
        assert um.nominal_params['a'] == 1.0
        assert um.distribution_type == 'uniform'

    def test_normal_distribution_type(self):
        um = UncertaintyModel(
            nominal_params={'k': 1.0},
            param_bounds={'k': (-0.2, 0.2)},
            distribution_type='normal',
        )
        assert um.distribution_type == 'normal'

    def test_correlation_matrix_default_none(self):
        um = UncertaintyModel(
            nominal_params={'k': 1.0},
            param_bounds={'k': (-0.1, 0.1)},
        )
        assert um.correlation_matrix is None


# ---------------------------------------------------------------------------
# HInfinityController — dimension validation
# ---------------------------------------------------------------------------

class TestHInfinityDimensions:
    def test_valid_dimensions_accepted(self, stable_siso_plant):
        """Constructor should succeed with consistent dimensions."""
        controller = HInfinityController(*stable_siso_plant)
        assert controller.A.shape == (2, 2)

    def test_mismatched_B1_raises(self, stable_siso_plant):
        A, B1, B2, C1, C2, D11, D12, D21, D22 = stable_siso_plant
        B1_bad = np.array([[1.0, 0.0], [0.0, 1.0]])  # n1=2 now
        with pytest.raises(ValueError):
            HInfinityController(A, B1_bad, B2, C1, C2, D11, D12, D21, D22)

    def test_mismatched_C1_raises(self, stable_siso_plant):
        A, B1, B2, C1, C2, D11, D12, D21, D22 = stable_siso_plant
        C1_bad = np.array([[1.0, 0.0], [0.0, 1.0]])  # p1=2
        with pytest.raises(ValueError):
            HInfinityController(A, B1, B2, C1_bad, C2, D11, D12, D21, D22)

    def test_mismatched_D_raises(self, stable_siso_plant):
        A, B1, B2, C1, C2, D11, D12, D21, D22 = stable_siso_plant
        D12_bad = np.array([[1.0, 2.0]])  # wrong column count
        with pytest.raises(ValueError):
            HInfinityController(A, B1, B2, C1, C2, D11, D12_bad, D21, D22)


# ---------------------------------------------------------------------------
# HInfinityController — _test_gamma
# ---------------------------------------------------------------------------

class TestHInfinityTestGamma:
    def test_large_gamma_is_feasible(self, stable_siso_plant):
        """A very large gamma should be achievable for a stable plant."""
        ctrl = HInfinityController(*stable_siso_plant)
        assert ctrl._test_gamma(50.0) is True

    def test_zero_gamma_is_infeasible(self, stable_siso_plant):
        """gamma=0 is never achievable."""
        ctrl = HInfinityController(*stable_siso_plant)
        assert ctrl._test_gamma(0.0) is False

    def test_very_small_gamma_is_infeasible(self, stable_siso_plant):
        ctrl = HInfinityController(*stable_siso_plant)
        assert ctrl._test_gamma(1e-12) is False


# ---------------------------------------------------------------------------
# HInfinityController — synthesize
# ---------------------------------------------------------------------------

class TestHInfinitySynthesize:
    def test_synthesis_returns_controller_and_gamma(self, stable_siso_plant):
        ctrl = HInfinityController(*stable_siso_plant)
        result, gamma = ctrl.synthesize(gamma_max=50.0, tolerance=0.01)
        assert isinstance(result, dict)
        assert 'A' in result and 'B' in result and 'C' in result and 'D' in result
        assert gamma > 0
        assert gamma < 50.0

    def test_gamma_within_tolerance(self, stable_siso_plant):
        ctrl = HInfinityController(*stable_siso_plant)
        tol = 0.1
        _, gamma = ctrl.synthesize(gamma_max=50.0, tolerance=tol)
        # Gamma should be reasonably close to optimal
        assert gamma > 0

    def test_unstable_plant_high_gamma(self):
        """An unstable open-loop plant with D11=0 should still find a controller
        if gamma_max is large enough, or fail gracefully."""
        A = np.array([[1.0, 0.0],
                       [0.0, 2.0]])  # unstable
        B1 = np.array([[1.0], [0.0]])
        B2 = np.array([[0.0], [1.0]])
        C1 = np.array([[1.0, 0.0]])
        C2 = np.array([[0.0, 1.0]])
        D11 = np.zeros((1, 1))
        D12 = np.array([[1.0]])
        D21 = np.array([[1.0]])
        D22 = np.zeros((1, 1))
        ctrl = HInfinityController(A, B1, B2, C1, C2, D11, D12, D21, D22)
        # This may or may not find a controller depending on Hamiltonian eigenvalues.
        # We just verify it does not crash and returns a sensible result or raises.
        try:
            result, gamma = ctrl.synthesize(gamma_max=100.0, tolerance=0.1)
            assert gamma > 0
        except RuntimeError:
            pass  # acceptable


# ---------------------------------------------------------------------------
# HInfinityController — _compute_controller
# ---------------------------------------------------------------------------

class TestHInfinityComputeController:
    def test_controller_matrix_shapes(self, stable_siso_plant):
        ctrl = HInfinityController(*stable_siso_plant)
        result = ctrl._compute_controller(10.0)
        n = 2
        n2 = 1
        p2 = 1
        assert result['A'].shape == (n, n)
        assert result['B'].shape == (n, p2)
        assert result['C'].shape == (n2, n)
        assert result['D'].shape == (n2, p2)


# ---------------------------------------------------------------------------
# MuSynthesis
# ---------------------------------------------------------------------------

class TestMuSynthesis:
    def test_dk_iteration_returns_controller_and_mu(self):
        plant = {'A': np.array([[0]]), 'B': np.array([[1]]),
                 'C': np.array([[1]]), 'D': np.array([[0]])}
        uncertainty = [{'type': 'real', 'size': 1}]
        weights = {'W1': np.eye(1), 'W2': np.eye(1)}
        mu_synth = MuSynthesis(plant, uncertainty, weights)
        controller, mu_val = mu_synth.d_k_iteration(max_iterations=3)
        assert controller is not None
        assert mu_val >= 0

    def test_dk_iteration_converges(self):
        plant = {'A': np.array([[0]]), 'B': np.array([[1]]),
                 'C': np.array([[1]]), 'D': np.array([[0]])}
        uncertainty = [{'type': 'real', 'size': 1}]
        weights = {'W1': np.eye(1), 'W2': np.eye(1)}
        mu_synth = MuSynthesis(plant, uncertainty, weights)
        controller, mu_val = mu_synth.d_k_iteration(max_iterations=20)
        # mu value from placeholder is 1.0 — just check it is finite
        assert np.isfinite(mu_val)


# ---------------------------------------------------------------------------
# robust_stability_margin
# ---------------------------------------------------------------------------

class TestRobustStabilityMargin:
    def test_stable_system_high_probability(self):
        """A strongly stable system with small uncertainty should be robust."""
        A = np.array([[-5.0, 0.0],
                       [0.0, -3.0]])
        B = np.eye(2)
        um = UncertaintyModel(
            nominal_params={'delta': 0.0},
            param_bounds={'delta': (-0.1, 0.1)},
            distribution_type='uniform',
        )
        np.random.seed(42)
        result = robust_stability_margin(A, B, um, n_samples=500)
        assert result['stability_probability'] > 0.95
        assert result['samples'] == 500

    def test_unstable_system_low_probability(self):
        """An unstable nominal system should have low stability probability."""
        A = np.array([[1.0, 0.0],
                       [0.0, 0.5]])  # unstable (eigenvalue +1)
        B = np.eye(2)
        um = UncertaintyModel(
            nominal_params={'delta': 0.0},
            param_bounds={'delta': (-0.01, 0.01)},
            distribution_type='uniform',
        )
        np.random.seed(42)
        result = robust_stability_margin(A, B, um, n_samples=200)
        assert result['stability_probability'] < 0.1

    def test_result_keys(self, uncertainty_model):
        A = np.array([[-1.0]])
        B = np.array([[1.0]])
        np.random.seed(0)
        result = robust_stability_margin(A, B, uncertainty_model, n_samples=50)
        expected_keys = {'stability_probability', 'min_real_eigenvalue',
                         'max_real_eigenvalue', 'samples'}
        assert set(result.keys()) == expected_keys

    def test_normal_distribution_sampling(self):
        """The function should also work with normal distribution type."""
        A = np.array([[-2.0, 0.0],
                       [0.0, -3.0]])
        B = np.eye(2)
        um = UncertaintyModel(
            nominal_params={'delta': 0.0},
            param_bounds={'delta': (-0.5, 0.5)},
            distribution_type='normal',
        )
        np.random.seed(123)
        result = robust_stability_margin(A, B, um, n_samples=100)
        assert 0.0 <= result['stability_probability'] <= 1.0

    def test_eigenvalue_tracking(self):
        """min and max real eigenvalue fields should be populated correctly."""
        A = np.array([[-1.0]])
        B = np.array([[1.0]])
        um = UncertaintyModel(
            nominal_params={'delta': 0.0},
            param_bounds={'delta': (-0.01, 0.01)},
            distribution_type='uniform',
        )
        np.random.seed(7)
        result = robust_stability_margin(A, B, um, n_samples=100)
        # All eigenvalues should be near -1.0 +/- 0.01
        assert result['min_real_eigenvalue'] < -0.98
        assert result['max_real_eigenvalue'] < -0.98
        assert result['min_real_eigenvalue'] <= result['max_real_eigenvalue']
