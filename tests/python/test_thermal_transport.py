"""
Tests for thermal transport modules: heat equation, phonon transport,
thermoelectric effects, heat exchangers, and nanoscale heat transfer.

Covers: Python.Thermal_Transport.core.heat_conduction
        Python.Thermal_Transport.core.heat_equation
"""
import pytest
import numpy as np
import numpy.testing as npt


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def heat_eq():
    """HeatEquation solver with default diffusivity."""
    from Python.Thermal_Transport.core.heat_conduction import HeatEquation
    return HeatEquation(thermal_diffusivity=1e-5)


@pytest.fixture
def heat_solver_1d():
    """HeatEquationSolver1D for a unit rod."""
    from Python.Thermal_Transport.core.heat_equation import HeatEquationSolver1D
    return HeatEquationSolver1D(L=1.0, nx=51, alpha=0.01)


@pytest.fixture
def phonon():
    """PhononTransport model with Si-like parameters."""
    from Python.Thermal_Transport.core.heat_conduction import PhononTransport
    return PhononTransport(debye_temperature=645, sound_velocities=(8433, 5843, 5843))


@pytest.fixture
def thermoelectric():
    from Python.Thermal_Transport.core.heat_conduction import ThermoelectricEffects
    return ThermoelectricEffects()


@pytest.fixture
def heat_exchanger_counter():
    from Python.Thermal_Transport.core.heat_conduction import HeatExchanger
    return HeatExchanger(exchanger_type='counterflow')


@pytest.fixture
def nanoscale():
    from Python.Thermal_Transport.core.heat_conduction import NanoscaleHeatTransfer
    return NanoscaleHeatTransfer()


# ---------------------------------------------------------------------------
# HeatEquation (heat_conduction.py)
# ---------------------------------------------------------------------------

class TestHeatEquation:
    """Tests for the HeatEquation solver."""

    def test_steady_state_linear_profile(self, heat_eq):
        """Steady state with T(0)=0, T(L)=100 and no source should be linear."""
        x = np.linspace(0, 1, 51)
        bc = {
            'left': {'type': 'dirichlet', 'value': 0.0},
            'right': {'type': 'dirichlet', 'value': 100.0}
        }
        T = heat_eq.solve_1d_steady_state(x, bc)
        npt.assert_allclose(T, 100 * x, atol=1.0)

    def test_steady_state_boundary_values(self, heat_eq):
        """Boundary values should match the specified Dirichlet conditions."""
        x = np.linspace(0, 1, 101)
        bc = {
            'left': {'type': 'dirichlet', 'value': 20.0},
            'right': {'type': 'dirichlet', 'value': 80.0}
        }
        T = heat_eq.solve_1d_steady_state(x, bc)
        npt.assert_allclose(T[0], 20.0, atol=1e-6)
        npt.assert_allclose(T[-1], 80.0, atol=1e-6)

    def test_transient_preserves_boundary_conditions(self, heat_eq):
        """Transient solution should maintain Dirichlet BCs at all times."""
        x = np.linspace(0, 1, 51)
        # Use a fine enough time step for stability
        alpha = heat_eq.alpha
        dx = x[1] - x[0]
        dt = 0.4 * dx**2 / alpha  # r = 0.4 < 0.5
        t = np.arange(0, 10 * dt, dt)
        bc = {
            'left': {'type': 'dirichlet', 'value': 0.0},
            'right': {'type': 'dirichlet', 'value': 100.0}
        }
        T = heat_eq.solve_1d_transient(
            x, t,
            initial_condition=lambda x: np.zeros_like(x),
            boundary_conditions=bc
        )
        # Check BCs: left boundary (first spatial point) = 0, right boundary (last spatial point) = 100
        # T shape depends on solver convention (time x space or space x time)
        # Check the boundary values at the last time step
        npt.assert_allclose(T[-1, 0], 0.0, atol=1e-10)
        npt.assert_allclose(T[-1, -1], 100.0, atol=1e-10)

    def test_transient_initial_condition(self, heat_eq):
        """At t=0, solution should match the initial condition."""
        x = np.linspace(0, 1, 51)
        dx = x[1] - x[0]
        dt = 0.4 * dx**2 / heat_eq.alpha
        t = np.arange(0, 5 * dt, dt)
        ic = lambda x: np.sin(np.pi * x)
        bc = {
            'left': {'type': 'dirichlet', 'value': 0.0},
            'right': {'type': 'dirichlet', 'value': 0.0}
        }
        T = heat_eq.solve_1d_transient(x, t, initial_condition=ic, boundary_conditions=bc)
        npt.assert_allclose(T[0, :], np.sin(np.pi * x), atol=1e-10)


# ---------------------------------------------------------------------------
# HeatEquationSolver1D (heat_equation.py)
# ---------------------------------------------------------------------------

