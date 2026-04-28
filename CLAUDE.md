---
type: canonical
source: none
sync: none
sla: none
authority: canonical
audience: [ai-agents, contributors]
last_updated: 2026-04-15
last-verified: 2026-04-15
---

# CLAUDE.md — SciComp

## Workspace identity

SciComp is a research-library repo for cross-platform scientific computing
across Python, MATLAB, and Mathematica. The repo is broad, but the work should
still read like computational physics and numerical methods, not like a generic
"AI for science" bundle.

Shared voice and research-writing contract:

- <https://github.com/alawein/alawein/blob/main/docs/style/VOICE.md>
- <https://github.com/alawein/alawein/blob/main/prompt-kits/AGENT.md>

## Directory structure

- `Python/`: canonical Python package and CLI surface
- `MATLAB/`: MATLAB implementations
- `Mathematica/`: symbolic notebooks and analytical workflows
- `examples/`: runnable demonstrations
- `tests/`: required verification across surfaces
- `docs/`: theory, installation, API, and troubleshooting
- `performance_baselines.json`: reference performance data

## Governance rules

1. Keep `Python/` as the canonical Python import boundary. Do not silently
   collapse the repo into a lowercase or `src/` layout.
2. Preserve cross-platform parity where it is part of the repo contract.
3. GPU paths must degrade cleanly to CPU paths when acceleration is unavailable.
4. Numerical changes need tolerance-aware tests and explicit rationale.
5. Do not rewrite the repo into one framework-specific subculture. Python,
   MATLAB, and Mathematica each remain first-class surfaces.
6. Treat performance baselines and reference examples as measurement surfaces,
   not casual copy.

## Code conventions

- Public Python behavior lives under `Python/`.
- Comments explain the mathematical idea, numerical assumption, or stability
  tradeoff before implementation detail.
- Keep notation and terminology consistent across the three language surfaces.
- Avoid renaming directory conventions just to look more conventional.

## Build and test commands

```bash
pip install -e ".[dev]"
pytest --cov=Python
ruff check Python/
mypy Python/
python scripts/validate_framework.py
matlab -batch "run('tests/matlab/test_heat_transfer.m')"
```
