# SciComp

Status:      experimental research library
Category:    lab
Owner:       alawein
Visibility:  public
Purpose:     Scientific computing utilities and shared numerical tooling.
Next action: maintain verified Python core

## Abstract

SciComp is a research-library repository containing numerical work across
`Python/` (the canonical import boundary), `MATLAB/`, and `Mathematica/`.
The verified support promise is intentionally limited to the Python core
exercised in CI. The remaining language trees, hardware-dependent features,
optional integrations, and untested domain modules are retained as
**experimental research surfaces**; they are not a claim of equivalent
cross-language verification.

## Status

- Lifecycle: experimental research library
- Verified scope: Python core test suite on Python 3.10–3.12
- Experimental scope: optional Python features, MATLAB, Mathematica, GPU, and
  untested domain modules
- Details: [support matrix](docs/SUPPORT_MATRIX.md)

## Runtime requirements

- Python 3.10+ with `pip install -e ".[dev]"`
- Optional: MATLAB R2024b+ for `MATLAB/` surfaces and batch tests
- Optional: Wolfram Mathematica for `Mathematica/` notebooks
- Optional: CUDA-capable GPU for accelerator modules (CPU fallback documented in `docs/GPU_TESTING_GUIDE.md`)

## Reproducibility

```bash
python -m pip install -e ".[dev]"
python -m pytest
```

The default test command collects the root regression tests and Python test
tree. Coverage is reported in CI for visibility; it is not used as a release
threshold because experimental modules materially exceed the verified core.
Install an optional feature only when needed, for example
`pip install -e ".[viz]"`, `.[quantum]`, or `.[ml]`. See the
[support matrix](docs/SUPPORT_MATRIX.md) for per-example prerequisites.

CLI entry points: `scicomp` and `bsc` (both resolve to
`Python.utils.cli:main`).

`tests/matlab/test_heat_transfer.m` requires MATLAB and
`tests/mathematica/test_symbolic_quantum.nb` requires Mathematica. They are
not run by Python CI and remain experimental.

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
