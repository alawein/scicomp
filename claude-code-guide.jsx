import { useState } from "react";

/* ═══════════════════════════════════════════════════════
   DATA: Reference Guide Sections
   ═══════════════════════════════════════════════════════ */
const refSections = [
  {
    id: "overview",
    icon: "🗺️",
    label: "The Big Picture",
    title: "Two Scopes, One System",
    content: (s) => (
      <div>
        <p style={s.p}>
          Claude Code reads configuration from <strong>two places</strong>, and understanding
          the split is the first thing to get right. Everything project-specific lives in your
          repo. Everything personal lives in your home directory. They compose — they don't conflict.
        </p>
        <div style={s.grid2}>
          <div style={s.card}>
            <div style={{...s.cardHead, background: "rgba(99,102,241,0.08)", borderColor: "rgba(99,102,241,0.15)"}}>
              <span style={{fontSize:"1.2rem"}}>📁</span>
              <div><div style={s.cardTitle}>Project-Level</div><code style={s.code}>your-project/.claude/</code></div>
            </div>
            <ul style={s.cardList}>
              <li><strong>Committed to git</strong> — shared with the team</li>
              <li>CLAUDE.md at project root for core instructions</li>
              <li>settings.json for permissions & hooks</li>
              <li>commands/, rules/, skills/, agents/</li>
              <li>settings.local.json for personal overrides (gitignored)</li>
            </ul>
          </div>
          <div style={s.card}>
            <div style={{...s.cardHead, background: "rgba(234,179,8,0.06)", borderColor: "rgba(234,179,8,0.15)"}}>
              <span style={{fontSize:"1.2rem"}}>🏠</span>
              <div><div style={s.cardTitle}>Global / Personal</div><code style={s.code}>~/.claude/</code></div>
            </div>
            <ul style={s.cardList}>
              <li><strong>Never committed</strong> — your personal defaults</li>
              <li>CLAUDE.md for cross-project preferences</li>
              <li>skills/ and commands/ available everywhere</li>
              <li>projects/ folder with auto-memory (MEMORY.md)</li>
              <li>keybindings.json, config.json</li>
            </ul>
          </div>
        </div>
        <Callout s={s} icon="⚡" title="Loading order">
          Global ~/.claude/CLAUDE.md loads first, then project CLAUDE.md, then any
          subdirectory CLAUDE.md files as you navigate deeper. Settings merge with
          project-local taking priority. The most specific instruction wins.
        </Callout>
      </div>
    ),
  },
  {
    id: "claudemd",
    icon: "📋",
    label: "CLAUDE.md",
    title: "CLAUDE.md — The Central Instruction Manual",
    content: (s) => (
      <div>
        <p style={s.p}>
          This is the single most important file in your setup. It loads into context at the
          start of every session, <strong>survives /compact</strong> (re-read from disk), and
          is the only reliable way to persist instructions. Chat messages don't survive compaction.
          CLAUDE.md does.
        </p>
        <Rule s={s} title="The golden rule">
          Only include what Claude <em>cannot infer from reading your code</em>.
          Build commands, architectural constraints, naming conventions, testing
          requirements, deployment quirks. If your linter already enforces it, don't
          repeat it here — use a hook instead.
        </Rule>
        <Code s={s} filename="CLAUDE.md">{`# Project: Acme API
Node 22, TypeScript, Fastify, Drizzle ORM, PostgreSQL.

## Commands
- \`pnpm dev\`: Dev server (port 3000)
- \`pnpm test\`: Vitest suite — always run before committing
- \`pnpm lint\`: Biome — runs via hook, don't manually invoke

## Architecture
- /src/routes/ → Fastify route handlers (one file per resource)
- /src/services/ → Business logic, never import from routes
- /src/db/ → Drizzle schema + migrations
- Services never call other services directly. Use events.

## Rules
- No raw SQL. Always use Drizzle query builder.
- Error responses use ApiError class from src/lib/errors.ts
- All new endpoints need integration tests in /tests/
- Never modify files in /src/generated/ — these are codegen output
- Prefer "X over Y" phrasing over "Do not Y" (Claude respects it more)`}</Code>
        <div style={s.grid2}>
          <TipBox s={s} variant="good" title="✅ Do">
            <li>Keep it under 200 lines per file</li>
            <li>Start with /init, then <strong>delete aggressively</strong></li>
            <li>Add rules only when Claude makes mistakes</li>
            <li>Use hierarchical CLAUDE.md in subdirs for monorepos</li>
            <li>Phrase as "Prefer X over Y" not "Do not Y"</li>
          </TipBox>
          <TipBox s={s} variant="bad" title="❌ Don't">
            <li>Duplicate what your linter enforces</li>
            <li>Include generic advice Claude already knows</li>
            <li>Write a novel — every line costs context tokens</li>
            <li>Forget to update it when conventions change</li>
            <li>Put personal preferences here (use CLAUDE.local.md)</li>
          </TipBox>
        </div>
        <Callout s={s} icon="💡" title="CLAUDE.local.md">
          For personal overrides that shouldn't be committed (editor preferences,
          personal shortcuts), create <code style={s.code}>CLAUDE.local.md</code> at
          the project root. It's automatically gitignored and loads alongside the shared CLAUDE.md.
        </Callout>
      </div>
    ),
  },
  {
    id: "rules",
    icon: "📐",
    label: "rules/",
    title: "rules/ — Modular, Growing Guidance",
    content: (s) => (
      <div>
        <p style={s.p}>
          When your CLAUDE.md starts getting unwieldy, <code style={s.code}>.claude/rules/</code> lets
          you break instructions into focused, modular files. Each <code style={s.code}>.md</code> file
          in this directory is loaded as additional context. Think of CLAUDE.md as the overview and rules/ as the
          detailed appendices.
        </p>
        <Code s={s} filename=".claude/rules/">{`.claude/rules/
├── code-style.md      → TypeScript conventions, import ordering
├── testing.md         → Test structure, mocking patterns, coverage
├── api-conventions.md → REST naming, error shapes, versioning
├── security.md        → Auth patterns, input validation, secrets
└── database.md        → Migration rules, query patterns, indexing`}</Code>
        <Rule s={s} title="When to use rules/ vs CLAUDE.md">
          <strong>CLAUDE.md</strong>: Project identity, build commands, top-level architecture — the stuff every session needs immediately.
          <br/><br/>
          <strong>rules/</strong>: Domain-specific depth that only matters when Claude is working in that area. A testing.md file doesn't need to burn context when Claude is writing a migration.
        </Rule>
        <Code s={s} filename=".claude/rules/testing.md">{`# Testing Conventions

## Structure
- Tests live next to source: src/services/user.ts → src/services/user.test.ts
- Integration tests in /tests/integration/ (need running DB)
- Use \`createTestContext()\` helper — never instantiate services directly

## Patterns
- Prefer factory functions over fixtures: \`createUser({role: "admin"})\`
- Mock external APIs at the HTTP layer (msw), not the service layer
- Every API endpoint needs at least: happy path, auth failure, validation error

## What NOT to test
- Don't test Drizzle schema definitions
- Don't test generated code in /src/generated/
- Don't write snapshot tests for API responses (they break on every change)`}</Code>
      </div>
    ),
  },
  {
    id: "commands",
    icon: "⚡",
    label: "commands/",
    title: "commands/ → skills/ — Reusable Workflows",
    content: (s) => (
      <div>
        <Callout s={s} icon="📌" title="Note: commands/ and skills/ have merged" variant="warn">
          As of early 2026, <code style={s.code}>.claude/commands/</code> and{" "}
          <code style={s.code}>.claude/skills/</code> create the same /slash-command interface.
          Existing commands/ files still work, but <strong>new workflows should go in skills/</strong> since
          they support frontmatter, bundled scripts, and auto-invocation.
        </Callout>
        <p style={s.p}>
          Commands are markdown files that become slash commands. Drop a file
          called <code style={s.code}>review.md</code> in .claude/commands/ and
          you get <code style={s.code}>/project:review</code>. Use <code style={s.code}>$ARGUMENTS</code> for parameterization.
        </p>
        <Code s={s} filename=".claude/commands/fix-issue.md">{`Fix GitHub issue #$ARGUMENTS following our coding standards.

1. Read the issue description and any linked discussion
2. Identify the affected files and create a plan
3. Implement the fix with appropriate tests
4. Run the full test suite before finishing
5. Create a commit with message: "fix: resolve #$ARGUMENTS"

Usage: /project:fix-issue 427`}</Code>
        <Code s={s} filename=".claude/commands/deploy.md">{`---
allowed-tools: Bash(git *), Bash(pnpm *)
description: Pre-deploy checklist and deployment
---
## Pre-deploy Checklist
- Current branch: !\`git branch --show-current\`
- Uncommitted changes: !\`git status --short\`
- Last test run: !\`pnpm test --run 2>&1 | tail -5\`

## Steps
1. Verify all tests pass (abort if they don't)
2. Verify we're on main or a release/* branch
3. Run \`pnpm build\` and verify no errors
4. Show me the deploy diff and wait for confirmation`}</Code>
        <p style={s.p}>
          The <code style={s.code}>!&#96;command&#96;</code> syntax is preprocessing — the shell command runs first and
          its output gets injected into the prompt. Claude only sees the result, not the command.
        </p>
      </div>
    ),
  },
  {
    id: "skills",
    icon: "✦",
    label: "skills/",
    title: "skills/ — Context-Aware Automation",
    content: (s) => (
      <div>
        <p style={s.p}>
          Skills are the evolved form of commands. Each skill is a <strong>directory</strong> (not
          a single file) containing a <code style={s.code}>SKILL.md</code> plus optional scripts,
          templates, and reference files. The key difference: skills support <strong>auto-invocation</strong> —
          Claude can decide to use them without you typing a slash command.
        </p>
        <Code s={s} filename=".claude/skills/">{`.claude/skills/
├── security-review/
│   ├── SKILL.md          ← The prompt + instructions
│   ├── checklist.md      ← Reference material
│   └── scripts/
│       └── scan.sh       ← Bundled tooling
├── tdd-workflow/
│   └── SKILL.md
└── create-migration/
    ├── SKILL.md
    └── templates/
        └── migration.ts  ← Template file`}</Code>
        <Code s={s} filename=".claude/skills/security-review/SKILL.md">{`---
name: security-review
description: Audit code for common security vulnerabilities
context: fork
agent: Explore
allowed-tools:
  - Read
  - Grep
  - Glob
---
# Security Review

Review the specified code for security issues. Check for:

1. **Injection**: SQL injection, XSS, command injection
2. **Auth**: Missing auth checks, privilege escalation
3. **Secrets**: Hardcoded credentials, leaked API keys
4. **Input**: Unvalidated user input, missing sanitization

Read the checklist at ./checklist.md for the full audit list.

Output a structured report with severity ratings:
🔴 Critical | 🟡 Warning | 🟢 Info`}</Code>
        <div style={s.grid2}>
          <TipBox s={s} variant="good" title="Key frontmatter options">
            <li><strong>context: fork</strong> — Run in isolated subagent, keeps main context clean</li>
            <li><strong>agent:</strong> — Which subagent: Explore, Plan, or custom from agents/</li>
            <li><strong>allowed-tools:</strong> — Restrict to specific tools (great for read-only tasks)</li>
            <li><strong>disable-model-invocation: true</strong> — Only runs when you explicitly invoke it</li>
          </TipBox>
          <TipBox s={s} variant="bad" title="Skills vs Commands cheatsheet">
            <li><strong>Need bundled scripts/templates?</strong> → Skill</li>
            <li><strong>Need auto-invocation?</strong> → Skill</li>
            <li><strong>Need tool restrictions?</strong> → Skill</li>
            <li><strong>Simple one-shot prompt?</strong> → Command is fine</li>
          </TipBox>
        </div>
      </div>
    ),
  },
  {
    id: "agents",
    icon: "🧠",
    label: "agents/",
    title: "agents/ — Isolated Subagent Personas",
    content: (s) => (
      <div>
        <p style={s.p}>
          Agents are specialized personas that run in isolation from your main session. They have
          their own system prompt, tool restrictions, and can even use different models. Think of them
          as coworkers with specific expertise that you delegate to.
        </p>
        <Code s={s} filename=".claude/agents/code-reviewer.md">{`---
description: Senior code reviewer that checks for quality issues
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash(git diff *)
  - Bash(git log *)
---
You are a senior code reviewer. Your job is read-only analysis.

## Review criteria
1. Logic errors and edge cases
2. Missing error handling
3. Performance issues (N+1 queries, unnecessary allocations)
4. API contract violations (check against OpenAPI spec)
5. Test coverage gaps

## Output format
For each finding:
- **File:Line** — what you found
- **Severity** — 🔴 Must fix | 🟡 Should fix | 🔵 Suggestion
- **Why** — explain the actual risk, not just the rule

Do NOT suggest style changes. Do NOT rewrite code.
Only report findings.`}</Code>
        <Rule s={s} title="When to use agents vs skills">
          <strong>Agents</strong> define <em>who does the work</em> — a persona with specific expertise and
          tool access. They run in isolation and return results to your main session.
          <br/><br/>
          <strong>Skills</strong> define <em>what work gets done</em> — a workflow with instructions and
          resources. Skills can specify which agent runs them via the <code style={s.code}>agent:</code> frontmatter.
          <br/><br/>
          In practice: a <code style={s.code}>security-review</code> skill might use
          a <code style={s.code}>security-auditor</code> agent. The skill defines the checklist. The agent
          defines the reviewer's personality and tool access.
        </Rule>
        <p style={s.p}>
          You can invoke agents explicitly: "Summarize this code using the code-reviewer agent" or reference
          them from skills via the <code style={s.code}>agent: code-reviewer</code> frontmatter field.
          Say "use subagents" in your prompt to tell Claude to parallelize work across multiple agents.
        </p>
      </div>
    ),
  },
  {
    id: "settings",
    icon: "⚙️",
    label: "settings.json",
    title: "settings.json — Permissions & Control",
    content: (s) => (
      <div>
        <p style={s.p}>
          This is the mechanical control layer — permissions, hooks, environment variables, and model
          selection. There are two files: <code style={s.code}>.claude/settings.json</code> (committed,
          team-shared) and <code style={s.code}>.claude/settings.local.json</code> (gitignored, personal).
          Local settings override shared ones.
        </p>
        <Code s={s} filename=".claude/settings.json">{`{
  "permissions": {
    "allow": [
      "Bash(pnpm *)",
      "Bash(git *)",
      "Bash(node *)",
      "Read",
      "Write",
      "Grep",
      "Glob"
    ],
    "deny": [
      "Bash(rm -rf *)",
      "Bash(curl *)",
      "Bash(wget *)"
    ]
  },
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "command": "npx biome check --fix \\"$CLAUDE_FILE_PATH\\" 2>/dev/null || true"
      }
    ]
  }
}`}</Code>
        <div style={s.grid2}>
          <TipBox s={s} variant="good" title="Hooks worth setting up">
            <li><strong>PostToolUse (Edit|Write)</strong> → Auto-format with Prettier/Biome</li>
            <li><strong>PostToolUse (Edit on .ts)</strong> → Run tsc --noEmit for type errors</li>
            <li><strong>PreCommit</strong> → Run lint + tests before any commit</li>
            <li><strong>Stop</strong> → Nudge Claude to verify work at end of turn</li>
          </TipBox>
          <TipBox s={s} variant="bad" title="Common mistakes">
            <li>Putting personal API keys in settings.json (use settings.local.json)</li>
            <li>Overly broad deny rules that break Claude's ability to work</li>
            <li>Forgetting hooks run on every edit — keep them fast (&lt;2s)</li>
            <li>Not testing hooks locally before committing</li>
          </TipBox>
        </div>
      </div>
    ),
  },
  {
    id: "memory",
    icon: "💾",
    label: "Memory",
    title: "Auto-Memory & the # Shortcut",
    content: (s) => (
      <div>
        <p style={s.p}>
          Claude Code automatically builds memory as you work. It stores learnings
          in <code style={s.code}>~/.claude/projects/{"<project>"}/memory/MEMORY.md</code> — things
          like build commands it discovered, debugging insights, and your preferences.
          The first 200 lines load into every session automatically.
        </p>
        <Rule s={s} title="The # shortcut">
          Type <code style={s.code}>#</code> followed by a note in Claude Code to instantly save
          something to memory. Example: <code style={s.code}># always use MUI components for new UI</code>.
          Claude figures out which memory file it belongs in (global, project, or local) and writes it for you.
        </Rule>
        <div style={s.grid2}>
          <div style={s.card}>
            <div style={{...s.cardHead, background: "rgba(99,102,241,0.08)", borderColor: "rgba(99,102,241,0.15)"}}>
              <span style={{fontSize:"1.2rem"}}>📋</span>
              <div><div style={s.cardTitle}>CLAUDE.md</div><span style={{fontSize:"0.72rem",color:"#71717a"}}>You write it. Team shares it.</span></div>
            </div>
            <ul style={s.cardList}>
              <li>Explicit, curated instructions</li>
              <li>Committed to git</li>
              <li>Project conventions & architecture</li>
              <li>The "official" source of truth</li>
            </ul>
          </div>
          <div style={s.card}>
            <div style={{...s.cardHead, background: "rgba(234,179,8,0.06)", borderColor: "rgba(234,179,8,0.15)"}}>
              <span style={{fontSize:"1.2rem"}}>🧠</span>
              <div><div style={s.cardTitle}>MEMORY.md</div><span style={{fontSize:"0.72rem",color:"#71717a"}}>Claude writes it. Personal.</span></div>
            </div>
            <ul style={s.cardList}>
              <li>Auto-generated from working sessions</li>
              <li>Never committed — personal to you</li>
              <li>Preferences, patterns, debugging notes</li>
              <li>Claude's "personal notebook"</li>
            </ul>
          </div>
        </div>
      </div>
    ),
  },
  {
    id: "fullstructure",
    icon: "🏗️",
    label: "Full Structure",
    title: "Putting It All Together",
    content: (s) => (
      <div>
        <Code s={s} filename="Complete project structure">{`your-project/
├── CLAUDE.md                    ← Team instructions (committed)
├── CLAUDE.local.md              ← Personal overrides (gitignored)
│
└── .claude/                     ← The control center (commit this!)
    │
    ├── settings.json            ← Permissions, hooks, config (committed)
    ├── settings.local.json      ← Personal permissions (gitignored)
    │
    ├── rules/                   ← Modular instruction files
    │   ├── code-style.md
    │   ├── testing.md
    │   └── api-conventions.md
    │
    ├── skills/                  ← Auto-invoked workflows (preferred)
    │   ├── security-review/
    │   │   ├── SKILL.md
    │   │   └── checklist.md
    │   └── create-migration/
    │       ├── SKILL.md
    │       └── templates/
    │           └── migration.ts
    │
    ├── commands/                ← Manual slash commands (legacy, still works)
    │   ├── fix-issue.md         → /project:fix-issue <number>
    │   └── deploy.md            → /project:deploy
    │
    ├── agents/                  ← Subagent personas
    │   ├── code-reviewer.md
    │   └── security-auditor.md
    │
    └── .mcp.json                ← MCP server integrations


~/.claude/                       ← Global / personal (never committed)
├── CLAUDE.md                    ← Cross-project preferences
├── skills/                      ← Skills available everywhere
├── commands/                    ← Commands available everywhere
├── keybindings.json             ← Custom keyboard shortcuts
└── projects/
    └── <project-hash>/
        └── memory/
            └── MEMORY.md        ← Auto-generated session memory`}</Code>
        <Rule s={s} title="The setup sequence for a new project">
          <strong>1.</strong> Run <code style={s.code}>/init</code> to generate a starter CLAUDE.md
          <br/><strong>2.</strong> Delete everything Claude can infer from code — aim for under 200 lines
          <br/><strong>3.</strong> Set up <code style={s.code}>.claude/settings.json</code> with permissions and a formatter hook
          <br/><strong>4.</strong> Add rules/ files only when CLAUDE.md gets too long (50+ lines on one topic)
          <br/><strong>5.</strong> Create skills/ as you discover repeatable workflows
          <br/><strong>6.</strong> Add agents/ when you need isolated, specialized reviewers
          <br/><strong>7.</strong> Commit <code style={s.code}>.claude/</code> to git. Add settings.local.json and CLAUDE.local.md to .gitignore
        </Rule>
        <Callout s={s} icon="🔒" title="Security note">
          Treat <code style={s.code}>.claude/</code> with the same scrutiny as package.json scripts
          when opening untrusted repos. Malicious skills or hooks could execute arbitrary commands.
          Review before opening any unfamiliar project that includes a .claude/ directory.
        </Callout>
      </div>
    ),
  },
];

