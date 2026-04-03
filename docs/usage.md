---
type: canonical
source: none
sync: none
sla: none
---

# Usage Guide

## Python

- Install editable: `pip install -e .`
- Quantum demo: `python examples/beginner/getting_started.py`
- GPU demo: `python examples/gpu_examples.py` (requires CUDA/CuPy)
- ML physics: `python examples/ml_physics_demo.py`

## MATLAB

- Run heat transfer tests: `matlab -batch "run('tests/matlab/test_heat_transfer.m')"`

## Mathematica

- Symbolic quantum checks: `wolframscript -f tests/mathematica/test_symbolic_quantum.nb`

## Tips

- Use `uv` for fast env creation: `uv pip install -e .`
- Keep large datasets out of git; place under `examples/data/` and ignore as needed.
- GPU runs should fall back to CPU automatically; report mismatches with environment details.
