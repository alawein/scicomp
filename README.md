# SciComp

Status:      frozen
Category:    research
Owner:       alawein
Visibility:  public
Purpose:     Scientific computing utilities and shared numerical tooling.
Next action: continue

## Abstract

SciComp is a cross-platform scientific computing suite that keeps Python,
MATLAB, and Mathematica in one repo on purpose. The value is a shared scientific
vocabulary across those implementations, with explicit notes on where GPU,
symbolic, and teaching workflows diverge. `Python/` is the canonical Python
import boundary by design.

## Status

- Lifecycle: frozen
- Verification date: 2026-06-29
- Scope: multi-language numerical modules, examples, and cross-surface tests

## Runtime requirements

- Python 3.10+ with `pip install -e ".[dev]"`
- Optional: MATLAB R2024b+ for `MATLAB/` surfaces and batch tests
- Optional: Wolfram Mathematica for `Mathematica/` notebooks
- Optional: CUDA-capable GPU for accelerator modules (CPU fallback documented in `docs/GPU_TESTING_GUIDE.md`)

## Reproducibility

```bash
git clone https://github.com/alawein/scicomp.git
cd scicomp
pip install -e ".[dev]"
python scripts/validate_framework.py
pytest
```

CLI entry points: `berkeley-scicomp` or `bsc`. For MATLAB parity checks:

```bash
matlab -batch "run('tests/matlab/test_heat_transfer.m')"
```

## Datasets

- No large vendored datasets; examples use generated or inline numerical inputs
- `performance_baselines.json` records timing baselines for regression checks
- Keep machine-local paths, GPU environment assumptions, and unpublished teaching
  data out of public examples

## Docs map

- [docs/README.md](docs/README.md)
- [SSOT.md](SSOT.md)
- [LESSONS.md](LESSONS.md)
