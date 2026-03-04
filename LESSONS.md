---
type: lessons
authority: observed
audience: [ai-agents, contributors, future-self]
last-updated: 2026-03-04
---

# LESSONS — SciComp

> Observed patterns only. Minimal initial entry — update as lessons accumulate.

## Patterns That Work

- **Equivalent implementations across Python, MATLAB, and Mathematica**: Providing the same algorithm in three environments lets researchers use whichever tool their institution or workflow supports, and cross-validation across languages catches implementation bugs.
- **HDF5 for large simulation data**: Using h5py for output storage rather than CSV or NumPy `.npy` files handles large, hierarchical scientific datasets efficiently and enables partial reads.

## Anti-Patterns

- **GPU code paths without CPU fallbacks**: CuPy-accelerated code should always have a NumPy fallback; most users won't have a compatible GPU and should not be blocked from running the framework.
- **Sharing mutable state between MATLAB and Python implementations**: The two runtimes cannot share memory; any cross-language workflow must go through file I/O or a defined data exchange format.

## Pitfalls

- **MATLAB licensing on HPC clusters**: MATLAB availability on HPC systems varies by institution; always document which computations require MATLAB vs. those that can run with open-source Python/Mathematica alternatives.
- **Physics-informed ML models that overfit to training physics**: Models trained on one physical regime (e.g., one temperature range) often fail outside it; always include out-of-distribution validation in benchmarks.
