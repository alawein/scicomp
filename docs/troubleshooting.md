---
type: canonical
owner: platform-engineering
last-reviewed: 2026-03-31
---

# Troubleshooting -- scicomp

## Common Issues

**Import fails after install**

If `import Python.Quantum` raises `ModuleNotFoundError`, the package was likely installed without
the editable flag. Install with:

```bash
pip install -e ".[dev]"
```

Verify that `Python/` is on the Python path and that the egg-info directory is present in the
repo root.

**CuPy not found / GPU path raises ImportError**

The base install does not include CuPy. Install the GPU extra matching your CUDA version:

```bash
pip install cupy-cuda12x  # CUDA 12
pip install cupy-cuda11x  # CUDA 11
```

If no GPU is available, all GPU-accelerated modules fall back to CPU (NumPy/SciPy) automatically.
No action is needed unless you explicitly require GPU performance.

**`nvidia-smi` reports a device but CuPy still raises `CUDADriverError`**

CUDA Toolkit version and CuPy build version must match. Run:

```bash
nvcc --version
python -c "import cupy; print(cupy.__version__)"
```

Reinstall CuPy selecting the correct `cupy-cuda<version>` variant.

**pytest collection errors**

The test suite is configured in `pyproject.toml` with `testpaths = ["tests"]`. If pytest is run
from outside the repo root, it may not locate the test paths. Always run `pytest` from the repo
root after `pip install -e ".[dev]"`.

**MATLAB tests not found**

MATLAB surface tests require a licensed MATLAB installation and must be run with:

```bash
matlab -batch "run('tests/matlab/test_heat_transfer.m')"
```

There is no automatic MATLAB test runner from the Python test suite.

## Diagnostic Steps

1. Confirm the install is editable: `pip show scicomp` should list the repo directory
   as the location.
2. Run the validation script: `python scripts/validate_framework.py`.
3. Run the test suite with verbose output: `pytest -v`.
4. For GPU issues, follow the full verification sequence in
   [GPU_TESTING_GUIDE.md](GPU_TESTING_GUIDE.md).

## Known Failure Modes

- CuPy version mismatch with the installed CUDA Toolkit (see above).
- Running pytest outside the repo root causes test collection to fail.
- `berkeley_scicomp.egg-info/` present in the repo root is expected; it is produced by the
  editable install and is gitignored.

## FAQ

**Does scicomp require a GPU?**
No. GPU acceleration is optional. All modules fall back to CPU paths when CuPy is not installed
or no CUDA device is detected.

**Can I use only the Python surface without MATLAB or Mathematica?**
Yes. The Python package is self-contained under `Python/`. MATLAB and Mathematica surfaces are
independent and require their respective licensed runtimes.
