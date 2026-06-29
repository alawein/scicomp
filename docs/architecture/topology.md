---
type: canonical
last_updated: 2026-06-29
---

# Repository topology

Archetype: `python-research-package` with earned multi-language roots (fleet topology canon).

On-disk layout as of 2026-06-29. `Python/` is the canonical Python import boundary by design.

## Tree

```text
scicomp/
├── Python/                      # canonical Python package (berkeley_scicomp)
│   ├── Linear_Algebra/ FEM/ ODE_PDE/ Optimization/
│   ├── Monte_Carlo/ Multiphysics/ Quantum/ QuantumOptics/
│   ├── Machine_Learning/ ml_physics/ gpu_acceleration/
│   └── Plotting/ Crystallography/ Elasticity/ Optics/ ...
├── MATLAB/                      # parallel MATLAB modules
├── Mathematica/                 # parallel Mathematica notebooks
├── examples/                    # cross-language usage examples
├── notebooks/                   # teaching and exploratory notebooks
├── tests/                       # Python pytest suite; matlab/ batch tests
├── scripts/                     # validate_framework.py and maintenance helpers
├── reports/                     # exported report artifacts
├── performance_baselines.json   # timing baselines for regression checks
└── docs/                        # installation, API, theory, GPU guide
```

## Surfaces

| Path | Role |
|------|------|
| `Python/` | Canonical Python import root; `pip install -e ".[dev]"` |
| `MATLAB/` | MATLAB R2024b+ modules and batch tests |
| `Mathematica/` | Wolfram notebooks mirroring selected Python topics |
| `examples/` | Guided entry points per language surface |
| `tests/` | Python tests; MATLAB parity via `tests/matlab/` |
| `scripts/` | Framework validation and repo hygiene |

## Rules

- Do not introduce a parallel `src/` tree without an explicit migration plan.
- Keep GPU, symbolic, and teaching workflows documented per language surface.
- Large datasets stay external; examples use generated or inline inputs.

## Related docs

- [architecture.md](../architecture.md) for component overview
- [INSTALLATION_GUIDE.md](../INSTALLATION_GUIDE.md) for per-language setup
