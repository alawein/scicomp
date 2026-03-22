---
type: guide
authority: canonical
audience: [ai-agents, contributors]
last-verified: 2026-03-03
---

<!-- CUSTOM OVERRIDE: domain-specific guide | Intentional specialization for cross-platform scientific computing framework (Python, MATLAB, Mathematica parity required) -->

# CLAUDE.md — scicomp

## Repository Context

**Name:** SciComp  
**Type:** research-framework  
**Purpose:** Cross-platform scientific computing framework for quantum mechanics, thermal transport, and physics-informed machine learning. Provides equivalent implementations across Python, MATLAB, and Mathematica for both research and education, with GPU acceleration via CuPy/CUDA.

## Tech Stack

- **Language:** Python 3.8+, MATLAB, Mathematica
- **Core deps:** NumPy, SciPy, Matplotlib, SymPy, h5py
- **Optional:** CuPy (GPU), TensorFlow, PyTorch, scikit-learn
- **Build:** setuptools (`pyproject.toml` + legacy `setup.py`)
- **Testing:** pytest, pytest-cov, pytest-benchmark
- **Linting:** ruff, mypy

## Key Files

- `README.md` — Main documentation
- `pyproject.toml` — Package configuration
- `scicomp/` — Python core package
- `matlab/` — MATLAB implementations
- `mathematica/` — Mathematica notebooks
- `examples/` — Demo scripts (beginner, GPU, ML physics)
- `tests/` — Test suite (Python, MATLAB, Mathematica)
- `scripts/` — Validation and deployment scripts
- `CITATION.cff` — Academic citation metadata

## Development Guidelines

1. Maintain cross-platform parity — new Python features should have MATLAB/Mathematica equivalents where feasible
2. GPU code must include automatic CPU fallback
3. Add tests for new features (`pytest`)
4. Use `ruff` for linting and `mypy` for type checking
5. Use conventional commits
6. Update `CITATION.cff` for releases

## Common Tasks

### Running Tests
```bash
pytest
pytest --cov=scicomp
# Cross-platform
python scripts/validate_framework.py
matlab -batch "run('tests/matlab/test_heat_transfer.m')"
```

### Building
```bash
pip install -e ".[dev]"
```

## Architecture

Modular scientific computing library with three parallel implementations (Python, MATLAB, Mathematica). Python core provides quantum mechanics (Bell states, VQE, QAOA, Jaynes-Cummings), GPU-accelerated numerics with CuPy/CUDA automatic fallback, physics-informed neural networks for PDEs, and thermal transport solvers. Cross-platform validation suite ensures numerical consistency across all three languages.

## Governance
See [AGENTS.md](AGENTS.md) for rules. See [SSOT.md](SSOT.md) for current state.