/* ═══════════════════════════════════════════════════════
   DATA: Migration Prompts
   ═══════════════════════════════════════════════════════ */
const PROMPTS = {
  audit: {
    label: "Audit & Upgrade",
    icon: "🔍",
    desc: () => <><strong style={{color:"#c7d2fe"}}>Single project.</strong> Scans your .claude/ setup, finds stale rules, proposes migrations (commands→skills, rules extraction, hook setup), executes only after approval. Run from the project root.</>,
    filename: "Paste into Claude Code inside a project",
    prompt: `# Request: Audit & Upgrade My Claude Code Configuration

## Phase 1: Full Inventory

Scan this project and report back with a structured inventory. Don't change anything yet.

### Config files
Find and list every governance/instruction file:
- CLAUDE.md (root and any subdirectories)
- CLAUDE.local.md
- .claude/ directory contents (settings.json, settings.local.json, commands/, skills/, agents/, rules/, .mcp.json)
- Any legacy files: .cursorrules, .github/copilot-instructions.md, AGENTS.md, .clinerules, CONVENTIONS.md

For each file found, give me:
- Path
- Line count
- One-sentence summary of what it covers
- Last modified date (from git log if available)
- Issues: stale info, contradictions, duplicated rules, things your linter already handles

### Memory files
Check ~/.claude/projects/ for any auto-memory related to this project. Summarize what's there.

### Migration candidates
- List any .claude/commands/*.md files that should become skills/ (they need bundled scripts, auto-invocation, or tool restrictions)
- List any CLAUDE.md rules that should be extracted to .claude/rules/ (50+ lines on a single topic)
- List any CLAUDE.md style rules that should become hooks instead (formatting, linting, import sorting)

## Phase 2: Recommendations

Based on the inventory, propose a specific upgrade plan. Organize it as:

### 🔴 Fix now (broken or harmful)
- Contradictory rules, stale build commands, wrong file paths, security issues

### 🟡 Upgrade (improve quality)
- Commands → Skills migration
- CLAUDE.md bloat → extract to rules/
- Style enforcement → hooks in settings.json
- Missing permissions in settings.json

### 🟢 Add (missing but valuable)
- Hooks not yet configured (formatter, type checker)
- Agents that would help (reviewer, security auditor)
- Skills for workflows you do repeatedly
- Rules files for domains with lots of conventions

### ⚪ Remove (dead weight)
- Rules Claude already follows without being told
- Duplicated instructions across files
- Stale references to removed code/dependencies

Present this plan and **wait for my approval** before making any changes.

## Phase 3: Execute

Once I approve (I may modify the plan), execute the changes in this order:
1. Fix broken/harmful issues first
2. Migrate commands → skills (preserve the old files until confirmed working)
3. Extract rules from CLAUDE.md
4. Add hooks to settings.json
5. Create any new agents/skills
6. Prune CLAUDE.md — delete lines that are now handled by rules/, hooks, or that Claude infers from code
7. Run a final check: read the complete config and flag any remaining contradictions

After all changes, show me a before/after line count comparison for every file touched.`,
  },
  global: {
    label: "Global Config",
    icon: "🏠",
    desc: () => <><strong style={{color:"#c7d2fe"}}>Personal defaults.</strong> Sets up ~/.claude/ with cross-project preferences, global skills, permissions, and keybindings. Inventories what exists before touching anything. Run from any directory.</>,
    filename: "Paste into Claude Code from any directory",
    prompt: `# Request: Set Up My Global Claude Code Configuration

I want to configure my global ~/.claude/ directory with sensible defaults that apply across all my projects. Survey what's already there before changing anything.

## Step 1: Inventory current global config

Check and report on:
- ~/.claude/CLAUDE.md — does it exist? What's in it?
- ~/.claude/settings.json — current permissions and hooks
- ~/.claude/skills/ — any global skills installed?
- ~/.claude/commands/ — any global commands?
- ~/.claude/keybindings.json — custom keybindings?
- ~/.claude/projects/ — list projects with auto-memory, show sizes

Report what you find and note anything that looks stale or misconfigured.

## Step 2: Propose a global setup

Based on what's there (and what's missing), propose:

### ~/.claude/CLAUDE.md (personal cross-project preferences)
Draft a concise file (~30–50 lines) covering:
- My coding style preferences (ask me if you don't know them)
- Default commit message format
- How I like plans presented (file? inline? structured?)
- Any "always do this" rules I've mentioned in past sessions (check memory)

### ~/.claude/settings.json (global permissions)
Propose sensible defaults:
- Safe allow-list for common tools
- Deny-list for dangerous operations (rm -rf, curl to unknown hosts)
- Any global hooks that make sense (like a formatter if I use one consistently)

### Global skills worth having
Suggest 2-3 global skills that are useful in any project:
- A reflection/session-review skill
- A commit skill with conventional commits
- Anything else that fits my workflow

### Keybindings
If I don't have custom keybindings, suggest useful ones.

Present the full plan and **wait for my approval** before writing any files.

## Step 3: Execute

Create/update files only after approval. For each file:
- Show me the content before writing
- If updating an existing file, show the diff
- Back up any file being replaced (copy to ~/.claude/backup/)`,
  },
  multi: {
    label: "Sync Repos",
    icon: "🔄",
    desc: () => <><strong style={{color:"#c7d2fe"}}>Multi-repo consistency.</strong> Compares .claude/ configs across projects, finds contradictions and gaps, recommends what should be global vs project-specific. Updates one repo at a time. Run from the parent directory.</>,
    filename: "Paste into Claude Code from your projects parent directory",
    prompt: `# Request: Audit Claude Code Config Across Multiple Projects

I want to make my Claude Code setup consistent across my projects. Help me find inconsistencies and create shared conventions.

## Step 1: Discover projects

Look for git repositories in the current directory (one level deep). For each repo found, scan for:
- CLAUDE.md (root)
- .claude/ directory and its contents
- Any other governance files (.cursorrules, AGENTS.md, etc.)

Create a comparison table:
| Project | CLAUDE.md | settings.json | commands/ | skills/ | agents/ | rules/ | hooks |
Show line counts and ✅/❌ for each.

## Step 2: Find inconsistencies

Across all projects, identify:
- **Contradictions**: Same topic, different rules between projects
- **Gaps**: Things configured in some projects but missing from others
- **Redundancy**: Instructions that should be in global ~/.claude/CLAUDE.md instead of per-project
- **Stale**: References to tools, deps, or patterns that no longer exist in that project

## Step 3: Recommend

Propose a plan to harmonize:
1. What should move to global config (shared across all)
2. What should stay project-specific (unique to each)
3. What should be added to projects that are missing it
4. What should be removed everywhere

**Wait for my approval before making any changes.**

## Step 4: Execute

After approval, update each project one at a time:
- Show the project name before each batch of changes
- Show diffs for every file modification
- After each project, pause and let me confirm before moving to the next`,
  },
};

