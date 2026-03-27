---
type: canonical
source: none
sync: none
sla: none
---

# GitHub ↔ Notion ops sync (this repo)

## What syncs where

| Surface | Source of truth | Notes |
|--------|------------------|--------|
| **Project row** in Notion "Projects (Canonical)" | [`alawein/alawein` `projects.json`](https://github.com/alawein/alawein/blob/main/projects.json) | If this repo is listed under **featured**, **notion_sync**, or **research**, org sync applies. |
| **This repo's activity** (PRs / issues / commits) | GitHub API | Use the sync report script below for scans and dashboards. |

There is **no** per-repo push to Notion in CI yet. The placeholder workflow [`.github/workflows/notion-sync.yml`](../../.github/workflows/notion-sync.yml) documents how to wire it when secrets exist.

## Generate a sync report (commits + open PRs + open issues)

Requires **Node 18+** (built-in `fetch`). From repo root, with a token that can **read** this repo:

```bash
export GH_TOKEN="ghp_..."   # or fine-grained PAT with Contents: Read
export GITHUB_REPOSITORY="alawein/scicomp"   # optional; defaults to alawein/scicomp
node scripts/github-sync-report.mjs
```

Artifact: `reports/sync-report.scicomp.json` (gitignored). In **GitHub Actions**, run workflow **"Ops — GitHub sync report"** (workflow_dispatch); it uploads the JSON as a workflow artifact.

**CI parity:** `GITHUB_TOKEN` is injected automatically; `GITHUB_REPOSITORY` is set by Actions.

## Canonical Notion project sync (org repo)

Full procedure: [alawein `docs/operations/notion-projects-database.md`](https://github.com/alawein/alawein/blob/main/docs/operations/notion-projects-database.md).

## Why this layout

- Small, repeatable **report** for ops without coupling every repo to Notion.
- **Org repo** remains the single place that maps `projects.json` → Notion rows.
