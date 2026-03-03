"""
Tests for FEM Global Assembly Procedures
Tests for DOF mapping, stiffness/mass assembly, boundary conditions,
load application, and static solve from Python.FEM.core.assembly.

Because assembly.py depends heavily on Mesh, MaterialProperty, and the
element factory, we construct lightweight real objects (Mesh, Node, Element,
MaterialProperty) rather than deeply mocking internals.  This validates the
assembly logic end-to-end for a simple 1-D two-bar truss problem where
analytical solutions are available.
"""
import numpy as np
import pytest

from Python.FEM.core.finite_elements import Node, Element
from Python.FEM.core.mesh_generation import Mesh
from Python.FEM.utils.material_properties import MaterialProperty


# ---------------------------------------------------------------------------
# Helpers — build a minimal 1-D bar mesh by hand
# ---------------------------------------------------------------------------

def _build_two_bar_mesh(L1=1.0, L2=1.0):
    """Create a 1-D mesh with two bar elements in series.

    Node layout:  0 ---[elem 0]--- 1 ---[elem 1]--- 2

    Parameters
    ----------
    L1, L2 : float
        Lengths of the two bars.

    Returns
    -------
    mesh : Mesh
    """
    mesh = Mesh()
    mesh.dimension = 1
    mesh.nodes = {
        0: Node(id=0, coordinates=np.array([0.0])),
        1: Node(id=1, coordinates=np.array([L1])),
        2: Node(id=2, coordinates=np.array([L1 + L2])),
    }
    mesh.elements = {
        0: Element(id=0, element_type='bar1d', node_ids=[0, 1],
                   material_id=1, properties={'cross_section_area': 1.0}),
        1: Element(id=1, element_type='bar1d', node_ids=[1, 2],
                   material_id=1, properties={'cross_section_area': 1.0}),
    }
    return mesh


def _steel_material():
    """Return a simple steel-like material."""
    return MaterialProperty(
        name='Steel',
        youngs_modulus=200e9,   # Pa
        poissons_ratio=0.3,
        density=7800.0,         # kg/m^3
    )


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def two_bar_assembly():
    """Assemble a two-bar 1-D problem and return the GlobalAssembly object.

    We import inside the fixture to keep the heavy import late.
    """
    from Python.FEM.core.assembly import GlobalAssembly

    mesh = _build_two_bar_mesh(L1=1.0, L2=1.0)
    materials = {1: _steel_material()}
    assembly = GlobalAssembly(mesh, materials)
    return assembly


@pytest.fixture
def single_bar_assembly():
    """Single bar element: node 0 -- node 1, length = 2.0."""
    from Python.FEM.core.assembly import GlobalAssembly

    mesh = Mesh()
    mesh.dimension = 1
    mesh.nodes = {
        0: Node(id=0, coordinates=np.array([0.0])),
        1: Node(id=1, coordinates=np.array([2.0])),
    }
    mesh.elements = {
        0: Element(id=0, element_type='bar1d', node_ids=[0, 1],
                   material_id=1, properties={'cross_section_area': 0.5}),
    }
    materials = {1: _steel_material()}
    return GlobalAssembly(mesh, materials)


# ---------------------------------------------------------------------------
# DOF mapping
# ---------------------------------------------------------------------------

class TestDOFMapping:
    def test_num_dofs_two_bar(self, two_bar_assembly):
        """3 nodes x 1 DOF/node = 3 DOFs."""
        assert two_bar_assembly.num_dofs == 3

    def test_num_dofs_single_bar(self, single_bar_assembly):
        assert single_bar_assembly.num_dofs == 2

    def test_dof_map_entries(self, two_bar_assembly):
        assert two_bar_assembly.dof_map[0] == [0]
        assert two_bar_assembly.dof_map[1] == [1]
        assert two_bar_assembly.dof_map[2] == [2]

    def test_global_dof_reverse_map(self, two_bar_assembly):
        assert two_bar_assembly.global_dof_to_node[0] == (0, 0)
        assert two_bar_assembly.global_dof_to_node[2] == (2, 0)


# ---------------------------------------------------------------------------
# Global stiffness assembly
# ---------------------------------------------------------------------------