/* ═══════════════════════════════════════════════════════
   DATA: Migration Checklist
   ═══════════════════════════════════════════════════════ */
const checklist = [
  { category: "CLAUDE.md Health Check", color: "#818cf8", items: [
    { text: "Run /init and compare output with current file — find gaps", priority: "start" },
    { text: "Delete rules your linter/formatter already enforces", priority: "high" },
    { text: "Delete rules Claude follows correctly without being told", priority: "high" },
    { text: "Verify all build/test/lint commands still work", priority: "high" },
    { text: "Check file paths — do referenced files/dirs still exist?", priority: "high" },
    { text: 'Rephrase "Do not X" as "Prefer Y over X"', priority: "mid" },
    { text: "Extract any 50+ line topic into .claude/rules/", priority: "mid" },
    { text: "Target under 200 lines total", priority: "mid" },
  ]},
  { category: "Commands → Skills Migration", color: "#f59e0b", items: [
    { text: "List all .claude/commands/*.md files", priority: "start" },
    { text: "For each: does it need bundled scripts, auto-invocation, or tool restrictions?", priority: "high" },
    { text: "If yes → create .claude/skills/<name>/SKILL.md with frontmatter", priority: "high" },
    { text: "If no → fine as command, but consider skills/ anyway (future-proof)", priority: "mid" },
    { text: "Add context: fork to skills that shouldn't pollute main context", priority: "mid" },
    { text: "Add allowed-tools to read-only skills (reviewers, analyzers)", priority: "mid" },
    { text: "Keep old command files until new skills confirmed working", priority: "low" },
  ]},
  { category: "settings.json Setup", color: "#22c55e", items: [
    { text: "Add PostToolUse hook for your formatter (Prettier, Biome, Black)", priority: "high" },
    { text: "Add PostToolUse hook for type checking on .ts/.tsx files", priority: "high" },
    { text: "Set deny rules for dangerous operations (rm -rf, curl to unknown hosts)", priority: "high" },
    { text: "Set allow rules for tools Claude needs (git, your package manager)", priority: "mid" },
    { text: "Move personal settings to settings.local.json", priority: "mid" },
    { text: "Add settings.local.json to .gitignore", priority: "mid" },
    { text: "Test that hooks run in <2 seconds (slow hooks kill productivity)", priority: "mid" },
  ]},
  { category: "Global ~/.claude/ Setup", color: "#ec4899", items: [
    { text: "Create ~/.claude/CLAUDE.md with cross-project preferences (30-50 lines)", priority: "high" },
    { text: "Move redundant per-project rules to global CLAUDE.md", priority: "mid" },
    { text: "Set up 2-3 global skills (commit, reflection, research)", priority: "mid" },
    { text: "Review auto-memory in ~/.claude/projects/ — prune stale entries", priority: "low" },
    { text: "Set up keybindings.json if you haven't", priority: "low" },
  ]},
  { category: "Git & Team Hygiene", color: "#06b6d4", items: [
    { text: "Commit .claude/ directory to git", priority: "high" },
    { text: "Add CLAUDE.local.md and .claude/settings.local.json to .gitignore", priority: "high" },
    { text: "Review .claude/ in PRs with same scrutiny as CI config", priority: "mid" },
    { text: "Audit .claude/ before opening untrusted repos", priority: "mid" },
    { text: "Document team's CLAUDE.md conventions in README or contributing guide", priority: "low" },
  ]},
];

