# SciComp

Status:      frozen
Category:    lab
Owner:       alawein
Visibility:  public
Purpose:     Scientific computing utilities and shared numerical tooling.
Next action: continue

## Abstract

SciComp keeps equivalent numerical implementations of the same physics
problems, quantum mechanics, thermal transport, and physics-informed ML,
across three language trees: `Python/` (the canonical import boundary),
`MATLAB/`, and `Mathematica/`. It is for researchers who need to check a
result in whichever of those three languages their institution or
collaborators already use, rather than reimplementing from a
single-language library. It does not require MATLAB, Mathematica, or a
GPU: those are optional per-tree runtimes, with CPU fallback for GPU code
documented in `docs/GPU_TESTING_GUIDE.md`.

## Status

- Lifecycle: frozen
- Verification date: 2026-08-28
- Scope: multi-language numerical modules, examples, and cross-surface tests

## Runtime requirements

- Python 3.10+ with `pip install -e ".[dev]"`
- Optional: MATLAB R2024b+ for `MATLAB/` surfaces and batch tests
- Optional: Wolfram Mathematica for `Mathematica/` notebooks
- Optional: CUDA-capable GPU for accelerator modules (CPU fallback documented in `docs/GPU_TESTING_GUIDE.md`)

## Reproducibility

```bash
python -m pip install -e .
python -m pytest tests/python -q
```

`pip install -e .` and `pytest tests/python -q` exit 0 (378 passed, 80
skipped: quantum and ML-physics tests that need the optional `ml` extra).
The framework check needs the optional `ml` extra: `pip install -e ".[ml]"`
then `python scripts/validate_framework.py` (11 of 13 checks pass without
it).

CLI entry points: `scicomp` and `bsc` (both resolve to
`Python.utils.cli:main`).

`tests/matlab/test_heat_transfer.m` requires MATLAB and
`tests/mathematica/test_symbolic_quantum.nb` requires Mathematica; neither
runtime is available here, so those tests are not run.

## Datasets

- No large vendored datasets; examples use generated or inline numerical inputs
- `performance_baselines.json` records timing baselines for regression checks

## Architecture

```text
scicomp/
├── Python/       # canonical Python import boundary
├── MATLAB/       # parallel MATLAB modules
├── Mathematica/  # parallel Wolfram notebooks
├── examples/     # cross-language usage
├── tests/        # Python and MATLAB regression
└── docs/         # installation, API, theory
```

Detail: [docs/architecture/topology.md](docs/architecture/topology.md) and [docs/architecture.md](docs/architecture.md).

## Docs map

- [docs/README.md](docs/README.md)
- [SSOT.md](SSOT.md)
- [LESSONS.md](LESSONS.md)