class TestGlobalStiffnessAssembly:
    def test_shape(self, two_bar_assembly):
        K = two_bar_assembly.assemble_global_stiffness()
        assert K.shape == (3, 3)

    def test_symmetry(self, two_bar_assembly):
        K = two_bar_assembly.assemble_global_stiffness()
        K_dense = K.toarray()
        np.testing.assert_allclose(K_dense, K_dense.T, atol=1e-10)

    def test_analytical_two_bar(self, two_bar_assembly):
        """For two identical bars (E, A, L), the assembled stiffness is:

        K = EA/L * [[ 1, -1,  0],
                    [-1,  2, -1],
                    [ 0, -1,  1]]
        """
        K = two_bar_assembly.assemble_global_stiffness().toarray()
        mat = _steel_material()
        EA_over_L = mat.youngs_modulus * 1.0 / 1.0  # A=1, L=1
        expected = EA_over_L * np.array([
            [1.0, -1.0, 0.0],
            [-1.0, 2.0, -1.0],
            [0.0, -1.0, 1.0],
        ])
        np.testing.assert_allclose(K, expected, rtol=1e-10)

    def test_singular_without_bc(self, two_bar_assembly):
        """Global stiffness without BCs should be singular (rigid body mode)."""
        K = two_bar_assembly.assemble_global_stiffness().toarray()
        eigvals = np.linalg.eigvalsh(K)
        # At least one eigenvalue much smaller than the largest (rigid body mode).
        # Ratio test avoids sensitivity to absolute scale of stiffness values.
        ratio = np.min(np.abs(eigvals)) / np.max(np.abs(eigvals))
        assert ratio < 1e-10, f"Smallest/largest eigenvalue ratio {ratio} too large"

    def test_single_bar_stiffness(self, single_bar_assembly):
        K = single_bar_assembly.assemble_global_stiffness().toarray()
        mat = _steel_material()
        EA_over_L = mat.youngs_modulus * 0.5 / 2.0  # A=0.5, L=2.0
        expected = EA_over_L * np.array([[1, -1], [-1, 1]])
        np.testing.assert_allclose(K, expected, rtol=1e-10)


# ---------------------------------------------------------------------------
# Global mass assembly
# ---------------------------------------------------------------------------

class TestGlobalMassAssembly:
    def test_shape(self, two_bar_assembly):
        M = two_bar_assembly.assemble_global_mass()
        assert M.shape == (3, 3)

    def test_symmetry(self, two_bar_assembly):
        M = two_bar_assembly.assemble_global_mass()
        M_dense = M.toarray()
        np.testing.assert_allclose(M_dense, M_dense.T, atol=1e-10)

    def test_positive_diagonal(self, two_bar_assembly):
        M = two_bar_assembly.assemble_global_mass()
        diag = M.toarray().diagonal()
        assert np.all(diag > 0)

    def test_total_mass_conservation(self, two_bar_assembly):
        """Sum of consistent mass matrix = total mass = rho*A*L_total."""
        M = two_bar_assembly.assemble_global_mass().toarray()
        total_mass_matrix = np.sum(M)
        mat = _steel_material()
        expected_mass = mat.density * 1.0 * 2.0  # rho * A * L_total
        np.testing.assert_allclose(total_mass_matrix, expected_mass, rtol=1e-10)


# ---------------------------------------------------------------------------
# Boundary conditions
# ---------------------------------------------------------------------------

class TestBoundaryConditions:
    def test_apply_displacement_bc(self, two_bar_assembly):
        two_bar_assembly.apply_boundary_conditions({(0, 0): 0.0})
        assert 0 in two_bar_assembly.prescribed_dofs
        assert two_bar_assembly.prescribed_values[0] == 0.0

    def test_multiple_bcs(self, two_bar_assembly):
        two_bar_assembly.apply_boundary_conditions({
            (0, 0): 0.0,
            (2, 0): 0.001,
        })
        assert len(two_bar_assembly.prescribed_dofs) == 2


# ---------------------------------------------------------------------------
# Point loads
# ---------------------------------------------------------------------------

class TestPointLoads:
    def test_single_load(self, two_bar_assembly):
        f = two_bar_assembly.apply_point_loads({(2, 0): 1000.0})
        assert f.shape == (3,)
        np.testing.assert_allclose(f[2], 1000.0)
        np.testing.assert_allclose(f[0], 0.0)

    def test_multiple_loads(self, two_bar_assembly):
        f = two_bar_assembly.apply_point_loads({
            (1, 0): 500.0,
            (2, 0): 1000.0,
        })
        np.testing.assert_allclose(f[1], 500.0)
        np.testing.assert_allclose(f[2], 1000.0)


# ---------------------------------------------------------------------------
# Static solve
# ---------------------------------------------------------------------------

