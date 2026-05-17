# SciComp

Status:      frozen
Category:    research
Owner:       alawein
Visibility:  public
Purpose:     Scientific computing utilities and shared numerical tooling.
Next action: continue

SciComp is a cross-platform scientific computing suite that keeps Python,
MATLAB, and Mathematica in the same repo on purpose. The value here is not just
having many numerical topics in one place. The value is maintaining a shared
scientific vocabulary across those implementations and exposing where GPU,
symbolic, and teaching workflows diverge.

The Python package surface is unusual by normal packaging standards:
`Python/` is the canonical import boundary. That constraint is deliberate and
should stay visible.

## Public value

SciComp is a research-portfolio candidate because it demonstrates breadth
across numerical methods, languages, GPU workflows, symbolic tooling, and
teaching examples. Public polish should make the unusual cross-language layout
feel intentional: explain which surface to use, what each language contributes,
and how examples can be reproduced.

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

## Publication boundaries

Keep machine-specific MATLAB/Mathematica paths, GPU environment assumptions,
large generated outputs, and unpublished teaching/research data out of public
examples. If a notebook or script supports a claim, document the required
runtime and expected output.

## Documentation

Start with [docs/README.md](docs/README.md) for installation notes, API
reference, GPU guidance, and theory material.