const prioStyle = {
  start: { bg: "rgba(129,140,248,0.1)", border: "rgba(129,140,248,0.25)", text: "#a5b4fc", label: "START HERE" },
  high: { bg: "rgba(239,68,68,0.06)", border: "rgba(239,68,68,0.15)", text: "#fca5a5", label: "HIGH" },
  mid: { bg: "rgba(234,179,8,0.06)", border: "rgba(234,179,8,0.15)", text: "#fcd34d", label: "MID" },
  low: { bg: "rgba(34,197,94,0.06)", border: "rgba(34,197,94,0.12)", text: "#86efac", label: "LOW" },
};

/* ═══════════════════════════════════════════════════════
   REUSABLE COMPONENTS
   ═══════════════════════════════════════════════════════ */
function Callout({ s, icon, title, children, variant }) {
  const isWarn = variant === "warn";
  return (
    <div style={{
      background: isWarn ? "rgba(234,179,8,0.04)" : "rgba(99,102,241,0.04)",
      border: `1px solid ${isWarn ? "rgba(234,179,8,0.25)" : "rgba(99,102,241,0.15)"}`,
      borderRadius: 6, padding: "1rem 1.2rem", margin: "1.2rem 0",
    }}>
      <div style={{fontSize:"0.82rem",fontWeight:700,color:"#e4e4e7",marginBottom:"0.4rem"}}>{icon} {title}</div>
      <div style={{fontSize:"0.8rem",lineHeight:1.7,color:"#a1a1aa"}}>{children}</div>
    </div>
  );
}

