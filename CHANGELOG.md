---
type: canonical
source: none
sync: none
sla: none
---

# Changelog

All notable changes to SciComp will be documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Package versions are derived from the source-control build metadata. This
repository has no published Git release tags at the time of this update, so the
historical version headings below are archival notes rather than verifiable
released artifacts.

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
