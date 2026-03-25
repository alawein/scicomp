# Ops runbook — sync reports & Notion

## Sync report failures

### `Missing GITHUB_TOKEN` / 401 from GitHub API

- **CI:** Should not happen on `workflow_dispatch` for this repository; token is `GITHUB_TOKEN`. If it does, check workflow `permissions` include `contents: read`, `pull-requests: read`, `issues: read`.
- **Local:** Export `GH_TOKEN` or `GITHUB_PAT` (classic: `repo` scope for private repos; public repo needs `public_repo` or fine-grained “Contents” read).

### 403 / Resource not accessible

- PAT may lack access to the org/repo.
- For SSO-enabled orgs, authorize the token for the org in GitHub settings.

### Rate limit (403 + `rate limit` in message)

- Authenticated REST limit is **5,000/hour** per installation/token under normal use.
- **Remediation:** wait, use `GITHUB_TOKEN` in Actions instead of anonymous calls, or reduce report frequency.

## Notion sync (when implemented)

### Missing secrets

Configure in repo or org **Secrets**:

| Secret | Purpose |
|--------|---------|
| `NOTION_TOKEN` | Integration secret from [notion.so/my-integrations](https://www.notion.so/my-integrations) |
| `NOTION_DB_ID` | Target database ID (Projects Canonical) |

### Integration not connected to database

- In Notion: open database → **…** → **Connections** → add your integration.
- Without this, API returns **404** or **object not found**.

### Property name mismatch

- Org sync uses property names from [`alawein/alawein` notion-sync workflow](https://github.com/alawein/alawein/blob/main/.github/workflows/notion-sync.yml). Align Notion column names or set the documented `NOTION_*_PROPERTY` env overrides.

## Who to check

- **GitHub:** repository `Settings` → `Actions` → workflow runs.
- **Notion:** integration capabilities and database connection (see [SYNC.md](./SYNC.md)).
