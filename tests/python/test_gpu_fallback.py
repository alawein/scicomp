"""
Tests for GPU acceleration module with CPU fallback paths.

When CuPy is not available, all operations must fall back to NumPy/SciPy
transparently.  These tests mock out CuPy to ensure the fallback logic works.

Covers: Python.gpu_acceleration.cuda_kernels
"""
import pytest
import numpy as np
import numpy.testing as npt
import sys
import types
import importlib


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _reimport_cuda_kernels():
    """
    Force-reimport of cuda_kernels so that the module-level CuPy detection
    re-runs with the current sys.modules state.
    """
    mod_name = 'Python.gpu_acceleration.cuda_kernels'
    if mod_name in sys.modules:
        del sys.modules[mod_name]
    return importlib.import_module(mod_name)


# ---------------------------------------------------------------------------
# GPU availability flag
# ---------------------------------------------------------------------------

class TestGPUAvailabilityDetection:
    """Verify that GPU_AVAILABLE is False when CuPy is absent."""

    def test_gpu_available_false_without_cupy(self):
        """When CuPy is missing from sys.modules, GPU_AVAILABLE should be False."""
        # Save original cupy reference
        original_cupy = sys.modules.pop('cupy', None)
        original_cupyx = sys.modules.pop('cupyx', None)
        original_cupyx_scipy = sys.modules.pop('cupyx.scipy', None)
        original_cupyx_scipy_linalg = sys.modules.pop('cupyx.scipy.linalg', None)
        original_cupyx_scipy_fft = sys.modules.pop('cupyx.scipy.fft', None)
        original_cupy_cuda = sys.modules.pop('cupy.cuda', None)
        try:
            # Block CuPy import by inserting None sentinel
            sys.modules['cupy'] = None
            mod = _reimport_cuda_kernels()
            assert mod.GPU_AVAILABLE is False
            assert mod.cp is None
        finally:
            # Restore
            sys.modules.pop('cupy', None)
            if original_cupy is not None:
                sys.modules['cupy'] = original_cupy
            for name, orig in [
                ('cupyx', original_cupyx),
                ('cupyx.scipy', original_cupyx_scipy),
                ('cupyx.scipy.linalg', original_cupyx_scipy_linalg),
                ('cupyx.scipy.fft', original_cupyx_scipy_fft),
                ('cupy.cuda', original_cupy_cuda),
            ]:
                if orig is not None:
                    sys.modules[name] = orig


# ---------------------------------------------------------------------------
# GPUAccelerator
# ---------------------------------------------------------------------------

class TestGPUAccelerator:
    """Tests for GPUAccelerator class on CPU fallback path."""

    @pytest.fixture
    def accelerator(self):
        from Python.gpu_acceleration.cuda_kernels import GPUAccelerator
        return GPUAccelerator()

    def test_to_gpu_returns_numpy_on_cpu(self, accelerator):
        """to_gpu should return the same numpy array when GPU is unavailable."""
        arr = np.array([1.0, 2.0, 3.0])
        result = accelerator.to_gpu(arr)
        assert isinstance(result, np.ndarray)
        npt.assert_array_equal(result, arr)

    def test_to_cpu_passthrough(self, accelerator):
        """to_cpu of a numpy array should return it unchanged."""
        arr = np.array([1.0, 2.0, 3.0])
        result = accelerator.to_cpu(arr)
        npt.assert_array_equal(result, arr)

    def test_synchronize_noop(self, accelerator):
        """synchronize should not raise on CPU path."""
        accelerator.synchronize()  # Should be a no-op

    def test_clear_memory_noop(self, accelerator):
        """clear_memory should not raise on CPU path."""
        accelerator.clear_memory()


# ---------------------------------------------------------------------------
# QuantumGPU (CPU fallback)
# ---------------------------------------------------------------------------

