"""
Tests for Crystal Structure Analysis
Tests for lattice parameters, coordinate transformations, d-spacing,
Bragg angles, and supercell generation from
Python.Crystallography.core.crystal_structure.

Uses well-known crystallographic results for cubic, hexagonal, and
orthorhombic systems as analytical references.
"""
import numpy as np
import pytest

from Python.Crystallography.core.crystal_structure import (
    LatticeParameters,
    AtomicPosition,
    CrystalStructure,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def cubic_lattice():
    """Simple cubic lattice with a = 5 Angstrom."""
    return LatticeParameters(a=5.0, b=5.0, c=5.0, alpha=90, beta=90, gamma=90)


@pytest.fixture
def si_diamond():
    """Silicon diamond structure (Fd3m, a = 5.431 A)."""
    lattice = LatticeParameters(a=5.431, b=5.431, c=5.431,
                                 alpha=90, beta=90, gamma=90)
    atoms = [
        AtomicPosition('Si', 0.0, 0.0, 0.0),
        AtomicPosition('Si', 0.5, 0.5, 0.0),
        AtomicPosition('Si', 0.5, 0.0, 0.5),
        AtomicPosition('Si', 0.0, 0.5, 0.5),
        AtomicPosition('Si', 0.25, 0.25, 0.25),
        AtomicPosition('Si', 0.75, 0.75, 0.25),
        AtomicPosition('Si', 0.75, 0.25, 0.75),
        AtomicPosition('Si', 0.25, 0.75, 0.75),
    ]
    return CrystalStructure(lattice, atoms)


@pytest.fixture
def simple_cubic_crystal():
    """Simple cubic with one atom at the origin, a = 3.0 A."""
    lattice = LatticeParameters(a=3.0, b=3.0, c=3.0, alpha=90, beta=90, gamma=90)
    atoms = [AtomicPosition('Fe', 0.0, 0.0, 0.0)]
    return CrystalStructure(lattice, atoms)


@pytest.fixture
def bcc_crystal():
    """BCC structure (e.g., iron), a = 2.87 A."""
    lattice = LatticeParameters(a=2.87, b=2.87, c=2.87, alpha=90, beta=90, gamma=90)
    atoms = [
        AtomicPosition('Fe', 0.0, 0.0, 0.0),
        AtomicPosition('Fe', 0.5, 0.5, 0.5),
    ]
    return CrystalStructure(lattice, atoms)


@pytest.fixture
def hexagonal_lattice():
    """Hexagonal lattice: a = b = 3.0, c = 5.0, alpha=beta=90, gamma=120."""
    return LatticeParameters(a=3.0, b=3.0, c=5.0, alpha=90, beta=90, gamma=120)


# ---------------------------------------------------------------------------
# LatticeParameters
# ---------------------------------------------------------------------------

class TestLatticeParameters:
    def test_valid_cubic(self, cubic_lattice):
        assert cubic_lattice.a == 5.0
        assert cubic_lattice.alpha == 90

    def test_angle_conversion(self, cubic_lattice):
        np.testing.assert_allclose(cubic_lattice.alpha_rad, np.pi / 2)
        np.testing.assert_allclose(cubic_lattice.beta_rad, np.pi / 2)
        np.testing.assert_allclose(cubic_lattice.gamma_rad, np.pi / 2)

    def test_hexagonal_gamma(self, hexagonal_lattice):
        np.testing.assert_allclose(hexagonal_lattice.gamma_rad, 2 * np.pi / 3)

    def test_negative_length_raises(self):
        with pytest.raises(ValueError, match="positive"):
            LatticeParameters(a=-1, b=1, c=1, alpha=90, beta=90, gamma=90)

    def test_zero_length_raises(self):
        with pytest.raises(ValueError, match="positive"):
            LatticeParameters(a=0, b=1, c=1, alpha=90, beta=90, gamma=90)

    def test_invalid_angle_raises(self):
        with pytest.raises(ValueError, match="between 0 and 180"):
            LatticeParameters(a=1, b=1, c=1, alpha=0, beta=90, gamma=90)
        with pytest.raises(ValueError, match="between 0 and 180"):
            LatticeParameters(a=1, b=1, c=1, alpha=90, beta=180, gamma=90)


# ---------------------------------------------------------------------------
# AtomicPosition
# ---------------------------------------------------------------------------

class TestAtomicPosition:
    def test_valid_atom(self):
        atom = AtomicPosition('Si', 0.25, 0.25, 0.25)
        assert atom.element == 'Si'
        assert atom.occupancy == 1.0

    def test_custom_occupancy(self):
        atom = AtomicPosition('Fe', 0.0, 0.0, 0.0, occupancy=0.5)
        assert atom.occupancy == 0.5

    def test_invalid_occupancy_raises(self):
        with pytest.raises(ValueError, match="Occupancy"):
            AtomicPosition('Si', 0, 0, 0, occupancy=1.5)

    def test_negative_thermal_factor_raises(self):
        with pytest.raises(ValueError, match="Thermal factor"):
            AtomicPosition('Si', 0, 0, 0, thermal_factor=-1.0)


# ---------------------------------------------------------------------------
# CrystalStructure — unit cell volume
# ---------------------------------------------------------------------------

class TestUnitCellVolume:
    def test_cubic_volume(self, simple_cubic_crystal):
        """V = a^3 for cubic."""
        vol = simple_cubic_crystal.unit_cell_volume()
        np.testing.assert_allclose(vol, 27.0, rtol=1e-10)

    def test_silicon_volume(self, si_diamond):
        expected = 5.431 ** 3
        np.testing.assert_allclose(si_diamond.unit_cell_volume(), expected, rtol=1e-6)

    def test_hexagonal_volume(self):
        """V = a^2 * c * sin(120) for hexagonal."""
        lattice = LatticeParameters(a=3.0, b=3.0, c=5.0,
                                     alpha=90, beta=90, gamma=120)
        atoms = [AtomicPosition('Zn', 0.0, 0.0, 0.0)]
        crystal = CrystalStructure(lattice, atoms)
        expected = 3.0**2 * 5.0 * np.sin(np.radians(120))
        np.testing.assert_allclose(crystal.unit_cell_volume(), expected, rtol=1e-6)


# ---------------------------------------------------------------------------
# CrystalStructure — density
# ---------------------------------------------------------------------------

class TestDensity:
    def test_silicon_density(self, si_diamond):
        """Silicon density ~ 2.33 g/cm^3 (8 atoms, MW = 28.085 g/mol, Z=8)."""
        density = si_diamond.density(molecular_weight=28.085, z=8)
        np.testing.assert_allclose(density, 2.33, atol=0.02)

    def test_iron_bcc_density(self, bcc_crystal):
        """Iron BCC density ~ 7.87 g/cm^3 (2 atoms, MW=55.845, Z=2)."""
        density = bcc_crystal.density(molecular_weight=55.845, z=2)
        np.testing.assert_allclose(density, 7.87, atol=0.1)


# ---------------------------------------------------------------------------
# CrystalStructure — coordinate transformations
# ---------------------------------------------------------------------------

class TestCoordinateTransformations:
    def test_fractional_to_cartesian_cubic_origin(self, simple_cubic_crystal):
        cart = simple_cubic_crystal.fractional_to_cartesian(np.array([0.0, 0.0, 0.0]))
        np.testing.assert_allclose(cart, [[0.0, 0.0, 0.0]], atol=1e-12)

    def test_fractional_to_cartesian_cubic_corner(self, simple_cubic_crystal):
        cart = simple_cubic_crystal.fractional_to_cartesian(np.array([1.0, 0.0, 0.0]))
        # For cubic a=3: x_cart = a * frac_x = 3.0
        np.testing.assert_allclose(cart[0, 0], 3.0, atol=1e-12)

    def test_roundtrip_cubic(self, simple_cubic_crystal):
        frac = np.array([0.3, 0.7, 0.1])
        cart = simple_cubic_crystal.fractional_to_cartesian(frac)
        frac_back = simple_cubic_crystal.cartesian_to_fractional(cart)
        np.testing.assert_allclose(frac_back, frac.reshape(1, 3), atol=1e-10)

    def test_roundtrip_hexagonal(self):
        lattice = LatticeParameters(a=3.0, b=3.0, c=5.0,
                                     alpha=90, beta=90, gamma=120)
        atoms = [AtomicPosition('Zn', 0.0, 0.0, 0.0)]
        crystal = CrystalStructure(lattice, atoms)
        frac = np.array([0.5, 0.25, 0.75])
        cart = crystal.fractional_to_cartesian(frac)
        frac_back = crystal.cartesian_to_fractional(cart)
        np.testing.assert_allclose(frac_back, frac.reshape(1, 3), atol=1e-10)

    def test_batch_transform(self, simple_cubic_crystal):
        frac = np.array([[0.0, 0.0, 0.0],
                          [0.5, 0.5, 0.5],
                          [1.0, 1.0, 1.0]])
        cart = simple_cubic_crystal.fractional_to_cartesian(frac)
        assert cart.shape == (3, 3)
        np.testing.assert_allclose(cart[2], [3.0, 3.0, 3.0], atol=1e-10)


# ---------------------------------------------------------------------------
# CrystalStructure — metric tensor and matrices
# ---------------------------------------------------------------------------

class TestMatrices:
    def test_metric_tensor_cubic(self, simple_cubic_crystal):
        """Metric tensor for cubic should be a^2 * I."""
        g = simple_cubic_crystal.metric_tensor
        np.testing.assert_allclose(g, 9.0 * np.eye(3), atol=1e-10)

    def test_direct_matrix_cubic(self, simple_cubic_crystal):
        """Direct matrix for cubic should be a * I."""
        M = simple_cubic_crystal.direct_matrix
        np.testing.assert_allclose(M, 3.0 * np.eye(3), atol=1e-10)

    def test_reciprocal_direct_relationship(self, si_diamond):
        """Reciprocal and direct matrices satisfy: recip^T @ direct = 2*pi*I."""
        M = si_diamond.direct_matrix
        R = si_diamond.reciprocal_matrix
        product = R.T @ M
        np.testing.assert_allclose(product, 2 * np.pi * np.eye(3), atol=1e-8)


# ---------------------------------------------------------------------------
# CrystalStructure — interatomic distance
# ---------------------------------------------------------------------------

class TestInteratomicDistance:
    def test_bcc_nearest_neighbour(self, bcc_crystal):
        """BCC nearest-neighbour distance = a*sqrt(3)/2."""
        d = bcc_crystal.interatomic_distance(0, 1)
        expected = 2.87 * np.sqrt(3) / 2
        np.testing.assert_allclose(d, expected, rtol=1e-6)

    def test_self_distance_zero(self, simple_cubic_crystal):
        d = simple_cubic_crystal.interatomic_distance(0, 0)
        np.testing.assert_allclose(d, 0.0, atol=1e-12)

    def test_out_of_range_raises(self, simple_cubic_crystal):
        with pytest.raises(IndexError):
            simple_cubic_crystal.interatomic_distance(0, 99)


# ---------------------------------------------------------------------------
# CrystalStructure — d-spacing
# ---------------------------------------------------------------------------

class TestDSpacing:
    def test_cubic_100(self, simple_cubic_crystal):
        """d(100) = a for cubic."""
        d = simple_cubic_crystal.d_spacing(1, 0, 0)
        np.testing.assert_allclose(d, 3.0, rtol=1e-10)

    def test_cubic_110(self, simple_cubic_crystal):
        """d(110) = a / sqrt(2) for cubic."""
        d = simple_cubic_crystal.d_spacing(1, 1, 0)
        np.testing.assert_allclose(d, 3.0 / np.sqrt(2), rtol=1e-10)

    def test_cubic_111(self, simple_cubic_crystal):
        """d(111) = a / sqrt(3) for cubic."""
        d = simple_cubic_crystal.d_spacing(1, 1, 1)
        np.testing.assert_allclose(d, 3.0 / np.sqrt(3), rtol=1e-10)

    def test_silicon_111(self, si_diamond):
        """d(111) for Si ~ 3.135 A."""
        d = si_diamond.d_spacing(1, 1, 1)
        expected = 5.431 / np.sqrt(3)
        np.testing.assert_allclose(d, expected, rtol=1e-6)


# ---------------------------------------------------------------------------
# CrystalStructure — Bragg angle
# ---------------------------------------------------------------------------

class TestBraggAngle:
    def test_cubic_100_cu_kalpha(self, simple_cubic_crystal):
        """Bragg angle for (100) with Cu K-alpha (1.5406 A), a=3.0."""
        theta = simple_cubic_crystal.bragg_angle(1, 0, 0, wavelength=1.5406)
        # sin(theta) = lambda / (2d) = 1.5406 / (2*3.0)
        expected = np.degrees(np.arcsin(1.5406 / 6.0))
        np.testing.assert_allclose(theta, expected, rtol=1e-6)

    def test_impossible_reflection_raises(self, simple_cubic_crystal):
        """If lambda > 2d, no Bragg reflection is possible."""
        with pytest.raises(ValueError, match="No diffraction"):
            simple_cubic_crystal.bragg_angle(5, 5, 5, wavelength=10.0)


# ---------------------------------------------------------------------------
# CrystalStructure — systematic absences
# ---------------------------------------------------------------------------

class TestSystematicAbsences:
    def test_fcc_absence_odd_indices(self, si_diamond):
        """FCC: reflections with mixed even/odd h,k,l are forbidden."""
        forbidden = si_diamond.systematic_absences('Fm3m')
        # (1,0,0) should be forbidden (h+k=1 is odd)
        assert (1, 0, 0) in forbidden

    def test_fcc_allowed_all_even(self, si_diamond):
        """FCC: (2,0,0) has h+k=2, h+l=2, k+l=0 all even -> allowed."""
        forbidden = si_diamond.systematic_absences('Fm3m')
        assert (2, 0, 0) not in forbidden

    def test_bcc_absence_odd_sum(self, bcc_crystal):
        """BCC (I): h+k+l odd are forbidden."""
        forbidden = bcc_crystal.systematic_absences('Im3m')
        assert (1, 0, 0) in forbidden  # sum=1, odd
        assert (1, 1, 0) not in forbidden  # sum=2, even


# ---------------------------------------------------------------------------
# CrystalStructure — multiplicity
# ---------------------------------------------------------------------------

class TestMultiplicity:
    def test_111_multiplicity(self, simple_cubic_crystal):
        m = simple_cubic_crystal._calculate_multiplicity(1, 1, 1)
        assert m == 8

    def test_110_multiplicity(self, simple_cubic_crystal):
        m = simple_cubic_crystal._calculate_multiplicity(1, 1, 0)
        assert m == 12

    def test_123_multiplicity(self, simple_cubic_crystal):
        m = simple_cubic_crystal._calculate_multiplicity(1, 2, 3)
        assert m == 24


# ---------------------------------------------------------------------------
# CrystalStructure — supercell
# ---------------------------------------------------------------------------

class TestSupercell:
    def test_supercell_atom_count(self, simple_cubic_crystal):
        sc = simple_cubic_crystal.supercell(2, 2, 2)
        assert len(sc.atoms) == 1 * 8  # 1 atom * 2^3

    def test_supercell_lattice_parameters(self, simple_cubic_crystal):
        sc = simple_cubic_crystal.supercell(2, 3, 1)
        np.testing.assert_allclose(sc.lattice.a, 6.0)
        np.testing.assert_allclose(sc.lattice.b, 9.0)
        np.testing.assert_allclose(sc.lattice.c, 3.0)

    def test_supercell_volume(self, simple_cubic_crystal):
        sc = simple_cubic_crystal.supercell(2, 2, 2)
        expected = simple_cubic_crystal.unit_cell_volume() * 8
        np.testing.assert_allclose(sc.unit_cell_volume(), expected, rtol=1e-10)

    def test_supercell_preserves_angles(self):
        lattice = LatticeParameters(a=3.0, b=3.0, c=5.0,
                                     alpha=90, beta=90, gamma=120)
        atoms = [AtomicPosition('Zn', 0.0, 0.0, 0.0)]
        crystal = CrystalStructure(lattice, atoms)
        sc = crystal.supercell(2, 2, 3)
        assert sc.lattice.alpha == 90
        assert sc.lattice.gamma == 120

    def test_supercell_bcc(self, bcc_crystal):
        sc = bcc_crystal.supercell(2, 2, 2)
        assert len(sc.atoms) == 2 * 8


# ---------------------------------------------------------------------------
# CrystalStructure — coordinate arrays
# ---------------------------------------------------------------------------

class TestCoordinateArrays:
    def test_get_fractional_coordinates_shape(self, si_diamond):
        coords = si_diamond.get_fractional_coordinates()
        assert coords.shape == (8, 3)

    def test_get_cartesian_coordinates_shape(self, si_diamond):
        coords = si_diamond.get_cartesian_coordinates()
        assert coords.shape == (8, 3)

    def test_fractional_values(self, bcc_crystal):
        coords = bcc_crystal.get_fractional_coordinates()
        np.testing.assert_allclose(coords[0], [0.0, 0.0, 0.0])
        np.testing.assert_allclose(coords[1], [0.5, 0.5, 0.5])