class TestHeatEquationSolver1D:
    """Tests for the HeatEquationSolver1D class."""

    def test_initialization(self, heat_solver_1d):
        assert heat_solver_1d.L == 1.0
        assert heat_solver_1d.nx == 51
        assert heat_solver_1d.alpha == 0.01
        assert len(heat_solver_1d.grid) == 51

    def test_dirichlet_boundary_conditions(self, heat_solver_1d):
        """Solution should respect Dirichlet BCs."""
        T_init = np.sin(np.pi * heat_solver_1d.grid)
        # Use stable time step
        dt = 0.4 * heat_solver_1d.dx**2 / heat_solver_1d.alpha
        T_final = heat_solver_1d.solve(T_init, t_final=dt * 10, dt=dt,
                                        T_left=0.0, T_right=0.0)
        npt.assert_allclose(T_final[0], 0.0, atol=1e-10)
        npt.assert_allclose(T_final[-1], 0.0, atol=1e-10)

    def test_neumann_boundary_conditions(self, heat_solver_1d):
        """Neumann (zero-flux) BCs should keep boundary values close to neighbors."""
        T_init = np.ones(heat_solver_1d.nx) * 50.0
        dt = 0.4 * heat_solver_1d.dx**2 / heat_solver_1d.alpha
        T_final = heat_solver_1d.solve(T_init, t_final=dt * 5, dt=dt,
                                        boundary_conditions="neumann")
        # With uniform initial temperature and no flux, should stay uniform
        npt.assert_allclose(T_final, 50.0, atol=1e-6)

    def test_heat_diffuses(self, heat_solver_1d):
        """A peaked initial profile should flatten over time."""
        T_init = np.zeros(heat_solver_1d.nx)
        center = heat_solver_1d.nx // 2
        T_init[center] = 100.0
        dt = 0.4 * heat_solver_1d.dx**2 / heat_solver_1d.alpha
        T_final = heat_solver_1d.solve(T_init, t_final=dt * 100, dt=dt,
                                        T_left=0.0, T_right=0.0)
        # Peak should have decreased
        assert T_final[center] < 100.0
        # Temperature should have spread to neighbors
        assert T_final[center - 1] > 0.0
        assert T_final[center + 1] > 0.0


# ---------------------------------------------------------------------------
# PhononTransport
# ---------------------------------------------------------------------------

class TestPhononTransport:
    """Tests for phonon transport calculations."""

    def test_debye_frequency_positive(self, phonon):
        """Debye frequency should be positive."""
        omega_D = phonon.debye_frequency(density=2329, n_atoms=5e28)
        assert omega_D > 0

    def test_specific_heat_zero_at_zero_temp(self, phonon):
        """Specific heat should be zero at T=0."""
        C_V = phonon.phonon_specific_heat(0)
        assert C_V == 0

    def test_specific_heat_positive(self, phonon):
        """Specific heat should be positive for T > 0."""
        for T in [10, 100, 300, 1000]:
            C_V = phonon.phonon_specific_heat(T)
            assert C_V > 0, f"C_V should be positive at T={T}"

    def test_thermal_conductivity_positive(self, phonon):
        """Kinetic theory conductivity should be positive."""
        kappa = phonon.thermal_conductivity_kinetic(300, mean_free_path=100e-9, density=2329)
        assert kappa > 0

    def test_umklapp_rate_increases_with_temperature(self, phonon):
        """Umklapp scattering rate should increase with temperature."""
        rate_100 = phonon.umklapp_scattering_rate(100)
        rate_300 = phonon.umklapp_scattering_rate(300)
        assert rate_300 > rate_100

    def test_boundary_scattering_rate_positive(self, phonon):
        rate = phonon.boundary_scattering_rate(1e-6)
        assert rate > 0

    def test_bte_relaxation_time_positive(self, phonon):
        """BTE solution should give positive thermal conductivity."""
        rates = [1e10, 5e9]
        kappa = phonon.solve_bte_relaxation_time(300, rates)
        assert kappa > 0


# ---------------------------------------------------------------------------
# ThermoelectricEffects
# ---------------------------------------------------------------------------