function Rule({ s, title, children }) {
  return (
    <div style={{background:"#111113",border:"1px solid #27272a",borderLeft:"3px solid #818cf8",borderRadius:"0 6px 6px 0",padding:"1rem 1.2rem",margin:"1.2rem 0"}}>
      <div style={{fontSize:"0.82rem",fontWeight:700,color:"#c7d2fe",marginBottom:"0.5rem"}}>{title}</div>
      <div style={{fontSize:"0.8rem",lineHeight:1.75,color:"#a1a1aa",margin:0}}>{children}</div>
    </div>
  );
}

function Code({ s, filename, children }) {
  return (
    <div style={{background:"#0c0c0d",border:"1px solid #1e1e22",borderRadius:8,overflow:"hidden",margin:"1.2rem 0"}}>
      <div style={{display:"flex",alignItems:"center",gap:"0.4rem",padding:"0.55rem 1rem",borderBottom:"1px solid #1e1e22",background:"#111113"}}>
        <span style={{width:8,height:8,borderRadius:"50%",background:"#27272a"}}/>
        <span style={{width:8,height:8,borderRadius:"50%",background:"#27272a"}}/>
        <span style={{width:8,height:8,borderRadius:"50%",background:"#27272a"}}/>
        <span style={{fontSize:"0.68rem",color:"#52525b",marginLeft:"0.5rem",fontFamily:"'IBM Plex Mono',monospace"}}>{filename}</span>
      </div>
      <pre style={{padding:"1rem",margin:0,fontSize:"0.74rem",lineHeight:1.7,color:"#a1a1aa",fontFamily:"'IBM Plex Mono','Fira Code',monospace",overflowX:"auto",whiteSpace:"pre"}}>{children}</pre>
    </div>
  );
}

