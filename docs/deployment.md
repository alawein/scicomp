---
type: canonical
owner: platform-engineering
last-reviewed: 2026-03-31
---

# Deployment and Release -- scicomp

SciComp is a research library, not a hosted service. There is no server deployment, container
orchestration, or infrastructure to operate. The release surface is the `berkeley-scicomp` Python
package on PyPI and the public GitHub repository.

## Deployment Process

Not applicable. SciComp does not deploy to a server or cloud environment.

To reproduce the full environment locally:

```bash
git clone https://github.com/alawein/scicomp.git
cd scicomp
pip install -e ".[dev]"
python scripts/validate_framework.py
pytest
```

For GPU-accelerated paths, add the `[gpu]` extra and ensure a CUDA-compatible device and CUDA
Toolkit 11.0+ or 12.0+ are available:

```bash
pip install -e ".[dev,gpu]"
```

## Release Strategy

Releases follow semantic versioning. Version is managed via `setuptools_scm` (written to
`Python/_version.py`). A release is cut from `main` by tagging the commit; PyPI publication is
handled via the project's CI workflow.

## Rollback Procedures

Not applicable for a library. If a published PyPI release is broken, the prior version can be
pinned by consumers with `pip install berkeley-scicomp==<previous-version>`. Yanking a release
from PyPI requires maintainer access (contact: contact@meshal.ai).

## Environment Configuration

No environment variables are required for the base package. The optional `[gpu]` extra requires
a CuPy build that matches the installed CUDA version (`cupy-cuda11x` or `cupy-cuda12x`). See
[GPU_TESTING_GUIDE.md](GPU_TESTING_GUIDE.md) for verification steps.
