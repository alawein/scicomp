---
type: normative
authority: canonical
audience: [agents, contributors, maintainers]
last-verified: 2026-03-09
---

<!-- CUSTOM OVERRIDE: domain-specific governance | Intentional specialization for cross-platform scientific computing (GPU/CPU fallback, Colab compatibility, multi-language parity rules) -->

# AGENTS — scicomp

> Cross-platform scientific computing framework for quantum mechanics,
> thermal transport, and physics-informed machine learning.

## Repository Scope

Python + MATLAB + Mathematica library providing equivalent implementations
across platforms. Features GPU acceleration via CuPy/CUDA with automatic
CPU fallback, quantum simulations, and physics-informed neural networks.

## Key Directories

| Directory | Purpose |
|-----------|---------|
| `scicomp/` | Core Python package |
| `matlab/` | MATLAB implementations |
| `mathematica/` | Mathematica notebooks |
| `examples/` | Demo scripts (beginner, GPU, ML physics) |
| `tests/` | Test suite (Python, MATLAB, Mathematica) |
| `scripts/` | Validation and deployment scripts |

## Commands

- `pip install -e .` -- install package
- `pytest` -- run Python tests
- `pytest --cov=scicomp` -- run tests with coverage
- `python scripts/validate_framework.py` -- cross-platform validation
- `matlab -batch "run('tests/matlab/test_heat_transfer.m')"` -- MATLAB tests

## Agent Rules

- Read this file before making changes
- Maintain cross-platform parity -- new Python features should have
  MATLAB/Mathematica equivalents where feasible
- GPU code must include automatic CPU fallback
- Add tests for new features (`pytest`)
- Use `ruff` for linting and `mypy` for type checking
- Update `CITATION.cff` for releases
- Do not add dependencies that break Google Colab compatibility
- Use conventional commit messages: `feat(scope):`, `fix(scope):`, etc.

## Naming Conventions

- Python modules: `snake_case.py`
- Classes: `PascalCase`
- Functions: `snake_case`
- Constants: `UPPER_SNAKE_CASE`
- MATLAB files: `camelCase.m`

See [CLAUDE.md](CLAUDE.md) | [SSOT.md](SSOT.md)