function TipBox({ s, variant, title, children }) {
  const isGood = variant === "good";
  return (
    <div style={{
      background: isGood ? "rgba(34,197,94,0.04)" : "rgba(239,68,68,0.04)",
      border: `1px solid ${isGood ? "rgba(34,197,94,0.12)" : "rgba(239,68,68,0.12)"}`,
      borderRadius: 8, padding: "1rem",
    }}>
      <div style={{fontSize:"0.78rem",fontWeight:700,color:"#e4e4e7",marginBottom:"0.5rem"}}>{title}</div>
      <ul style={{listStyle:"none",padding:0,margin:0,fontSize:"0.78rem",lineHeight:1.8,color:"#a1a1aa"}}>{children}</ul>
    </div>
  );
}

/* ═══════════════════════════════════════════════════════
   SHARED STYLES
   ═══════════════════════════════════════════════════════ */
const S = {
  p: { fontSize:"0.87rem", lineHeight:1.75, color:"#d4d4d8", margin:"0 0 1.2rem" },
  code: { background:"rgba(99,102,241,0.1)", border:"1px solid rgba(99,102,241,0.15)", padding:"0.1rem 0.4rem", borderRadius:3, fontSize:"0.77rem", fontFamily:"'IBM Plex Mono',monospace", color:"#c7d2fe" },
  grid2: { display:"grid", gridTemplateColumns:"1fr 1fr", gap:"1rem", margin:"1.2rem 0" },
  card: { background:"#111113", borderRadius:8, border:"1px solid #1e1e22", overflow:"hidden" },
  cardHead: { display:"flex", alignItems:"center", gap:"0.7rem", padding:"0.8rem 1rem", borderBottom:"1px solid #1e1e22" },
  cardTitle: { fontSize:"0.84rem", fontWeight:700, color:"#fafafa" },
  cardList: { listStyle:"none", padding:"0.8rem 1rem", margin:0, fontSize:"0.79rem", lineHeight:1.8, color:"#a1a1aa" },
};

/* ═══════════════════════════════════════════════════════
   MAIN APP
   ═══════════════════════════════════════════════════════ */
