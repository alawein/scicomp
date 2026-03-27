---
type: canonical
source: none
sync: none
sla: none
---

<!-- Template: research-library v1.0.0 -->
<!-- Generated from _pkos governance templates. Do not edit the template sections -->
<!-- directly in consuming projects — update the template and re-sync instead.    -->
---
type: normative
authority: canonical
audience: [agents, contributors, maintainers]
last-verified: 2026-03-09
---

# AGENTS — scicomp

> **Status: Normative.** Do not modify without maintainer review.

This repository is governed by clear engineering and documentation standards
aligned with the **Morphism Categorical Governance Framework** principles.

## Governance Source

| Authority | Location |
|-----------|----------|
| Root governance | [AGENTS.md](AGENTS.md) (this file) |
| Contributing guide | [CONTRIBUTING.md](CONTRIBUTING.md) |
| Changelog | [CHANGELOG.md](CHANGELOG.md) |

## Repository Scope

Python + MATLAB + Mathematica library providing equivalent implementations
across platforms. Features GPU acceleration via CuPy/CUDA with automatic
CPU fallback, quantum simulations, and physics-informed neural networks.

## Directory Layout

| Directory | Purpose | Governance Level |
|-----------|---------|-----------------|
| `scicomp/` | Core Python package | **Primary** -- all changes require tests |
| `matlab/` | MATLAB implementations | **Primary** -- must maintain parity |
| `mathematica/` | Mathematica notebooks | **Primary** -- must maintain parity |
| `examples/` | Demo scripts (beginner, GPU, ML physics) | **Illustrative** -- must stay runnable |
| `tests/` | Test suite (Python, MATLAB, Mathematica) | **Required** -- never delete without replacement |
| `scripts/` | Validation and deployment scripts | **Tooling** -- document changes |

## Invariants (Must Always Hold)

<!-- STANDARD INVARIANTS — do not remove or weaken these -->

1. **Tests pass**: All tests must pass before merging to main
2. **Lint clean**: Linter must exit 0 on the primary source directories
3. **Imports work**: The package must be importable after install
4. **No secrets**: API keys or credentials must never appear in source
5. **Reproducibility**: Experiment and benchmark results must be deterministic (fixed seeds)
6. **README accurate**: README code examples must match actual API signatures

<!-- EXTENSION SLOT: Additional Invariants
     Add project-specific invariants here.
-->
7. **Cross-platform parity**: New Python features should have MATLAB/Mathematica equivalents where feasible
8. **GPU/CPU fallback**: All GPU code must include automatic CPU fallback

## Agent Rules

When this repository is modified by an AI agent or automated tool:

<!-- STANDARD AGENT RULES — do not remove or weaken these -->

- **Read** `AGENTS.md` and `CONTRIBUTING.md` before making changes
- **Never** skip the test suite -- run tests before committing
- **Always** update `CHANGELOG.md` when changing public API or behavior
- **Always** keep docstrings and type hints accurate
- **Prefer** small, focused commits with conventional commit messages
- **Never** modify validated benchmark results or reference data

### Research-Specific Agent Rules

- **Data integrity**: Do not modify, rename, or delete files in immutable data
  directories (e.g., `data/`, `archive/`). Populate data directories via
  provided scripts; treat them as read-only afterward.
- **Numerical precision**: When comparing floating-point results, use tolerance-based
  comparisons. Do not tighten tolerances without verifying against known reference
  values. Document the precision requirements of any new numerical method.
- **Citation / attribution**: Update `CITATION.cff` for release-grade changes.
  Preserve author attribution in file headers. Reference the originating paper
  when implementing published algorithms.
- **Reproducibility**: All experiments, benchmarks, and simulations must be
  reproducible. Use fixed random seeds, pin dependency versions for published
  results, and record full parameter provenance for simulation outputs.

<!-- EXTENSION SLOT: Project-Specific Agent Rules
     Add rules unique to this project's domain.
-->
- Maintain cross-platform parity -- new Python features should have MATLAB/Mathematica equivalents where feasible
- GPU code must include automatic CPU fallback
- Use `ruff` for linting and `mypy` for type checking
- Update `CITATION.cff` for releases
- Do not add dependencies that break Google Colab compatibility

## Naming Conventions

- **Modules**: `snake_case.py`
- **Classes**: `PascalCase`
- **Functions**: `snake_case`
- **Constants**: `UPPER_SNAKE_CASE`
- **MATLAB files**: `camelCase.m`

## Commit Message Format

```
type(scope): short description

feat(quantum): add VQE optimizer
fix(thermal): correct boundary condition handling
docs(readme): update installation instructions
test(gpu): add CuPy fallback edge case
refactor(core): extract validation to shared utility
```

Types: `feat`, `fix`, `docs`, `test`, `refactor`, `perf`, `ci`, `chore`

## Dependency Policy

- **Core deps**: Keep minimal -- NumPy, SciPy, Matplotlib, SymPy, h5py
- **Optional deps**: CuPy, TensorFlow, PyTorch, scikit-learn as extras
- **Dev deps**: pytest, ruff, mypy -- no production code may import dev deps
- **Version pins**: Minimum versions only (no upper bounds unless proven necessary)

---

*Aligned with Morphism Systems governance principles.*

See [CLAUDE.md](CLAUDE.md) | [SSOT.md](SSOT.md)
