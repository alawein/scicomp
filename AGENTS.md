---
type: canonical
source: none
sync: none
sla: none
authority: canonical
audience: [agents, contributors, maintainers]
last_updated: 2026-04-15
last-verified: 2026-04-15
---

# AGENTS — SciComp

## Workspace identity

SciComp is a research-library repo for cross-platform scientific computing
across Python, MATLAB, and Mathematica.

## Directory structure

- `Python/`: primary Python surface
- `MATLAB/`: MATLAB implementations
- `Mathematica/`: symbolic notebooks
- `examples/`: runnable demos
- `tests/`: required verification

## Governance rules

1. Keep `Python/` as the canonical Python package boundary.
2. Preserve cross-platform parity where the repo already provides it.
3. GPU code must retain a CPU fallback path.
4. Numerical behavior changes need tests with explicit tolerances.
5. Do not normalize away the uppercase directory layout just for aesthetics.

## Code conventions

- Comments explain numerical assumptions and computational tradeoffs
- Keep terminology aligned across Python, MATLAB, and Mathematica
- Conventional commits only

## Build and test commands

```bash
pip install -e ".[dev]"
pytest --cov=Python
ruff check Python/
mypy Python/
python scripts/validate_framework.py
```