export default function ClaudeCodeGuide() {
  const [mode, setMode] = useState("reference");
  const [refActive, setRefActive] = useState("overview");
  const [upgradeTab, setUpgradeTab] = useState("prompts");
  const [activePrompt, setActivePrompt] = useState("audit");
  const [copied, setCopied] = useState(false);
  const [checked, setChecked] = useState({});

  const activeRef = refSections.find((s) => s.id === refActive);
  const totalItems = checklist.reduce((a, c) => a + c.items.length, 0);
  const checkedCount = Object.values(checked).filter(Boolean).length;

  const handleCopy = async (text) => {
    try { await navigator.clipboard.writeText(text); } catch {
      const ta = document.createElement("textarea"); ta.value = text;
      document.body.appendChild(ta); ta.select(); document.execCommand("copy"); document.body.removeChild(ta);
    }
    setCopied(true); setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div style={{ minHeight:"100vh", background:"#0a0a0b", color:"#d4d4d8", fontFamily:"'IBM Plex Sans',-apple-system,sans-serif" }}>
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600;700&display=swap');
        *{box-sizing:border-box}
        code{font-family:'IBM Plex Mono',monospace}
        ul li::before{content:"→ ";color:#52525b}
        ::-webkit-scrollbar{width:6px;height:6px}
        ::-webkit-scrollbar-track{background:transparent}
        ::-webkit-scrollbar-thumb{background:#27272a;border-radius:3px}
        .check-item{transition:opacity .2s}.check-item.done{opacity:.45}.check-item.done .ct{text-decoration:line-through}
        @media(max-width:800px){
          .main-layout{flex-direction:column!important}
          .ref-sidebar{flex-direction:row!important;overflow-x:auto!important;border-right:none!important;border-bottom:1px solid #1e1e22!important;width:100%!important;min-width:0!important;padding:.5rem!important}
          .ref-sidebar button{white-space:nowrap!important;padding:.45rem .7rem!important;font-size:.7rem!important}
          .ref-content{padding:1.5rem 1rem!important}
          .g2{grid-template-columns:1fr!important}
        }
      `}</style>

      <div style={{ maxWidth:1100, margin:"0 auto", borderLeft:"1px solid #1e1e22", borderRight:"1px solid #1e1e22", minHeight:"100vh" }}>
        {/* ── HEADER ── */}
        <div style={{ padding:"1.5rem 2rem 1.25rem", borderBottom:"1px solid #1e1e22" }}>
          <div style={{ display:"flex", alignItems:"center", justifyContent:"space-between", flexWrap:"wrap", gap:"0.75rem" }}>
            <div>
              <div style={{ display:"inline-block", fontSize:"0.58rem", fontWeight:600, letterSpacing:"0.14em", textTransform:"uppercase", color:"#818cf8", background:"rgba(129,140,248,0.08)", border:"1px solid rgba(129,140,248,0.15)", padding:"0.2rem 0.6rem", borderRadius:3, marginBottom:"0.6rem", fontFamily:"'IBM Plex Mono',monospace" }}>
                Claude Code Companion
              </div>
              <h1 style={{ fontSize:"1.45rem", fontWeight:700, color:"#fafafa", margin:"0.3rem 0 0.2rem", lineHeight:1.2 }}>
                {mode === "reference" ? "Anatomy of a Claude Code Project" : "Upgrade Existing Projects"}
              </h1>
              <p style={{ fontSize:"0.8rem", color:"#71717a", margin:0 }}>
                {mode === "reference"
                  ? "How to structure .claude/ so it's scalable, team-friendly, and useful long-term."
                  : "Copy-paste prompts for Claude Code + an interactive migration checklist."}
              </p>
            </div>

            {/* Mode toggle */}
            <div style={{ display:"flex", gap:"0.2rem", background:"#111113", padding:"0.25rem", borderRadius:7, border:"1px solid #1e1e22" }}>
              {[
                { id: "reference", label: "📖 Reference", sub: "Learn" },
                { id: "upgrade", label: "🔧 Upgrade", sub: "Migrate" },
              ].map((m) => (
                <button key={m.id} onClick={() => setMode(m.id)} style={{
                  padding:"0.5rem 1rem", background: mode===m.id ? "rgba(129,140,248,0.08)" : "transparent",
                  border:`1px solid ${mode===m.id ? "rgba(129,140,248,0.15)" : "transparent"}`, borderRadius:5,
                  color: mode===m.id ? "#c7d2fe" : "#52525b", fontSize:"0.78rem", fontWeight: mode===m.id ? 600 : 400,
                  cursor:"pointer", fontFamily:"'IBM Plex Sans',sans-serif", transition:"all .15s",
                }}>
                  {m.label}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* ════════════════ REFERENCE MODE ════════════════ */}
        {mode === "reference" && (
          <div className="main-layout" style={{ display:"flex", minHeight:"calc(100vh - 130px)" }}>
            <div className="ref-sidebar" style={{ display:"flex", flexDirection:"column", gap:"0.12rem", padding:"0.7rem", minWidth:180, borderRight:"1px solid #1e1e22", background:"#09090a" }}>
              {refSections.map((sec) => (
                <button key={sec.id} onClick={() => setRefActive(sec.id)} style={{
                  display:"flex", alignItems:"center", gap:"0.55rem", padding:"0.5rem 0.7rem",
                  background: refActive===sec.id ? "rgba(129,140,248,0.08)" : "transparent",
                  border:`1px solid ${refActive===sec.id ? "rgba(129,140,248,0.15)" : "transparent"}`,
                  borderRadius:6, color: refActive===sec.id ? "#c7d2fe" : "#71717a",
                  fontSize:"0.77rem", fontWeight: refActive===sec.id ? 600 : 400,
                  fontFamily:"'IBM Plex Sans',sans-serif", cursor:"pointer", textAlign:"left", transition:"all .15s",
                }}>
                  <span style={{fontSize:"0.85rem",width:18,textAlign:"center"}}>{sec.icon}</span>{sec.label}
                </button>
              ))}

              {/* Quick link to Upgrade */}
              <div style={{ marginTop:"auto", paddingTop:"0.5rem", borderTop:"1px solid #1e1e22" }}>
                <button onClick={() => setMode("upgrade")} style={{
                  display:"flex", alignItems:"center", gap:"0.55rem", padding:"0.5rem 0.7rem", width:"100%",
                  background:"rgba(245,158,11,0.05)", border:"1px solid rgba(245,158,11,0.12)",
                  borderRadius:6, color:"#fcd34d", fontSize:"0.72rem", fontWeight:500,
                  cursor:"pointer", fontFamily:"'IBM Plex Sans',sans-serif", textAlign:"left",
                }}>
                  🔧 Upgrade existing projects →
                </button>
              </div>
            </div>

            <div className="ref-content" style={{ flex:1, padding:"1.75rem 2.25rem", overflowY:"auto", maxHeight:"calc(100vh - 130px)" }}>
              <h2 style={{ fontSize:"1.15rem", fontWeight:700, color:"#fafafa", margin:"0 0 1.2rem" }}>{activeRef?.title}</h2>
              {activeRef?.content(S)}
            </div>
          </div>
        )}

        {/* ════════════════ UPGRADE MODE ════════════════ */}
        {mode === "upgrade" && (
          <div style={{ padding:"1.5rem 2rem", overflowY:"auto", maxHeight:"calc(100vh - 130px)" }}>
            {/* Sub-tabs */}
            <div style={{ display:"flex", gap:"0.25rem", marginBottom:"1.5rem", background:"#111113", padding:"0.25rem", borderRadius:7, border:"1px solid #1e1e22" }}>
              {[
                { id:"prompts", label:"📋 Copy-Paste Prompts", sub:"3 prompts for Claude Code" },
                { id:"checklist", label:"✅ Migration Checklist", sub:`${checkedCount}/${totalItems} done` },
              ].map((t) => (
                <button key={t.id} onClick={() => setUpgradeTab(t.id)} style={{
                  flex:1, padding:"0.6rem 1rem", textAlign:"left",
                  background: upgradeTab===t.id ? "rgba(129,140,248,0.08)" : "transparent",
                  border:`1px solid ${upgradeTab===t.id ? "rgba(129,140,248,0.15)" : "transparent"}`,
                  borderRadius:5, color: upgradeTab===t.id ? "#c7d2fe" : "#71717a",
                  fontSize:"0.8rem", fontWeight: upgradeTab===t.id ? 600 : 400,
                  cursor:"pointer", fontFamily:"'IBM Plex Sans',sans-serif", transition:"all .15s",
                }}>
                  {t.label}
                  <span style={{ display:"block", fontSize:"0.66rem", color: upgradeTab===t.id ? "#818cf8" : "#3f3f46", marginTop:"0.1rem" }}>{t.sub}</span>
                </button>
              ))}
            </div>

            {/* ── PROMPTS TAB ── */}
            {upgradeTab === "prompts" && (
              <div style={{ maxWidth:820 }}>
                <div style={{ display:"flex", gap:"0.4rem", marginBottom:"1rem" }}>
                  {Object.entries(PROMPTS).map(([k, p]) => (
                    <button key={k} onClick={() => setActivePrompt(k)} style={{
                      padding:"0.5rem 0.9rem", background: activePrompt===k ? "#18181b" : "transparent",
                      border:`1px solid ${activePrompt===k ? "#27272a" : "#1e1e22"}`, borderRadius:6,
                      color: activePrompt===k ? "#fafafa" : "#71717a", fontSize:"0.77rem",
                      fontWeight: activePrompt===k ? 600 : 400, cursor:"pointer",
                      fontFamily:"'IBM Plex Sans',sans-serif", transition:"all .15s",
                    }}>
                      {p.icon} {p.label}
                    </button>
                  ))}
                </div>

                <div style={{ background:"rgba(99,102,241,0.04)", border:"1px solid rgba(99,102,241,0.12)", borderRadius:6, padding:"0.8rem 1rem", marginBottom:"1rem", fontSize:"0.78rem", color:"#a1a1aa", lineHeight:1.6 }}>
                  {PROMPTS[activePrompt].desc()}
                </div>

                <button onClick={() => handleCopy(PROMPTS[activePrompt].prompt)} style={{
                  display:"flex", alignItems:"center", gap:"0.5rem", marginBottom:"1rem", padding:"0.55rem 1.1rem",
                  background: copied ? "rgba(74,222,128,0.08)" : "rgba(129,140,248,0.08)",
                  border:`1px solid ${copied ? "rgba(74,222,128,0.2)" : "rgba(129,140,248,0.2)"}`,
                  color: copied ? "#4ade80" : "#a5b4fc", fontFamily:"'IBM Plex Mono',monospace",
                  fontSize:"0.77rem", fontWeight:600, borderRadius:5, cursor:"pointer", transition:"all .2s",
                }}>
                  {copied ? (
                    <><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round"><polyline points="20 6 9 17 4 12"/></svg>Copied</>
                  ) : (
                    <><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>Copy prompt</>
                  )}
                </button>

                <div style={{ background:"#0c0c0d", border:"1px solid #1e1e22", borderRadius:8, overflow:"hidden" }}>
                  <div style={{ display:"flex", alignItems:"center", gap:"0.4rem", padding:"0.5rem 1rem", borderBottom:"1px solid #1e1e22", background:"#111113" }}>
                    <span style={{width:8,height:8,borderRadius:"50%",background:"#27272a"}}/>
                    <span style={{width:8,height:8,borderRadius:"50%",background:"#27272a"}}/>
                    <span style={{width:8,height:8,borderRadius:"50%",background:"#27272a"}}/>
                    <span style={{fontSize:"0.66rem",color:"#52525b",marginLeft:"0.5rem",fontFamily:"'IBM Plex Mono',monospace"}}>{PROMPTS[activePrompt].filename}</span>
                  </div>
                  <pre style={{ padding:"1.1rem", margin:0, fontSize:"0.72rem", lineHeight:1.7, color:"#8b8b96", fontFamily:"'IBM Plex Mono',monospace", overflowX:"auto", whiteSpace:"pre-wrap", wordBreak:"break-word", maxHeight:460, overflowY:"auto" }}>
                    {PROMPTS[activePrompt].prompt}
                  </pre>
                </div>
              </div>
            )}

            {/* ── CHECKLIST TAB ── */}
            {upgradeTab === "checklist" && (
              <div style={{ maxWidth:820 }}>
                {/* Progress */}
                <div style={{ background:"#111113", border:"1px solid #1e1e22", borderRadius:8, padding:"0.9rem 1.1rem", marginBottom:"1.4rem" }}>
                  <div style={{ display:"flex", justifyContent:"space-between", alignItems:"center", marginBottom:"0.5rem" }}>
                    <span style={{fontSize:"0.8rem",fontWeight:600,color:"#e4e4e7"}}>Migration Progress</span>
                    <span style={{ fontSize:"0.74rem", fontFamily:"'IBM Plex Mono',monospace", color: checkedCount===totalItems ? "#4ade80" : "#71717a" }}>
                      {checkedCount}/{totalItems}{checkedCount===totalItems && " ✨"}
                    </span>
                  </div>
                  <div style={{height:5,background:"#1e1e22",borderRadius:3,overflow:"hidden"}}>
                    <div style={{ height:"100%", width:`${(checkedCount/totalItems)*100}%`, background: checkedCount===totalItems ? "linear-gradient(90deg,#22c55e,#4ade80)" : "linear-gradient(90deg,#818cf8,#a78bfa)", borderRadius:3, transition:"width .3s" }}/>
                  </div>
                </div>

                {checklist.map((cat, ci) => {
                  const catDone = cat.items.filter((_,i) => checked[`${ci}-${i}`]).length;
                  return (
                    <div key={ci} style={{ marginBottom:"1.4rem" }}>
                      <div style={{ display:"flex", alignItems:"center", gap:"0.6rem", marginBottom:"0.65rem" }}>
                        <div style={{width:4,height:18,borderRadius:2,background:cat.color}}/>
                        <span style={{fontSize:"0.85rem",fontWeight:700,color:"#fafafa"}}>{cat.category}</span>
                        <span style={{fontSize:"0.68rem",fontFamily:"'IBM Plex Mono',monospace",color:"#52525b",marginLeft:"auto"}}>{catDone}/{cat.items.length}</span>
                      </div>
                      <div style={{ display:"flex", flexDirection:"column", gap:"0.3rem" }}>
                        {cat.items.map((item, ii) => {
                          const k = `${ci}-${ii}`, done = checked[k], ps = prioStyle[item.priority];
                          return (
                            <div key={ii} className={`check-item ${done?"done":""}`} onClick={() => setChecked(p => ({...p,[k]:!p[k]}))} style={{
                              display:"flex", alignItems:"flex-start", gap:"0.7rem", padding:"0.6rem 0.8rem",
                              background: done ? "#0c0c0d" : "#111113", border:"1px solid #1e1e22",
                              borderRadius:6, cursor:"pointer", transition:"all .15s",
                            }}>
                              <div style={{
                                width:17, height:17, borderRadius:4, flexShrink:0, marginTop:1,
                                border:`1.5px solid ${done ? "#4ade80" : "#3f3f46"}`,
                                background: done ? "rgba(74,222,128,0.1)" : "transparent",
                                display:"flex", alignItems:"center", justifyContent:"center", transition:"all .15s",
                              }}>
                                {done && <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="#4ade80" strokeWidth="3" strokeLinecap="round"><polyline points="20 6 9 17 4 12"/></svg>}
                              </div>
                              <span className="ct" style={{ flex:1, fontSize:"0.77rem", color: done ? "#52525b" : "#d4d4d8", lineHeight:1.5 }}>{item.text}</span>
                              <span style={{
                                fontSize:"0.56rem", fontWeight:700, fontFamily:"'IBM Plex Mono',monospace",
                                letterSpacing:"0.06em", color: done ? "#3f3f46" : ps.text,
                                background: done ? "transparent" : ps.bg, border:`1px solid ${done ? "transparent" : ps.border}`,
                                padding:"0.13rem 0.4rem", borderRadius:3, flexShrink:0, whiteSpace:"nowrap",
                              }}>{ps.label}</span>
                            </div>
                          );
                        })}
                      </div>
                    </div>
                  );
                })}
                {checkedCount > 0 && (
                  <button onClick={() => setChecked({})} style={{
                    padding:"0.45rem 0.9rem", background:"transparent", border:"1px solid #27272a",
                    borderRadius:5, color:"#52525b", fontSize:"0.7rem", cursor:"pointer",
                    fontFamily:"'IBM Plex Mono',monospace",
                  }}>Reset checklist</button>
                )}
              </div>
            )}

            {/* Quick link back to Reference */}
            <div style={{ marginTop:"2rem", paddingTop:"1rem", borderTop:"1px solid #1e1e22" }}>
              <button onClick={() => setMode("reference")} style={{
                padding:"0.5rem 1rem", background:"rgba(129,140,248,0.05)", border:"1px solid rgba(129,140,248,0.12)",
                borderRadius:6, color:"#a5b4fc", fontSize:"0.74rem", cursor:"pointer",
                fontFamily:"'IBM Plex Sans',sans-serif",
              }}>
                ← Back to Reference Guide
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