class TestQuantumGPUFallback:
    """Tests for QuantumGPU operations using CPU fallback."""

    @pytest.fixture
    def quantum_gpu(self):
        from Python.gpu_acceleration.cuda_kernels import GPUAccelerator, QuantumGPU
        acc = GPUAccelerator()
        return QuantumGPU(acc)

    def test_tensor_product(self, quantum_gpu):
        """Tensor product should match np.kron."""
        A = np.array([[1, 0], [0, 1]], dtype=complex)
        B = np.array([[0, 1], [1, 0]], dtype=complex)
        result = quantum_gpu.tensor_product_gpu(A, B)
        expected = np.kron(A, B)
        npt.assert_allclose(result, expected, atol=1e-12)

    def test_evolve_state_preserves_norm(self, quantum_gpu):
        """Time evolution should preserve the norm of the state."""
        H = np.array([[1, 0], [0, -1]], dtype=complex)  # Pauli Z
        state = np.array([1, 1], dtype=complex) / np.sqrt(2)
        evolved = quantum_gpu.evolve_state_gpu(state, H, time=1.0, steps=100)
        npt.assert_allclose(np.linalg.norm(evolved), 1.0, atol=1e-6)

    def test_evolve_state_at_zero_time(self, quantum_gpu):
        """Evolution for t=0 should return the original state."""
        H = np.array([[0, 1], [1, 0]], dtype=complex)
        state = np.array([1, 0], dtype=complex)
        evolved = quantum_gpu.evolve_state_gpu(state, H, time=0.0, steps=1)
        npt.assert_allclose(np.abs(evolved), np.abs(state), atol=1e-6)

    def test_quantum_fft(self, quantum_gpu):
        """GPU QFT should match np.fft.fft / sqrt(N)."""
        state = np.array([1, 0, 0, 0], dtype=complex)
        result = quantum_gpu.quantum_fft_gpu(state)
        expected = np.fft.fft(state) / np.sqrt(len(state))
        npt.assert_allclose(result, expected, atol=1e-12)

    def test_entanglement_entropy_product_state(self, quantum_gpu):
        """Entanglement entropy of a product state should be near 0."""
        # |00> in 4-dimensional space (2x2 partition)
        state = np.array([1, 0, 0, 0], dtype=complex)
        entropy = quantum_gpu.entanglement_entropy_gpu(state, partition=2)
        npt.assert_allclose(entropy, 0.0, atol=1e-10)

    def test_entanglement_entropy_bell_state(self, quantum_gpu):
        """Entanglement entropy of a Bell state should be 1 bit."""
        # |Phi+> = (|00> + |11>) / sqrt(2)
        state = np.array([1, 0, 0, 1], dtype=complex) / np.sqrt(2)
        entropy = quantum_gpu.entanglement_entropy_gpu(state, partition=2)
        npt.assert_allclose(entropy, 1.0, atol=1e-6)


# ---------------------------------------------------------------------------
# PhysicsGPU (CPU fallback)
# ---------------------------------------------------------------------------

