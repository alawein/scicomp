#!/usr/bin/env node
/**
 * Writes reports/sync-report.<slug>.json — last commits, open PRs, open issues (GitHub REST).
 * Why: deterministic, no extra deps; works locally with GH_TOKEN/PAT or in CI via GITHUB_TOKEN.
 *
 * Usage:
 *   GITHUB_REPOSITORY=alawein/scicomp node scripts/github-sync-report.mjs
 */
import { mkdir, writeFile } from "node:fs/promises";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = join(__dirname, "..");

function authHeaders(token) {
  return {
    Accept: "application/vnd.github+json",
    Authorization: `Bearer ${token}`,
    "X-GitHub-Api-Version": "2022-11-28",
  };
}

async function getJson(url, headers) {
  const res = await fetch(url, { headers });
  const text = await res.text();
  let body;
  try {
    body = text ? JSON.parse(text) : null;
  } catch {
    body = { raw: text };
  }
  if (!res.ok) {
    const msg = body?.message || text || res.statusText;
    throw new Error(`GitHub API ${res.status} ${url}: ${msg}`);
  }
  return body;
}

async function main() {
  const token =
    process.env.GITHUB_TOKEN || process.env.GH_TOKEN || process.env.GITHUB_PAT;
  const repository =
    process.env.GITHUB_REPOSITORY ||
    process.env.GH_REPO ||
    "alawein/scicomp";

  if (!token) {
    console.error(
      "Missing GITHUB_TOKEN (CI) or GH_TOKEN / GITHUB_PAT (local). Not fetching GitHub.",
    );
    process.exitCode = 1;
    return;
  }

  const [owner, repo] = repository.split("/");
  if (!owner || !repo) {
    console.error(`Invalid repository slug: ${repository}`);
    process.exitCode = 1;
    return;
  }

  const headers = authHeaders(token);
  const base = "https://api.github.com";

  const repoMeta = await getJson(`${base}/repos/${owner}/${repo}`, headers);
  const defaultBranch = repoMeta.default_branch || "main";

  const commits = await getJson(
    `${base}/repos/${owner}/${repo}/commits?per_page=10`,
    headers,
  );
  const pulls = await getJson(
    `${base}/repos/${owner}/${repo}/pulls?state=open&per_page=100`,
    headers,
  );
  const issuesRaw = await getJson(
    `${base}/repos/${owner}/${repo}/issues?state=open&per_page=100`,
    headers,
  );
  const openIssuesOnly = Array.isArray(issuesRaw)
    ? issuesRaw.filter((i) => !i.pull_request)
    : [];

  const slug = repo;
  const report = {
    generatedAt: new Date().toISOString(),
    repository: repository,
    defaultBranch,
    counts: {
      lastCommitsSampled: Array.isArray(commits) ? commits.length : 0,
      openPullRequests: Array.isArray(pulls) ? pulls.length : 0,
      openIssues: openIssuesOnly.length,
    },
    lastCommits: (Array.isArray(commits) ? commits : []).map((c) => ({
      sha: c.sha?.slice(0, 7),
      date: c.commit?.author?.date,
      message: (c.commit?.message || "").split("\n")[0],
    })),
    openPullRequests: (Array.isArray(pulls) ? pulls : []).map((p) => ({
      number: p.number,
      title: p.title,
      url: p.html_url,
    })),
    openIssues: openIssuesOnly.map((i) => ({
      number: i.number,
      title: i.title,
      url: i.html_url,
    })),
  };

  const reportsDir = join(REPO_ROOT, "reports");
  await mkdir(reportsDir, { recursive: true });
  const outPath = join(reportsDir, `sync-report.${slug}.json`);
  await writeFile(outPath, JSON.stringify(report, null, 2) + "\n", "utf8");
  console.log(`Wrote ${outPath}`);
}

main().catch((e) => {
  console.error(e);
  process.exitCode = 1;
});
