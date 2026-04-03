"""
Tests for utility modules: physical constants, unit conversions, and derived quantities.

Covers: Python.utils.constants
        Python.utils.units
"""
import pytest
import numpy as np
import numpy.testing as npt


# ---------------------------------------------------------------------------
# Physical constants
# ---------------------------------------------------------------------------

class TestPhysicalConstants:
    """Tests for CODATA physical constants."""

    def test_speed_of_light(self):
        from Python.utils.constants import c
        npt.assert_allclose(c, 299792458.0, rtol=1e-15)

    def test_planck_constant(self):
        from Python.utils.constants import h
        npt.assert_allclose(h, 6.62607015e-34, rtol=1e-10)

    def test_reduced_planck_constant(self):
        from Python.utils.constants import h, hbar
        npt.assert_allclose(hbar, h / (2 * np.pi), rtol=1e-10)

    def test_elementary_charge(self):
        from Python.utils.constants import e
        npt.assert_allclose(e, 1.602176634e-19, rtol=1e-10)

    def test_boltzmann_constant(self):
        from Python.utils.constants import kb
        npt.assert_allclose(kb, 1.380649e-23, rtol=1e-10)

    def test_electron_mass(self):
        from Python.utils.constants import me
        npt.assert_allclose(me, 9.1093837015e-31, rtol=1e-6)

    def test_fine_structure_constant(self):
        """alpha ~ 1/137."""
        from Python.utils.constants import alpha
        npt.assert_allclose(alpha, 1 / 137.036, rtol=1e-3)

    def test_constants_dict_completeness(self):
        """PHYSICAL_CONSTANTS dict should contain at least the core constants."""
        from Python.utils.constants import PHYSICAL_CONSTANTS
        expected_keys = [
            'speed_of_light', 'planck_constant', 'reduced_planck_constant',
            'elementary_charge', 'boltzmann_constant', 'electron_mass',
            'proton_mass', 'bohr_radius', 'fine_structure_constant',
        ]
        for key in expected_keys:
            assert key in PHYSICAL_CONSTANTS, f"Missing constant: {key}"

    def test_constants_have_units(self):
        """Each constant entry should have a 'unit' field."""
        from Python.utils.constants import PHYSICAL_CONSTANTS
        for name, data in PHYSICAL_CONSTANTS.items():
            assert 'unit' in data, f"Constant {name} missing 'unit' field"
            assert 'value' in data, f"Constant {name} missing 'value' field"


# ---------------------------------------------------------------------------
# Temperature conversions
# ---------------------------------------------------------------------------

class TestTemperatureConversions:
    """Tests for temperature conversion functions."""

    def test_celsius_to_kelvin_boiling(self):
        from Python.utils.constants import celsius_to_kelvin
        npt.assert_allclose(celsius_to_kelvin(100), 373.15, atol=1e-10)

    def test_celsius_to_kelvin_freezing(self):
        from Python.utils.constants import celsius_to_kelvin
        npt.assert_allclose(celsius_to_kelvin(0), 273.15, atol=1e-10)

    def test_kelvin_to_celsius_roundtrip(self):
        from Python.utils.constants import celsius_to_kelvin, kelvin_to_celsius
        T = 42.0
        npt.assert_allclose(kelvin_to_celsius(celsius_to_kelvin(T)), T, atol=1e-10)

    def test_fahrenheit_to_kelvin_boiling(self):
        from Python.utils.constants import fahrenheit_to_kelvin
        npt.assert_allclose(fahrenheit_to_kelvin(212), 373.15, atol=1e-10)

    def test_kelvin_to_fahrenheit_roundtrip(self):
        from Python.utils.constants import fahrenheit_to_kelvin, kelvin_to_fahrenheit
        T = 98.6
        npt.assert_allclose(kelvin_to_fahrenheit(fahrenheit_to_kelvin(T)), T, atol=1e-10)


# ---------------------------------------------------------------------------
# Energy conversions
# ---------------------------------------------------------------------------

