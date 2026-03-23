---
type: reference
audience: [contributors]
---

# Coding Guidelines

## Naming Conventions

**Files:**
- Python: `snake_case.py`
- TypeScript components: `PascalCase.tsx`
- Config files: `kebab-case.json` or `kebab-case.md`

**Functions/Methods:**
- Verb-noun pattern: `fetchData()`, `buildWidget()`
- Consistent tense: present for operations (`validate`), past for state (`loaded`)

**Git Branches:**
- Feature: `feat/description`
- Fix: `fix/issue-number`
- Docs: `docs/topic`
- Chore: `chore/task`

**Commits:**
- Conventional commits: `feat(scope): subject`, `fix(scope): subject`
- Subject: lowercase, imperative, <50 chars
- Body: explain why, not what (if needed)

## Code Style

Style configuration: See eslint.config.js (ESLint rules), prettier.config.js (formatting), and vite.config.ts (build).

## Testing

- Write tests before code (TDD)
- Test file colocation: `src/foo.ts` → `src/foo.test.ts`
- Run: `npm test` before committing

## Documentation

- README.md: Project overview, quick start, installation
- Code comments: Why, not what. Comments explain intent.
- Architecture docs: `docs/architecture/` — design decisions