class TestSolveStatic:
    def test_cantilever_bar(self, two_bar_assembly):
        """Two bars in series, fixed at node 0, force F at node 2.

        Analytical solution:
          u(node 1) = F*L / (EA)
          u(node 2) = F*(L+L) / (EA) = 2*F*L / (EA)
        since both bars have same E, A, L.
        """
        asm = two_bar_assembly
        asm.assemble_global_stiffness()
        asm.apply_boundary_conditions({(0, 0): 0.0})
        F = 1e6  # 1 MN
        asm.apply_point_loads({(2, 0): F})
        u = asm.solve_static()

        mat = _steel_material()
        EA = mat.youngs_modulus * 1.0
        L = 1.0
        np.testing.assert_allclose(u[0], 0.0, atol=1e-10)
        np.testing.assert_allclose(u[1], F * L / EA, rtol=1e-6)
        np.testing.assert_allclose(u[2], 2 * F * L / EA, rtol=1e-6)

    def test_prescribed_displacement(self, two_bar_assembly):
        """Fix both ends: u(0)=0, u(2)=delta. Internal node displacement
        should be delta/2 by symmetry (equal bars)."""
        asm = two_bar_assembly
        asm.assemble_global_stiffness()
        delta = 0.001
        asm.apply_boundary_conditions({(0, 0): 0.0, (2, 0): delta})
        asm.apply_point_loads({})  # no external loads
        u = asm.solve_static()

        np.testing.assert_allclose(u[0], 0.0, atol=1e-10)
        np.testing.assert_allclose(u[1], delta / 2, rtol=1e-4)
        np.testing.assert_allclose(u[2], delta, rtol=1e-4)

    def test_no_stiffness_raises(self, two_bar_assembly):
        asm = two_bar_assembly
        asm.apply_point_loads({(2, 0): 100.0})
        with pytest.raises(ValueError, match="stiffness"):
            asm.solve_static()

    def test_no_load_raises(self, two_bar_assembly):
        asm = two_bar_assembly
        asm.assemble_global_stiffness()
        asm.apply_boundary_conditions({(0, 0): 0.0})
        with pytest.raises(ValueError, match="Load vector"):
            asm.solve_static()


# ---------------------------------------------------------------------------
# Element stresses
# ---------------------------------------------------------------------------

class TestElementStresses:
    def test_uniform_stress(self, two_bar_assembly):
        """With fixed-free BCs and axial load, both bars should have
        the same uniform stress = F/A."""
        asm = two_bar_assembly
        asm.assemble_global_stiffness()
        asm.apply_boundary_conditions({(0, 0): 0.0})
        F = 1e6
        asm.apply_point_loads({(2, 0): F})
        u = asm.solve_static()
        stresses = asm.compute_element_stresses(u)
        expected_stress = F / 1.0  # A = 1.0
        for elem_id, stress in stresses.items():
            np.testing.assert_allclose(stress[0], expected_stress, rtol=1e-4)


# ---------------------------------------------------------------------------
# Reaction forces
# ---------------------------------------------------------------------------

class TestReactionForces:
    def test_reaction_equals_applied_force(self, two_bar_assembly):
        """Equilibrium: reaction at fixed end should equal -F."""
        asm = two_bar_assembly
        asm.assemble_global_stiffness()
        asm.apply_boundary_conditions({(0, 0): 0.0})
        F = 1e6
        asm.apply_point_loads({(2, 0): F})
        u = asm.solve_static()
        reactions = asm.compute_reaction_forces(u)
        # Node 0 is constrained
        assert 0 in reactions
        np.testing.assert_allclose(reactions[0][0], -F, rtol=1e-4)


# ---------------------------------------------------------------------------
# Node displacement extraction
# ---------------------------------------------------------------------------

class TestGetDisplacementAtNode:
    def test_known_displacement(self, two_bar_assembly):
        asm = two_bar_assembly
        asm.assemble_global_stiffness()
        asm.apply_boundary_conditions({(0, 0): 0.0})
        F = 1e6
        asm.apply_point_loads({(2, 0): F})
        u = asm.solve_static()
        u_node2 = asm.get_displacement_at_node(u, 2)
        mat = _steel_material()
        expected = 2 * F * 1.0 / (mat.youngs_modulus * 1.0)
        np.testing.assert_allclose(u_node2[0], expected, rtol=1e-6)

    def test_invalid_node_raises(self, two_bar_assembly):
        u = np.zeros(3)
        with pytest.raises(ValueError, match="not found"):
            two_bar_assembly.get_displacement_at_node(u, 99)


# ---------------------------------------------------------------------------
# System energy
# ---------------------------------------------------------------------------

class TestSystemEnergy:
    def test_strain_energy(self, two_bar_assembly):
        """Strain energy U = 0.5 * F * delta for a linear elastic bar."""
        asm = two_bar_assembly
        asm.assemble_global_stiffness()
        asm.assemble_global_mass()
        asm.apply_boundary_conditions({(0, 0): 0.0})
        F = 1e6
        asm.apply_point_loads({(2, 0): F})
        u = asm.solve_static()
        energy = asm.compute_system_energy(u)
        # U = 0.5 * F * u_tip
        expected_U = 0.5 * F * u[2]
        np.testing.assert_allclose(energy['strain_energy'], expected_U, rtol=1e-4)

    def test_energy_keys(self, two_bar_assembly):
        asm = two_bar_assembly
        asm.assemble_global_stiffness()
        asm.assemble_global_mass()
        asm.apply_boundary_conditions({(0, 0): 0.0})
        asm.apply_point_loads({(2, 0): 1e3})
        u = asm.solve_static()
        energy = asm.compute_system_energy(u)
        assert set(energy.keys()) == {'strain_energy', 'potential_energy', 'total_potential'}
