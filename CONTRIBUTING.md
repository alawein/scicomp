---
type: canonical
source: _devkit/templates
sync: propagated
sla: none
---

<!-- Token legend:
     AUTO-SUBSTITUTED by sync-contributing.sh (derived from git remote):
       scicomp = GitHub slug used as heading (e.g. "bolts", "handshake-hai")
       scicomp      = GitHub slug used in URLs  (e.g. "bolts", "handshake-hai")
     MANUALLY FILLED in Plan 2 per-repo pass:
       {INSTALL_COMMAND}  = e.g. "npm ci" or "uv pip install -e ."
       {TEST_COMMAND}     = e.g. "npm test" or "pytest"
       {VALIDATE_COMMAND} = e.g. "npm run lint && npm test" or "ruff check . && pytest"
-->

# Contributing to scicomp

<!-- REPO-SPECIFIC: one-line context about what this repo is -->

This project follows the [alawein org contributing standards](https://github.com/alawein/alawein/blob/main/CONTRIBUTING.md).

## Getting Started

```bash
git clone https://github.com/alawein/scicomp.git
cd scicomp
{INSTALL_COMMAND}
```

## Development Workflow

1. Branch off `main` using prefix: `feat/`, `fix/`, `docs/`, `chore/`, `test/`
2. Make your changes — keep PRs focused on a single concern
3. Run `{TEST_COMMAND}` to validate your changes before committing
4. Commit using [Conventional Commits](https://www.conventionalcommits.org/) — `type(scope): subject`
5. Open a Pull Request to `main`

## Code Standards

<!-- REPO-SPECIFIC: 2-4 bullets about this repo's conventions -->
- Follow existing patterns in the codebase
- Run linting and type checks before committing
- Write tests for new functionality

## Pull Request Checklist

- [ ] CI passes (no failing checks)
- [ ] Tests added or updated for new functionality
- [ ] `{VALIDATE_COMMAND}` passes
- [ ] `CHANGELOG.md` updated under `[Unreleased]`
- [ ] No breaking changes without a version bump plan

## Reporting Issues

Open an issue on the [GitHub repository](https://github.com/alawein/scicomp/issues) with steps to reproduce and relevant context.

## License

By contributing, you agree that your contributions will be licensed under [MIT](LICENSE).
