---
type: canonical
authority: canonical
audience: [ai-agents, contributors]
last-verified: 2026-04-09
source: none
sync: none
sla: none
---

# CLAUDE.md — SciComp

## Repository Context

**Name:** SciComp
**Type:** research-library
**Purpose:** Cross-platform scientific computing framework for quantum mechanics, thermal
transport, and physics-informed machine learning. Provides equivalent implementations across
Python, MATLAB, and Mathematica for both research and education, with GPU acceleration via
CuPy/CUDA.

---

## Tech Stack

- **Language:** Python 3.8+
- **Additional languages:** MATLAB, Mathematica
- **Core deps:** NumPy, SciPy, Matplotlib, SymPy, h5py
- **Build:** setuptools (`pyproject.toml` + legacy `setup.py`)
- **Testing:** pytest, pytest-cov, pytest-benchmark
- **Linting:** ruff, mypy

<!-- EXTENSION SLOT: Toolchain
     Add project-specific toolchain details here (HPC tools, simulation
     engines, external solvers, GPU frameworks, etc.)
-->
- **GPU:** CuPy (GPU acceleration with automatic CPU fallback)
- **ML:** TensorFlow, PyTorch, scikit-learn (optional)
- **Citation:** `CITATION.cff` for academic attribution

---

## Commands

### Setup

```bash
pip install -e ".[dev]"
```

### Test

```bash
pytest
pytest --cov=scicomp
# Cross-platform validation
python scripts/validate_framework.py
matlab -batch "run('tests/matlab/test_heat_transfer.m')"
```

### Lint / Format

```bash
ruff check scicomp/
mypy scicomp/
```

<!-- EXTENSION SLOT: Additional Commands
     Add project-specific command sections here (benchmarks, agents,
     SSOT, simulation workflows, HPC job submission, etc.)
-->

---

## Architecture Overview

Modular scientific computing library with three parallel implementations (Python, MATLAB,
Mathematica). Python core provides quantum mechanics (Bell states, VQE, QAOA,
Jaynes-Cummings), GPU-accelerated numerics with CuPy/CUDA automatic fallback,
physics-informed neural networks for PDEs, and thermal transport solvers. Cross-platform
validation suite ensures numerical consistency across all three languages.

---

## Project Structure

```
scicomp/
├── scicomp/               # Core Python package
├── matlab/                # MATLAB implementations
├── mathematica/           # Mathematica notebooks
├── examples/              # Demo scripts (beginner, GPU, ML physics)
├── tests/                 # Test suite (Python, MATLAB, Mathematica)
├── scripts/               # Validation and deployment scripts
├── pyproject.toml         # Package configuration
└── CITATION.cff           # Academic citation metadata
```

---

## Key Configuration

| File | Purpose |
|------|---------|
| `pyproject.toml` | Build, deps, tool config |
| `AGENTS.md` | Governance invariants (normative) |
| `CITATION.cff` | Academic citation metadata |

---

## Important Notes / Known Quirks

<!-- Standard research library notes -->

**Deterministic seeds** -- All benchmark and experiment runs must use fixed seeds.
Reproducibility is a governance invariant. Never remove seed arguments from benchmark
or test code.

**Archive is read-only** -- If an `archive/` directory exists, it contains historical
data and papers. Never modify its contents.

**API stability** -- Breaking changes to the public API require a version bump and a
`CHANGELOG.md` entry.

**Pre-commit / linting** -- Run the project's format command before committing.

<!-- EXTENSION SLOT: Domain-Specific Notes
     Add project-specific quirks, numerical issues, data handling rules,
     dependency caveats, etc.
-->

**Cross-platform parity** -- New Python features should have MATLAB/Mathematica equivalents
where feasible. This is a governance requirement.

**GPU/CPU fallback** -- All GPU code must include automatic CPU fallback. Never assume CuPy
is available.

**Google Colab compatibility** -- Do not add dependencies that break Google Colab compatibility.

---

## Domain-Specific Rules

<!-- EXTENSION SLOT: Domain-Specific Rules
     Each project fills this section with rules unique to its research domain.
-->

- **Cross-platform parity required**: New Python features should have MATLAB/Mathematica equivalents where feasible
- **GPU code must have CPU fallback**: All CuPy/CUDA code must include automatic CPU fallback paths
- **Google Colab compatibility**: Do not add dependencies that break Colab environments
- **Update CITATION.cff for releases**: Academic citation metadata must stay current
- **MATLAB naming**: MATLAB files use `camelCase.m`; Python modules use `snake_case.py`

---

## Data Integrity

<!-- EXTENSION SLOT: Data Integrity
     Define project-specific rules for data handling, reproducibility,
     and research artifact management.
-->

- **Cross-platform numerical consistency**: Validation suite ensures Python, MATLAB, and Mathematica produce equivalent results within tolerance
- **Benchmark results must be reproducible**: Fixed seeds and pinned dependency versions for published comparisons

---

## Governance

See [AGENTS.md](AGENTS.md) for rules. See [SSOT.md](SSOT.md) for current state.
