---
type: canonical
source: none
sync: none
sla: none
---

# Changelog

All notable changes to SciComp will be documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

---

## [1.1.0] — 2026-03-06

### Added
- Test scaffolding for eigenstate normalization and scipy compat
- Workspace standardization (P1-P20) — governance files, CI, documentation

### Changed
- Consolidated configuration to `pyproject.toml`
- Added AGENTS.md governance rules
- Updated deprecated API usage to current numpy/scipy patterns

### Fixed
- Resolved 46 test failures: eigenstate normalization, numpy/scipy compatibility, skip guards

---

## [1.0.0] — 2026-01-01

### Added
- Scientific computing toolkit for computational physics
- Eigenstate solvers and numerical methods
- Comprehensive numpy/scipy integration

[Unreleased]: https://github.com/alawein/scicomp/compare/v1.1.0...HEAD
[1.1.0]: https://github.com/alawein/scicomp/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/alawein/scicomp/releases/tag/v1.0.0
