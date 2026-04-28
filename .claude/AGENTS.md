---
type: derived
source: org/governance-templates
sync: script
sla: on-change
authority: canonical
audience: [agents, contributors]
last-verified: 2026-04-16
---

# scicomp — local governance mirror

Use the root governance files as the source of truth for this repo.

## Authority

- Root [AGENTS.md](AGENTS.md) is authoritative for repo rules and operating boundaries.
- Root [CLAUDE.md](CLAUDE.md) is authoritative for repo context and implementation constraints.
- Shared voice contract: <https://github.com/alawein/alawein/blob/main/docs/style/VOICE.md>

## Operating Rules

- Change the smallest complete surface and verify immediately.
- Keep GitHub-facing `README.md` and `docs/README.md` frontmatter-free.
- Keep `SSOT.md`, `LESSONS.md`, and `CHANGELOG.md` aligned when structure or behavior changes.
- Treat generated or runtime state as generated. Fix the source or validator boundary instead of hand-editing artifacts.
- Never commit secrets, tokens, or credentials.

## Handoff

- Record meaningful structural or behavioral changes in the repo-local docs that already own that contract.
- Leave follow-up work in visible repo surfaces, not hidden chat state.
