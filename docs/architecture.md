---
type: canonical
owner: platform-engineering
last-reviewed: 2026-03-31
---

# Architecture Overview -- scicomp

SciComp is a cross-platform scientific computing suite that keeps Python, MATLAB, and Mathematica
in the same repository. The three language surfaces share a common numerical vocabulary and cover
overlapping topic areas so that implementations can be compared and verified across languages.

## Components

The repository is organized into four primary surfaces:

- **`Python/`** -- canonical Python package and CLI entry point (`scicomp` / `bsc`).
  Sub-directories mirror the domain structure (Quantum, Thermal_Transport, Machine_Learning,
  Spintronics, Optics, etc.). GPU acceleration is provided by CuPy and degrades cleanly to
  NumPy/SciPy when a CUDA device is unavailable.
- **`MATLAB/`** -- MATLAB implementations of the same domain modules. Uses MATLAB package
  namespaces (`+namespace` directories) where applicable.
- **`Mathematica/`** -- Mathematica notebooks covering symbolic and analytical workflows for the
  same domains.
- **`examples/`** and **`tests/`** -- runnable demonstrations and cross-surface verification.

## Data Flow

Each surface is self-contained: a computation begins with an input (parameters or data), is
processed by the domain module in the chosen language, and produces numerical or symbolic output.
There is no shared runtime state between Python, MATLAB, and Mathematica; parity is verified by
comparing outputs for the same inputs across surfaces in the test suite.

## Dependencies

Core Python dependencies (from `pyproject.toml`): NumPy, SciPy, Matplotlib, SymPy, h5py.
Optional extras:

- `[gpu]` -- CuPy (CUDA 12) for GPU-accelerated paths
- `[ml]` -- TensorFlow, PyTorch, scikit-learn
- `[performance]` -- Numba, Dask, joblib
- `[visualization]` -- Seaborn, Plotly, ipywidgets

MATLAB and Mathematica surfaces have no Python dependency. MATLAB requires a licensed MATLAB
installation; Mathematica requires a licensed Mathematica installation.

## Constraints

- `Python/` is the canonical Python import boundary; do not move modules to `src/` or a
  lowercase layout without a deliberate migration.
- GPU paths must fall back to CPU without raising an unhandled error.
- Numerical changes require tolerance-aware tests (`pytest`) and explicit rationale.
- Cross-platform parity is part of the repo contract; equivalent MATLAB and Mathematica
  implementations should exist for each Python domain module where feasible.
