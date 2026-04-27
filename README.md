# SciComp

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8+-green.svg)](https://www.python.org/)

Cross-platform scientific computing framework for quantum mechanics,
thermal transport, and physics-informed machine learning. Provides
equivalent implementations across Python, MATLAB, and Mathematica
for both research and education — with CPU/GPU parity and reproducible examples.

## Features

- Quantum mechanics: Bell states, entanglement, operators, circuits
- Quantum optics: Jaynes-Cummings, cavity QED, coherent states
- GPU acceleration: CUDA/CuPy with automatic CPU fallback
- ML physics: Physics-informed neural networks for PDEs and equation discovery
- Thermal transport: Heat solvers, phonon dynamics
- Signal processing: FFT, spectral methods
- Cross-platform: Python, MATLAB, and Mathematica APIs

## Quick Start

```bash
uv pip install berkeley-scicomp
```

More examples: [docs/examples.md](docs/examples.md)

## Usage Demo

```python
from scicomp.linalg import sparse_solve
from scicomp.optimize import gradient_descent
import numpy as np

A = np.random.randn(100, 100)
b = np.random.randn(100)
x = sparse_solve(A, b)
```

## Installation

```bash
git clone https://github.com/alawein/scicomp.git
cd scicomp
pip install -e .
```

Requirements: Python 3.8+, NumPy, SciPy, Matplotlib.
Optional: CUDA 11.0+, TensorFlow 2.0+.

## Usage

```bash
# Quantum simulations
python examples/beginner/getting_started.py

# GPU computations
python examples/gpu_examples.py

# ML physics
python examples/ml_physics_demo.py
```

## Roadmap

- **Near term:** stabilize GPU fallback paths; refresh PINN examples; document determinism tips.
- **Mid term:** add VQE/QAOA variants and cross-platform parity checks; expand thermal transport datasets.
- **Future:** JAX backends and distributed runners.

## TODO

- [ ] Add `.env.example` if future APIs require keys (none required now)
- [ ] Add sample datasets for thermal transport demos
- [ ] Publish determinism notes for GPU vs CPU runs

## Modules

- **Quantum**: Bell states, VQE, QAOA, Jaynes-Cummings
- **GPU**: CUDA kernels, automatic CPU fallback
- **ML Physics**: PINNs for heat/wave/Schrodinger equations
- **Platforms**: Python core, MATLAB/Mathematica support

## Testing

```bash
# Validation suite
python scripts/validate_framework.py

# Individual modules
python tests/python/test_quantum_physics.py

# Cross-platform
matlab -batch "run('tests/matlab/test_heat_transfer.m')"
wolframscript -f tests/mathematica/test_symbolic_quantum.nb
```

## Project Structure

```text
scicomp/
├── Python/          # Core implementation
│   ├── Quantum/     # Quantum mechanics/computing
│   ├── ml_physics/  # Physics-informed ML
│   └── utils/       # CLI tools
├── MATLAB/          # MATLAB versions
├── Mathematica/     # Symbolic computation
├── examples/        # Demo scripts
└── tests/           # Test suites
```

## Citation

```bibtex
@software{alawein2025scicomp,
  title={SciComp},
  author={Alawein, Meshal},
  year={2025},
  url={https://github.com/alawein/scicomp}
}
```

## License

MIT License -- see [LICENSE](LICENSE).

## Ownership

- **Maintainer:** @alawein
- **Support:** [GitHub Issues](https://github.com/alawein/scicomp/issues)