class TestThermoelectricEffects:
    """Tests for thermoelectric transport."""

    def test_electrical_conductivity_positive(self, thermoelectric):
        sigma = thermoelectric.electrical_conductivity(1e20, 0.1)
        assert sigma > 0

    def test_thermal_conductivity_electronic(self, thermoelectric):
        """Wiedemann-Franz law: kappa_e = L * sigma * T."""
        sigma = 1e6
        T = 300
        kappa_e = thermoelectric.thermal_conductivity_electronic(sigma, T)
        expected = 2.44e-8 * sigma * T
        npt.assert_allclose(kappa_e, expected, rtol=1e-10)

    def test_figure_of_merit_formula(self, thermoelectric):
        """ZT = S^2 * sigma * T / kappa."""
        S = 200e-6  # 200 uV/K
        sigma = 1e5
        kappa = 1.5
        T = 300
        ZT = thermoelectric.figure_of_merit(S, sigma, kappa, T)
        expected = S**2 * sigma * T / kappa
        npt.assert_allclose(ZT, expected, rtol=1e-10)

    def test_peltier_coefficient(self, thermoelectric):
        """Peltier coefficient Pi = S * T."""
        S = 200e-6
        T = 300
        Pi = thermoelectric.peltier_coefficient(S, T)
        npt.assert_allclose(Pi, S * T, rtol=1e-10)


# ---------------------------------------------------------------------------
# HeatExchanger
# ---------------------------------------------------------------------------

class TestHeatExchanger:
    """Tests for heat exchanger NTU method."""

    def test_effectiveness_zero_ntu(self, heat_exchanger_counter):
        """Effectiveness should be 0 when NTU = 0."""
        eff = heat_exchanger_counter.effectiveness_ntu(0, 0.5)
        npt.assert_allclose(eff, 0.0, atol=1e-10)

    def test_effectiveness_bounded(self, heat_exchanger_counter):
        """Effectiveness should be in [0, 1]."""
        for ntu in [0.1, 1, 5, 10]:
            for cr in [0.0, 0.5, 1.0]:
                eff = heat_exchanger_counter.effectiveness_ntu(ntu, cr)
                assert 0 <= eff <= 1.0 + 1e-10

    def test_counterflow_cr_one(self, heat_exchanger_counter):
        """For C_r = 1, effectiveness = NTU/(1+NTU)."""
        ntu = 2.0
        eff = heat_exchanger_counter.effectiveness_ntu(ntu, 1.0)
        expected = ntu / (1 + ntu)
        npt.assert_allclose(eff, expected, atol=1e-10)

    def test_heat_transfer_rate(self, heat_exchanger_counter):
        """Q = eff * C_min * (T_hot_in - T_cold_in)."""
        eff = 0.8
        c_min = 1000
        t_hot = 100
        t_cold = 20
        q = heat_exchanger_counter.heat_transfer_rate(eff, c_min, t_hot, t_cold)
        expected = 0.8 * 1000 * (100 - 20)
        npt.assert_allclose(q, expected, rtol=1e-10)

    def test_parallel_flow_exchanger(self):
        """Parallel flow should also give bounded effectiveness."""
        from Python.Thermal_Transport.core.heat_conduction import HeatExchanger
        hx = HeatExchanger(exchanger_type='parallel')
        eff = hx.effectiveness_ntu(3.0, 0.5)
        assert 0 <= eff <= 1.0

    def test_unknown_type_raises(self):
        from Python.Thermal_Transport.core.heat_conduction import HeatExchanger
        hx = HeatExchanger(exchanger_type='unknown')
        with pytest.raises(ValueError, match="Unknown heat exchanger type"):
            hx.effectiveness_ntu(1.0, 0.5)


# ---------------------------------------------------------------------------
# NanoscaleHeatTransfer
# ---------------------------------------------------------------------------

class TestNanoscaleHeatTransfer:
    """Tests for nanoscale thermal transport."""

    def test_ballistic_conductance_positive(self, nanoscale):
        G = nanoscale.ballistic_thermal_conductance(300, 1e-14)
        assert G > 0

    def test_ballistic_conductance_proportional_to_temperature(self, nanoscale):
        """G ~ T for ballistic conductance."""
        G1 = nanoscale.ballistic_thermal_conductance(100, 1e-14)
        G2 = nanoscale.ballistic_thermal_conductance(200, 1e-14)
        npt.assert_allclose(G2 / G1, 2.0, rtol=0.01)

    def test_kapitza_resistance_positive(self, nanoscale):
        R = nanoscale.kapitza_resistance(300, 500, 300, 1e-12)
        assert R > 0

    def test_phonon_tunneling_below_wavelength(self, nanoscale):
        """Transmission should be nonzero when gap < wavelength."""
        T = nanoscale.phonon_tunneling(1e-9, 10e-9, 0.5)
        assert T > 0

    def test_phonon_tunneling_above_wavelength(self, nanoscale):
        """Transmission should be zero when gap >= wavelength."""
        T = nanoscale.phonon_tunneling(100e-9, 10e-9, 0.5)
        npt.assert_allclose(T, 0.0, atol=1e-15)

    def test_near_field_radiation_positive(self, nanoscale):
        """Near-field radiation should be positive when T1 > T2."""
        q = nanoscale.near_field_radiation(500, 300, 10e-9, 1e-6, {})
        assert q > 0
