---
type: canonical
source: none
sync: none
sla: none
---

# Repo Sweep — Universal Agent Prompt

> Drop into any agent on any repo under `alawein/`. Stack-agnostic, governance-aware.

---

## Rules

- **No features.** Fix, clean, document — nothing new.
- **No push without confirmation.** Stage commits, show summary, wait for go.
- **No destructive git.** No force-push, no rebase of shared branches, no history rewrite.
- **Respect existing governance.** If `AGENTS.md` says "ask first", ask first.

---

## Phase 0 — Orient

Read governance files in this order (skip missing ones, note which are absent):

1. `AGENTS.md` → boundaries, always/never/ask-first rules
2. `CLAUDE.md` → dev workflow, quality gates, structure
3. `SSOT.md` → current state, version, what's active
4. `LESSONS.md` → known patterns, anti-patterns, pitfalls

Then discover the stack:

| Signal | Stack | Lint | Types | Test | Build |
|--------|-------|------|-------|------|-------|
| `pyproject.toml` / `requirements.txt` | Python | `ruff check .` | `mypy .` | `pytest` | — |
| `package.json` + `tsconfig.json` | TS/Node | `npx eslint .` | `npx tsc --noEmit` | `npx vitest run` or `npx jest` | `npm run build` |
| `package.json` (no tsconfig) | JS/Node | `npx eslint .` | — | `npx vitest run` or `npx jest` | `npm run build` |
| `Cargo.toml` | Rust | `cargo clippy` | (built-in) | `cargo test` | `cargo build` |
| `go.mod` | Go | `golangci-lint run` | (built-in) | `go test ./...` | `go build ./...` |
| `*.html` + no manifest | Static | — | — | — | — |

Record which commands exist and which don't. This is your baseline.

---

## Phase 1 — Validate

Run every available check from Phase 0. Record pass/fail counts as baseline:

```
BASELINE (before):
  lint:       ___  (pass/fail/n-a)
  typecheck:  ___
  test:       ___  (X passed, Y failed, Z skipped)
  build:      ___
```

If a command doesn't exist (e.g. no test runner configured), record `n/a`.

---

## Phase 2 — Fix (strict priority order)

Work top-to-bottom. Do not skip ahead.

1. **Build blockers** — missing deps, broken imports, config errors that prevent `build` from completing.
2. **Type errors** — fix all `tsc --noEmit` / `mypy` failures.
3. **Test failures** — fix failing tests. Do NOT add new tests or delete existing ones.
4. **Lint errors** — fix auto-fixable first (`--fix`), then manual.
5. **Dead code** — remove unused imports, unreachable code, commented-out blocks older than 30 days.
6. **Security** — exposed secrets (remove + rotate), known vulnerable deps (`npm audit fix` / `pip audit`).
7. **Dependency hygiene** — remove unused deps, pin floating versions, update lockfile.

---

## Phase 3 — Governance

Verify these files exist and are accurate. Create missing ones from what the repo actually contains.

### Required files (per alawein convention)

| File | Purpose | Create if missing? |
|------|---------|-------------------|
| `AGENTS.md` | Agent boundaries, always/never/ask-first | ✅ Yes — derive from repo purpose |
| `CLAUDE.md` | Dev workflow, quality gates, structure | ✅ Yes — derive from stack + scripts |
| `SSOT.md` | Current state, version, status | ✅ Yes — derive from repo contents |
| `LESSONS.md` | Observed patterns and anti-patterns | ✅ Yes — minimal initial entry |
| `README.md` | Project overview, setup, usage | ✅ Yes — derive from package manifest + src |

### Governance file format

All governance files must have YAML frontmatter:

```yaml
---
type: normative | guide | lessons
authority: canonical | observed
last-verified: YYYY-MM-DD
audience: [ai-agents, contributors]
---
```

### Accuracy checks

- `SSOT.md` structure tree matches actual file layout
- `CLAUDE.md` quality gates match actual available commands
- `AGENTS.md` boundaries make sense for the repo's purpose
- `README.md` setup instructions actually work
- `LESSONS.md` doesn't contain stale or contradicted entries

---

## Phase 4 — Re-validate

Run the same checks from Phase 1. All must pass (or match `n/a` baseline).

```
AFTER:
  lint:       ___
  typecheck:  ___
  test:       ___
  build:      ___
```

If anything regressed, fix it before proceeding.

---

## Phase 5 — Commit

Stage commits grouped by scope, each independently revertible:

```
fix(<scope>): <what was fixed>
chore(<scope>): <cleanup or dep change>
docs(<scope>): <governance file created or updated>
```

Examples:
- `fix(types): resolve 3 TypeScript strict-mode errors`
- `chore(deps): remove unused lodash dependency`
- `docs(governance): create SSOT.md from repo state`

**Do NOT push.** Show the commit list and wait for confirmation.

---

## Phase 6 — Report

Produce a summary table:

```markdown
## Sweep Report: <repo-name>

| Check      | Before | After | Delta |
|------------|--------|-------|-------|
| Lint       |        |       |       |
| Typecheck  |        |       |       |
| Tests      |        |       |       |
| Build      |        |       |       |

### Governance
| File        | Status |
|-------------|--------|
| AGENTS.md   | ✅ existed / 🆕 created / 🔧 updated |
| CLAUDE.md   | ... |
| SSOT.md     | ... |
| LESSONS.md  | ... |
| README.md   | ... |

### Remaining Items
- [ ] ...

### Recommendations
- ...
```

Append any new lessons to `LESSONS.md` (observed patterns only, not aspirational).

---

## Repo Roster (alawein workspace)

For batch execution, here are the repos grouped by stack:

### TypeScript / React (product)
`gymboy` · `meshal-web` · `repz` · `scribd` · `attributa` · `llmworks` · `qmlab` · `simcore` · `bolts` · `atelier-rounaq`

### Python (research / tools)
`qaplibria` · `meatheadphysicist` · `neper` · `edfp` · `maglogic` · `qmatsim` · `qubeml` · `scicomp` · `spincirc` · `loopholelab` · `adil`

### Tooling
`_devkit` · `_ops` · `_workspace`

### Static / Other
`chshlab` · `helios` · `ingesta-toolkit`

### Org Profile (docs-only)
`alawein`

---

## Notes

- This prompt is stack-agnostic. Phase 0 auto-detects the stack.
- It respects existing `AGENTS.md` boundaries — if a repo says "ask first" for something, the agent asks.
- It explicitly forbids adding features or pushing without confirmation.
- Governance files follow the alawein YAML frontmatter convention.
- For batch execution across multiple repos, see `alawein/docs/governance/parallel-batch-execution.md`.
