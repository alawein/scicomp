# Cursor Rules for scicomp

You are working in scicomp.

## Context

[Brief project description and tech stack.]

## Key Files

- Config: [CLAUDE.md](../CLAUDE.md), [AGENTS.md](../AGENTS.md)
- Guidelines: [GUIDELINES.md](../GUIDELINES.md)
- Shared governance guides: [../../../docs/shared/](../../../docs/shared/)

## Work Style

- Execute incrementally. Small, complete changes.
- Read governance docs before structural changes.
- Use `/bootstrap` to load session context.
- No cross-project file access.

## Testing

Before committing:
- Run `npm test` (TypeScript projects)
- Run `pytest` (Python projects)

## Do Not

- Commit unverified changes
- Scope creep (refuse multi-file changes for single-sentence tasks)
- Assume file existence; verify with `ls` first
