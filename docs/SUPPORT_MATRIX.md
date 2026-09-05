---
type: canonical
source: pyproject.toml and CI
sync: none
sla: none
---

# SciComp support matrix

SciComp is a research library. The supported promise is deliberately narrower
than the source inventory: **the verified surface is the Python core exercised
by `pytest` in CI on Python 3.10–3.12**. A passing core run does not validate
every numerical model in the repository.

| Surface | Status | Install / verification |
|---|---|---|
| Python core (`Python/`, core dependencies) | Verified | `pip install -e ".[dev]"`; `python -m pytest` |
| Signal processing root regression suite | Verified | Included in `python -m pytest` |
| Visualization examples | Experimental optional | `pip install -e ".[viz]"` |
| Quantum-computing examples | Experimental optional | `pip install -e ".[quantum]"` |
| ML-physics examples and tests | Experimental optional | `pip install -e ".[ml]"` |
| GPU acceleration | Experimental optional | `pip install -e ".[gpu]"`; hardware-specific |
| Performance/distributed helpers | Experimental optional | `pip install -e ".[performance]"` |
| MATLAB tree | Experimental, runtime not verified in Python CI | Requires MATLAB |
| Mathematica tree | Experimental, runtime not verified in Python CI | Requires Mathematica |
| Untested Python domain packages | Experimental research modules | Retained; no stability or parity claim |

The repository uses the historical capitalized `Python` import boundary:
`from Python.Quantum.core.quantum_states import BellStates`. It does not
currently provide a separate lowercase `scicomp` import namespace.

## Example prerequisites

| Example | Command |
|---|---|
| `examples/beginner/basic_physics.py` | `python examples/beginner/basic_physics.py` |
| `examples/beginner/getting_started.py` | `python examples/beginner/getting_started.py` |
| `examples/beginner/harmonic_oscillator_demo.py` | `pip install -e ".[viz]"` first |
| `examples/intermediate/vqe_demo.py`, `examples/python/quantum_computing_demo.py` | `pip install -e ".[quantum]"` first |
| `examples/python/quantum_tunneling_demo.py` | `pip install -e ".[viz]"` first |
| `examples/python/ml_physics_demo.py` | `pip install -e ".[ml]"` first |

Optional selections are installed and smoke-tested independently in CI. They
remain experimental because full feature, hardware, and cross-language
validation is outside the verified Python-core promise.