class TestPhysicsGPUFallback:
    """Tests for PhysicsGPU operations using CPU fallback."""

    @pytest.fixture
    def physics_gpu(self):
        from Python.gpu_acceleration.cuda_kernels import GPUAccelerator, PhysicsGPU
        acc = GPUAccelerator()
        return PhysicsGPU(acc)

    def test_heat_equation_boundary_conditions(self, physics_gpu):
        """Heat equation solver should preserve boundary conditions."""
        n = 50
        initial = np.zeros(n)
        initial[n // 2] = 100.0
        # Dirichlet BCs: T(0) = T(n-1) = 0
        initial[0] = 0.0
        initial[-1] = 0.0
        dx = 1.0 / (n - 1)
        alpha = 0.01
        dt = 0.4 * dx**2 / alpha  # stable
        result = physics_gpu.solve_heat_equation_gpu(initial, alpha, dx, dt, steps=20)
        # Boundaries should remain at initial value
        npt.assert_allclose(result[:, 0], 0.0, atol=1e-10)
        npt.assert_allclose(result[:, -1], 0.0, atol=1e-10)

    def test_heat_equation_diffuses(self, physics_gpu):
        """Temperature peak should decrease over time."""
        n = 50
        initial = np.zeros(n)
        initial[n // 2] = 100.0
        dx = 1.0 / (n - 1)
        alpha = 0.01
        dt = 0.4 * dx**2 / alpha
        result = physics_gpu.solve_heat_equation_gpu(initial, alpha, dx, dt, steps=50)
        assert result[-1, n // 2] < result[0, n // 2]

    def test_heat_equation_result_shape(self, physics_gpu):
        """Result should be (steps+1, n)."""
        n = 30
        initial = np.ones(n) * 50.0
        steps = 10
        result = physics_gpu.solve_heat_equation_gpu(initial, 0.01, 0.1, 0.001, steps)
        assert result.shape == (steps + 1, n)

    def test_wave_equation_boundary_conditions(self, physics_gpu):
        """Wave equation solver should maintain fixed boundary conditions."""
        n = 50
        initial_u = np.sin(np.pi * np.linspace(0, 1, n))
        initial_u[0] = 0
        initial_u[-1] = 0
        initial_v = np.zeros(n)
        dx = 1.0 / (n - 1)
        c = 1.0
        dt = 0.5 * dx / c  # CFL condition
        result = physics_gpu.solve_wave_equation_gpu(initial_u, initial_v, c, dx, dt, steps=20)
        npt.assert_allclose(result[:, 0], 0.0, atol=1e-10)
        npt.assert_allclose(result[:, -1], 0.0, atol=1e-10)

    def test_wave_equation_result_shape(self, physics_gpu):
        n = 30
        initial_u = np.zeros(n)
        initial_v = np.zeros(n)
        steps = 15
        result = physics_gpu.solve_wave_equation_gpu(initial_u, initial_v, 1.0, 0.1, 0.01, steps)
        assert result.shape == (steps + 1, n)

    def test_fft_convolution_delta(self, physics_gpu):
        """Convolution with delta function should return the original signal."""
        signal = np.array([1, 2, 3, 4, 5], dtype=float)
        kernel = np.array([1, 0, 0, 0, 0], dtype=float)  # delta
        result = physics_gpu.fft_convolution_gpu(signal, kernel)
        npt.assert_allclose(result, signal, atol=1e-10)

    def test_fft_convolution_commutativity(self, physics_gpu):
        """Convolution should be commutative (for same-length inputs)."""
        np.random.seed(42)
        a = np.random.randn(64)
        b = np.random.randn(64)
        result_ab = physics_gpu.fft_convolution_gpu(a, b)
        result_ba = physics_gpu.fft_convolution_gpu(b, a)
        npt.assert_allclose(result_ab, result_ba, atol=1e-10)


# ---------------------------------------------------------------------------
# MatrixGPU (CPU fallback)
# ---------------------------------------------------------------------------

class TestMatrixGPUFallback:
    """Tests for MatrixGPU operations using CPU fallback."""

    @pytest.fixture
    def matrix_gpu(self):
        from Python.gpu_acceleration.cuda_kernels import GPUAccelerator, MatrixGPU
        acc = GPUAccelerator()
        return MatrixGPU(acc)

    def test_large_matrix_multiply(self, matrix_gpu):
        """GPU matrix multiply should match numpy."""
        np.random.seed(42)
        A = np.random.randn(32, 32)
        B = np.random.randn(32, 32)
        result = matrix_gpu.large_matrix_multiply_gpu(A, B)
        expected = A @ B
        npt.assert_allclose(result, expected, atol=1e-10)

    def test_eigendecomposition_hermitian(self, matrix_gpu):
        """Eigendecomposition of Hermitian matrix should satisfy A v = lambda v."""
        np.random.seed(42)
        A = np.random.randn(8, 8)
        A = (A + A.T) / 2  # Make symmetric
        eigenvalues, eigenvectors = matrix_gpu.eigendecomposition_gpu(A)
        # Verify A @ v = lambda * v for each eigenpair
        for i in range(len(eigenvalues)):
            lhs = A @ eigenvectors[:, i]
            rhs = eigenvalues[i] * eigenvectors[:, i]
            npt.assert_allclose(lhs, rhs, atol=1e-8)

    def test_svd_reconstruction(self, matrix_gpu):
        """SVD should satisfy A = U @ diag(S) @ Vt."""
        np.random.seed(42)
        A = np.random.randn(8, 8)
        U, S, Vt = matrix_gpu.svd_gpu(A)
        reconstructed = U @ np.diag(S) @ Vt
        npt.assert_allclose(reconstructed, A, atol=1e-10)

    def test_svd_singular_values_nonnegative(self, matrix_gpu):
        """Singular values should be non-negative."""
        np.random.seed(42)
        A = np.random.randn(10, 10)
        _, S, _ = matrix_gpu.svd_gpu(A)
        assert np.all(S >= -1e-15)
