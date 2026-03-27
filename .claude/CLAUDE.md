---
type: derived
source: org/governance-templates
sync: script
sla: on-change
authority: canonical
audience: [agents, contributors]
last-verified: 2026-03-26
---

# scicomp — Claude Code Configuration

## Project Context

Cross-platform scientific computing framework for quantum mechanics, thermal

## Quick Links

- Governance: [AGENTS.md](AGENTS.md)
- Shared governance guides: [../../../docs/shared/](../../../docs/shared/)

## Session Bootstrap

Before working:
1. Run `git log --oneline -5` to see recent work
2. Read root `CLAUDE.md` for project-specific context
3. Run the project's test suite to verify current state

## Work Style

- Execute, do not plan. When asked to do something, do it.
- One change at a time. Make the smallest complete change, verify, then move to next.
- If stuck for >2 tool calls, stop and ask.

## Test Gates

After modifying code, run relevant tests before proceeding.

## Environment

- Git configured for LF (not CRLF)
- Python: use `python` (not `python3`)
- No credentials in chat; use `gh secret set` or `vercel env add` instead
