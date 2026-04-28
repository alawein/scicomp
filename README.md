# SciComp

SciComp is a cross-platform scientific computing suite that keeps Python,
MATLAB, and Mathematica in the same repo on purpose. The value here is not just
having many numerical topics in one place. The value is maintaining a shared
scientific vocabulary across those implementations and exposing where GPU,
symbolic, and teaching workflows diverge.

The Python package surface is unusual by normal packaging standards:
`Python/` is the canonical import boundary. That constraint is deliberate and
should stay visible.

## Core surfaces

- `Python/`: canonical Python package and CLI entrypoint
- `MATLAB/`: MATLAB implementation surface
- `Mathematica/`: Mathematica notebooks and symbolic workflows
- `examples/`: runnable demos
- `tests/`: cross-surface verification
- `docs/`: API, theory, installation, and troubleshooting

## Focus areas

- Quantum mechanics and quantum computing
- Thermal transport and heat-transfer numerics
- Physics-informed machine learning
- GPU acceleration with explicit CPU fallback
- Spintronics, optics, control, and related computational physics modules

## Quick start

```bash
git clone https://github.com/alawein/scicomp.git
cd scicomp
pip install -e ".[dev]"
python scripts/validate_framework.py
pytest
```

## CLI

```bash
berkeley-scicomp --help
bsc --help
```

## Development

```bash
pytest --cov=Python
ruff check Python/
mypy Python/
python scripts/validate_framework.py
matlab -batch "run('tests/matlab/test_heat_transfer.m')"
```

## Documentation

Start with [docs/README.md](docs/README.md) for installation notes, API
reference, GPU guidance, and theory material.