class TestEnergyConversions:
    """Tests for energy unit conversion functions."""

    def test_eV_to_wavenumber_and_back(self):
        from Python.utils.constants import eV_to_wavenumber, wavenumber_to_eV
        E = 1.0  # 1 eV
        wn = eV_to_wavenumber(E)
        assert wn > 0
        npt.assert_allclose(wavenumber_to_eV(wn), E, rtol=1e-6)

    def test_eV_to_frequency_and_back(self):
        from Python.utils.constants import eV_to_frequency, frequency_to_eV
        E = 2.0
        f = eV_to_frequency(E)
        assert f > 0
        npt.assert_allclose(frequency_to_eV(f), E, rtol=1e-6)

    def test_eV_to_wavelength_and_back(self):
        from Python.utils.constants import eV_to_wavelength, wavelength_to_eV
        E = 1.5
        lam = eV_to_wavelength(E)
        assert lam > 0
        npt.assert_allclose(wavelength_to_eV(lam), E, rtol=1e-6)

    def test_eV_to_J_conversion(self):
        from Python.utils.constants import eV_to_J, J_to_eV
        npt.assert_allclose(eV_to_J * J_to_eV, 1.0, rtol=1e-15)


# ---------------------------------------------------------------------------
# Atomic unit conversions
# ---------------------------------------------------------------------------

class TestAtomicUnitConversions:
    """Tests for atomic unit conversion functions."""

    def test_energy_roundtrip(self):
        from Python.utils.constants import convert_to_atomic_units, convert_from_atomic_units
        E_si = 4.3597e-18  # ~ 1 Hartree
        E_au = convert_to_atomic_units(E_si, 'energy')
        E_back = convert_from_atomic_units(E_au, 'energy')
        npt.assert_allclose(E_back, E_si, rtol=1e-4)

    def test_length_roundtrip(self):
        from Python.utils.constants import convert_to_atomic_units, convert_from_atomic_units
        L_si = 5.29e-11  # ~ 1 Bohr radius
        L_au = convert_to_atomic_units(L_si, 'length')
        L_back = convert_from_atomic_units(L_au, 'length')
        npt.assert_allclose(L_back, L_si, rtol=1e-3)

    def test_mass_roundtrip(self):
        from Python.utils.constants import convert_to_atomic_units, convert_from_atomic_units
        m_si = 9.109e-31  # ~ electron mass
        m_au = convert_to_atomic_units(m_si, 'mass')
        npt.assert_allclose(m_au, 1.0, rtol=1e-3)

    def test_unknown_unit_type_raises(self):
        from Python.utils.constants import convert_to_atomic_units
        with pytest.raises(ValueError, match="Unknown unit type"):
            convert_to_atomic_units(1.0, 'foobar')


# ---------------------------------------------------------------------------
# Derived constants
# ---------------------------------------------------------------------------

class TestDerivedConstants:
    """Tests for derived physical quantities."""

    def test_compton_wavelength_electron(self):
        from Python.utils.constants import compton_wavelength, me
        lam_c = compton_wavelength(me)
        # Electron Compton wavelength ~ 2.426e-12 m
        npt.assert_allclose(lam_c, 2.426e-12, rtol=1e-2)

    def test_classical_electron_radius(self):
        from Python.utils.constants import classical_electron_radius
        r_e = classical_electron_radius()
        # ~ 2.818e-15 m
        npt.assert_allclose(r_e, 2.818e-15, rtol=1e-2)

    def test_cyclotron_frequency_positive(self):
        from Python.utils.constants import cyclotron_frequency
        omega_c = cyclotron_frequency(1.0)  # 1 Tesla
        assert omega_c > 0

    def test_plasma_frequency_positive(self):
        from Python.utils.constants import plasma_frequency
        omega_p = plasma_frequency(1e20)
        assert omega_p > 0

    def test_debye_length_positive(self):
        from Python.utils.constants import debye_length
        lam_D = debye_length(1e4, 1e20)
        assert lam_D > 0

    def test_thermal_de_broglie_wavelength_positive(self):
        from Python.utils.constants import thermal_de_broglie_wavelength
        lam = thermal_de_broglie_wavelength(300)
        assert lam > 0


# ---------------------------------------------------------------------------
# UnitConverter
# ---------------------------------------------------------------------------

class TestUnitConverter:
    """Tests for the UnitConverter class."""

    @pytest.fixture
    def converter(self):
        from Python.utils.units import UnitConverter
        return UnitConverter()

    def test_energy_eV_to_J(self, converter):
        """1 eV ~ 1.602e-19 J."""
        result = converter.convert(1.0, 'eV', 'J', 'energy')
        npt.assert_allclose(result, 1.602176634e-19, rtol=1e-6)

    def test_energy_identity(self, converter):
        """Converting eV to eV should be identity."""
        result = converter.convert(42.0, 'eV', 'eV', 'energy')
        npt.assert_allclose(result, 42.0, rtol=1e-15)

    def test_length_angstrom_to_nm(self, converter):
        """1 Angstrom = 0.1 nm."""
        result = converter.convert(1.0, 'angstrom', 'nm', 'length')
        npt.assert_allclose(result, 0.1, rtol=1e-10)

    def test_length_bohr_to_angstrom(self, converter):
        """1 Bohr ~ 0.529 Angstrom."""
        result = converter.convert(1.0, 'bohr', 'angstrom', 'length')
        npt.assert_allclose(result, 0.529177, rtol=1e-3)

    def test_time_fs_to_ps(self, converter):
        """1000 fs = 1 ps."""
        result = converter.convert(1000.0, 'fs', 'ps', 'time')
        npt.assert_allclose(result, 1.0, rtol=1e-10)

    def test_mass_amu_to_kg(self, converter):
        """1 amu ~ 1.66e-27 kg."""
        result = converter.convert(1.0, 'amu', 'kg', 'mass')
        npt.assert_allclose(result, 1.66053906660e-27, rtol=1e-6)

    def test_pressure_atm_to_pa(self, converter):
        """1 atm = 101325 Pa."""
        result = converter.convert(1.0, 'atm', 'Pa', 'pressure')
        npt.assert_allclose(result, 101325.0, rtol=1e-10)

    def test_magnetic_field_gauss_to_tesla(self, converter):
        """10000 Gauss = 1 Tesla."""
        result = converter.convert(10000.0, 'G', 'T', 'magnetic_field')
        npt.assert_allclose(result, 1.0, rtol=1e-10)

    def test_unknown_quantity_type_raises(self, converter):
        with pytest.raises(ValueError, match="Unknown quantity type"):
            converter.convert(1.0, 'eV', 'J', 'unknown_type')

    def test_unknown_unit_raises(self, converter):
        with pytest.raises(ValueError, match="Unknown energy unit"):
            converter.convert(1.0, 'invalid_unit', 'J', 'energy')

    def test_array_conversion(self, converter):
        """Converter should work with numpy arrays."""
        values = np.array([1.0, 2.0, 3.0])
        result = converter.convert(values, 'eV', 'meV', 'energy')
        npt.assert_allclose(result, values * 1000, rtol=1e-10)


# ---------------------------------------------------------------------------
# Convenience functions
# ---------------------------------------------------------------------------

class TestConvenienceFunctions:
    """Tests for module-level convenience conversion functions."""

    def test_energy_convert(self):
        from Python.utils.units import energy_convert
        result = energy_convert(1.0, 'Ha', 'eV')
        # 1 Hartree ~ 27.2 eV
        npt.assert_allclose(result, 27.2114, rtol=1e-3)

    def test_length_convert(self):
        from Python.utils.units import length_convert
        result = length_convert(1.0, 'nm', 'angstrom')
        npt.assert_allclose(result, 10.0, rtol=1e-10)

    def test_time_convert(self):
        from Python.utils.units import time_convert
        result = time_convert(1.0, 'ns', 'ps')
        npt.assert_allclose(result, 1000.0, rtol=1e-10)

    def test_mass_convert(self):
        from Python.utils.units import mass_convert
        result = mass_convert(1.0, 'kg', 'g')
        npt.assert_allclose(result, 1000.0, rtol=1e-10)

    def test_pressure_convert(self):
        from Python.utils.units import pressure_convert
        result = pressure_convert(1.0, 'GPa', 'MPa')
        npt.assert_allclose(result, 1000.0, rtol=1e-10)
