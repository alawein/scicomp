import { useState } from "react";

const SUPERPROMPT = `# Claude Code Setup & Upgrade — Superprompt

> Attached: claude-code-guide.jsx — use it as your reference for all .claude/ structure decisions.

## Context

I'm running Claude Code from PowerShell on Windows. Before doing anything, orient yourself:

1. Print my current working directory
2. Confirm this is a git repository (or tell me if it isn't)
3. If I'm in a system directory (like System32, Program Files, Windows, etc.), STOP and tell me to \`cd\` into my actual project directory first — never write config to system paths

## Your Mission

Act as my Claude Code infrastructure architect. You have three jobs, executed in order. Complete each phase fully before moving to the next. **Never write or modify files without my explicit approval.**

---

## PHASE 1: Discovery & Audit

### 1A. Project-Level Scan
Find and inventory every governance/instruction file in this project:
- CLAUDE.md (root + any subdirectories)
- CLAUDE.local.md
- .claude/ directory and ALL contents (settings.json, settings.local.json, commands/, skills/, agents/, rules/, hooks, .mcp.json)
- Legacy files: .cursorrules, .github/copilot-instructions.md, AGENTS.md, .clinerules, CONVENTIONS.md

For each file found, report:
| File | Lines | Summary | Last Modified | Issues |
Flag: stale info, contradictions, duplicated rules, things a linter already handles, wrong file paths, references to removed dependencies.

### 1B. Global Scan
Check my global config at ~/.claude/ (on Windows: %USERPROFILE%\\.claude\\):
- CLAUDE.md — exists? contents?
- settings.json — current permissions/hooks?
- skills/ — any global skills?
- commands/ — any global commands?
- keybindings.json — custom keybindings?
- projects/ — list projects with auto-memory, note stale ones

### 1C. Gap Analysis
Using the attached claude-code-guide.jsx as your reference for ideal structure, identify:

**🔴 Broken or harmful** — contradictory rules, stale commands, security issues, wrong paths
**🟡 Upgrade candidates:**
  - .claude/commands/*.md files that should migrate to skills/ (need bundled scripts, auto-invocation, or tool restrictions)
  - CLAUDE.md sections over 50 lines on one topic → extract to .claude/rules/
  - Style rules in CLAUDE.md that should be hooks instead (formatting, linting, import sorting)
  - Missing permissions or deny rules in settings.json
**🟢 Missing but valuable** — hooks, agents, skills, rules files that would help based on this project's stack
**⚪ Dead weight** — rules Claude already follows, duplicated instructions, stale references

Present Phase 1 findings as a structured report. Then STOP and wait for my input.

---

## PHASE 2: Plan

Based on my feedback on Phase 1, create a concrete execution plan covering:

### Project-Level Changes
1. **CLAUDE.md** — proposed content (aim for <200 lines, only what Claude can't infer from code)
   - Use "Prefer X over Y" phrasing, not "Do not Y"
   - Include: build/test/lint commands, architecture overview, hard rules
   - Exclude: anything the linter handles, generic advice, personal preferences
2. **settings.json** — proposed permissions (allow/deny) and hooks
   - PostToolUse hook for formatter (detect which one this project uses)
   - PostToolUse hook for type checking if TypeScript
   - Deny list for dangerous operations
3. **.claude/rules/** — proposed modular rule files (only if CLAUDE.md topics need depth)
4. **.claude/skills/** — proposed skills for repeatable workflows (with frontmatter)
   - Add \`context: fork\` for skills that shouldn't pollute main context
   - Add \`allowed-tools\` for read-only skills
5. **.claude/agents/** — proposed subagents if this project benefits from isolated reviewers
6. **Commands → Skills migration** — for any existing commands that should upgrade
7. **.gitignore additions** — CLAUDE.local.md, .claude/settings.local.json

### Global Changes (if needed)
1. **~/.claude/CLAUDE.md** — cross-project preferences (30-50 lines)
2. **Global skills** — 2-3 universally useful skills (commit, reflection, etc.)
3. **Stale memory cleanup** — prune dead projects from ~/.claude/projects/

### Execution Order
Number every change. Group them as:
- Phase 2A: Fix broken/harmful issues
- Phase 2B: Migrate commands → skills
- Phase 2C: Extract rules, add hooks
- Phase 2D: Create new agents/skills
- Phase 2E: Prune CLAUDE.md
- Phase 2F: Global config updates
- Phase 2G: Git hygiene (.gitignore, commit .claude/)

For each change, show me the EXACT content that will be written. Show diffs for modifications.

Present the full plan. Then STOP and wait for my approval. I may modify items before you proceed.

---

## PHASE 3: Execute

After I approve (with any modifications):

1. Execute changes in the approved order
2. After each file write/modification, confirm what was done
3. After all project-level changes: re-read the complete config and flag any remaining contradictions
4. Show a before/after comparison:
   | File | Before (lines) | After (lines) | Action |
5. After all global changes: confirm what was written to ~/.claude/
6. Final verification: run a quick sanity check
   - Can Claude find the build command?
   - Do all referenced file paths exist?
   - Are there any contradictions between CLAUDE.md and rules/?
   - Is settings.json valid JSON?

---

## Guiding Principles (from the attached reference)

- **CLAUDE.md is built through deletion, not addition.** Start with /init output and subtract.
- **Only include what Claude cannot infer from reading code.** If the linter enforces it, use a hook.
- **commands/ and skills/ have merged.** New workflows go in skills/. Existing commands still work.
- **Skills are directories, not files.** Each has a SKILL.md + optional scripts/templates.
- **Agents define WHO, skills define WHAT.** A skill can reference an agent via frontmatter.
- **settings.json hooks must be fast (<2s).** Slow hooks kill productivity.
- **Treat .claude/ like CI config.** Commit it, review it in PRs, audit it in untrusted repos.
- **Global ~/.claude/ is for personal defaults.** Never committed, applies to all projects.
- **CLAUDE.local.md and settings.local.json are gitignored.** Personal overrides go here.
- **Target <200 lines per CLAUDE.md file.** Extract depth into rules/.
- **Phrase rules as "Prefer X over Y" not "Do not Y."** Claude respects positive framing more.`;

export default function SuperPrompt() {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(SUPERPROMPT);
    } catch {
      const ta = document.createElement("textarea");
      ta.value = SUPERPROMPT;
      document.body.appendChild(ta);
      ta.select();
      document.execCommand("copy");
      document.body.removeChild(ta);
    }
    setCopied(true);
    setTimeout(() => setCopied(false), 2500);
  };

  /* ── Parsed display ── */
  const lines = SUPERPROMPT.split("\n");

  const renderLine = (line, i) => {
    const trimmed = line.trimStart();
    const indent = line.length - trimmed.length;

    // Main title
    if (trimmed.startsWith("# ") && !trimmed.startsWith("## ") && !trimmed.startsWith("### ")) {
      return <div key={i} style={{ fontSize: "1.15rem", fontWeight: 700, color: "#fafafa", margin: "0 0 0.25rem", lineHeight: 1.3 }}>{trimmed.slice(2)}</div>;
    }
    // Blockquote
    if (trimmed.startsWith("> ")) {
      return (
        <div key={i} style={{
          background: "rgba(129,140,248,0.06)", border: "1px solid rgba(129,140,248,0.12)",
          borderLeft: "3px solid #818cf8", borderRadius: "0 5px 5px 0",
          padding: "0.6rem 0.9rem", margin: "0.5rem 0 1rem", fontSize: "0.77rem",
          color: "#a5b4fc", fontStyle: "italic", lineHeight: 1.6,
        }}>
          {trimmed.slice(2)}
        </div>
      );
    }
    // Phase headers (## PHASE)
    if (trimmed.startsWith("## PHASE")) {
      return (
        <div key={i} style={{
          fontSize: "0.95rem", fontWeight: 700, color: "#fafafa",
          margin: "1.75rem 0 0.5rem", padding: "0.65rem 0.9rem",
          background: "rgba(129,140,248,0.06)", border: "1px solid rgba(129,140,248,0.12)",
          borderRadius: 6, letterSpacing: "0.01em",
        }}>
          {trimmed.slice(3)}
        </div>
      );
    }
    // H2
    if (trimmed.startsWith("## ")) {
      return <div key={i} style={{ fontSize: "0.92rem", fontWeight: 700, color: "#e4e4e7", margin: "1.5rem 0 0.35rem" }}>{trimmed.slice(3)}</div>;
    }
    // H3
    if (trimmed.startsWith("### ")) {
      return <div key={i} style={{ fontSize: "0.82rem", fontWeight: 600, color: "#c084fc", margin: "1rem 0 0.25rem" }}>{trimmed.slice(4)}</div>;
    }
    // Horizontal rule
    if (trimmed === "---") {
      return <hr key={i} style={{ border: "none", borderTop: "1px solid #1e1e22", margin: "0.75rem 0" }} />;
    }
    // Table header
    if (trimmed.startsWith("| ") && trimmed.includes(" | ")) {
      return (
        <div key={i} style={{
          fontFamily: "'IBM Plex Mono',monospace", fontSize: "0.7rem",
          color: "#71717a", background: "#111113", padding: "0.35rem 0.7rem",
          borderRadius: 4, margin: "0.3rem 0", border: "1px solid #1e1e22",
          overflowX: "auto", whiteSpace: "nowrap",
        }}>
          {trimmed}
        </div>
      );
    }
    // Colored severity items
    if (trimmed.startsWith("**🔴")) {
      return <div key={i} style={{ fontSize: "0.77rem", color: "#fca5a5", fontWeight: 600, margin: "0.5rem 0 0.15rem", paddingLeft: indent > 0 ? "0.5rem" : 0 }}>{renderInline(trimmed)}</div>;
    }
    if (trimmed.startsWith("**🟡")) {
      return <div key={i} style={{ fontSize: "0.77rem", color: "#fcd34d", fontWeight: 600, margin: "0.5rem 0 0.15rem", paddingLeft: indent > 0 ? "0.5rem" : 0 }}>{renderInline(trimmed)}</div>;
    }
    if (trimmed.startsWith("**🟢")) {
      return <div key={i} style={{ fontSize: "0.77rem", color: "#86efac", fontWeight: 600, margin: "0.5rem 0 0.15rem", paddingLeft: indent > 0 ? "0.5rem" : 0 }}>{renderInline(trimmed)}</div>;
    }
    if (trimmed.startsWith("**⚪")) {
      return <div key={i} style={{ fontSize: "0.77rem", color: "#a1a1aa", fontWeight: 600, margin: "0.5rem 0 0.15rem", paddingLeft: indent > 0 ? "0.5rem" : 0 }}>{renderInline(trimmed)}</div>;
    }
    // Numbered items
    if (/^\d+\./.test(trimmed)) {
      const num = trimmed.match(/^(\d+)\./)[1];
      const rest = trimmed.slice(num.length + 1).trim();
      return (
        <div key={i} style={{ display: "flex", gap: "0.5rem", fontSize: "0.77rem", lineHeight: 1.7, color: "#a1a1aa", margin: "0.15rem 0", paddingLeft: indent > 2 ? "1rem" : 0 }}>
          <span style={{ color: "#818cf8", fontWeight: 600, fontFamily: "'IBM Plex Mono',monospace", flexShrink: 0, fontSize: "0.72rem" }}>{num}.</span>
          <span>{renderInline(rest)}</span>
        </div>
      );
    }
    // Bullet items
    if (trimmed.startsWith("- ")) {
      return (
        <div key={i} style={{ display: "flex", gap: "0.5rem", fontSize: "0.77rem", lineHeight: 1.7, color: "#a1a1aa", margin: "0.1rem 0", paddingLeft: indent > 2 ? Math.min(indent * 0.3, 2) + "rem" : "0.3rem" }}>
          <span style={{ color: "#3f3f46", flexShrink: 0 }}>—</span>
          <span>{renderInline(trimmed.slice(2))}</span>
        </div>
      );
    }
    // Empty line
    if (trimmed === "") return <div key={i} style={{ height: "0.4rem" }} />;
    // Default paragraph
    return <div key={i} style={{ fontSize: "0.77rem", lineHeight: 1.7, color: "#a1a1aa", margin: "0.1rem 0", paddingLeft: indent > 2 ? "0.5rem" : 0 }}>{renderInline(trimmed)}</div>;
  };

  const renderInline = (text) => {
    // Handle **bold**, `code`, and *italic*
    const parts = [];
    let remaining = text;
    let key = 0;
    while (remaining.length > 0) {
      // Bold
      const boldMatch = remaining.match(/\*\*(.+?)\*\*/);
      // Code
      const codeMatch = remaining.match(/`(.+?)`/);
      // Find earliest match
      const matches = [
        boldMatch ? { type: "bold", index: boldMatch.index, len: boldMatch[0].length, content: boldMatch[1] } : null,
        codeMatch ? { type: "code", index: codeMatch.index, len: codeMatch[0].length, content: codeMatch[1] } : null,
      ].filter(Boolean).sort((a, b) => a.index - b.index);

      if (matches.length === 0) {
        parts.push(<span key={key++}>{remaining}</span>);
        break;
      }

      const m = matches[0];
      if (m.index > 0) parts.push(<span key={key++}>{remaining.slice(0, m.index)}</span>);

      if (m.type === "bold") {
        parts.push(<strong key={key++} style={{ color: "#e4e4e7", fontWeight: 600 }}>{m.content}</strong>);
      } else {
        parts.push(
          <code key={key++} style={{
            background: "rgba(99,102,241,0.1)", border: "1px solid rgba(99,102,241,0.12)",
            padding: "0.05rem 0.3rem", borderRadius: 3, fontSize: "0.72rem",
            fontFamily: "'IBM Plex Mono',monospace", color: "#c7d2fe",
          }}>{m.content}</code>
        );
      }
      remaining = remaining.slice(m.index + m.len);
    }
    return parts;
  };

  return (
    <div style={{
      minHeight: "100vh", background: "#0a0a0b", color: "#d4d4d8",
      fontFamily: "'IBM Plex Sans',-apple-system,sans-serif",
    }}>
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600;700&display=swap');
        *{box-sizing:border-box}
        code{font-family:'IBM Plex Mono',monospace}
        ::-webkit-scrollbar{width:6px}
        ::-webkit-scrollbar-track{background:transparent}
        ::-webkit-scrollbar-thumb{background:#27272a;border-radius:3px}
      `}</style>

      <div style={{ maxWidth: 820, margin: "0 auto", padding: "2rem 1.5rem" }}>
        {/* Header */}
        <div style={{ marginBottom: "1.75rem", paddingBottom: "1.25rem", borderBottom: "1px solid #1e1e22" }}>
          <div style={{
            display: "inline-block", fontSize: "0.58rem", fontWeight: 600,
            letterSpacing: "0.14em", textTransform: "uppercase", color: "#f59e0b",
            background: "rgba(245,158,11,0.08)", border: "1px solid rgba(245,158,11,0.15)",
            padding: "0.2rem 0.6rem", borderRadius: 3, marginBottom: "0.6rem",
            fontFamily: "'IBM Plex Mono',monospace",
          }}>
            Superprompt
          </div>
          <h1 style={{ fontSize: "1.45rem", fontWeight: 700, color: "#fafafa", margin: "0.4rem 0 0.3rem" }}>
            Claude Code Setup & Upgrade
          </h1>
          <p style={{ fontSize: "0.82rem", color: "#71717a", margin: 0, lineHeight: 1.55 }}>
            Copy this prompt, attach the <code style={{
              background: "rgba(99,102,241,0.1)", border: "1px solid rgba(99,102,241,0.12)",
              padding: "0.05rem 0.35rem", borderRadius: 3, fontSize: "0.76rem",
              fontFamily: "'IBM Plex Mono',monospace", color: "#c7d2fe",
            }}>claude-code-guide.jsx</code> file as context, and paste into Claude Code from your project directory.
          </p>
        </div>

        {/* Warning */}
        <div style={{
          background: "rgba(239,68,68,0.04)", border: "1px solid rgba(239,68,68,0.15)",
          borderLeft: "3px solid #ef4444", borderRadius: "0 6px 6px 0",
          padding: "0.85rem 1.1rem", marginBottom: "1.5rem",
        }}>
          <div style={{ fontSize: "0.8rem", fontWeight: 700, color: "#fca5a5", marginBottom: "0.3rem" }}>
            ⚠️ Don't run this from System32 or any system directory
          </div>
          <div style={{ fontSize: "0.76rem", color: "#a1a1aa", lineHeight: 1.65 }}>
            <code style={{
              background: "rgba(239,68,68,0.08)", padding: "0.05rem 0.3rem", borderRadius: 3,
              fontSize: "0.72rem", fontFamily: "'IBM Plex Mono',monospace", color: "#fca5a5",
            }}>cd</code> into your actual project folder first. The prompt includes a safety check — Claude Code will refuse to write config into system paths. Store the JSX reference file somewhere sensible like <code style={{
              background: "rgba(99,102,241,0.08)", padding: "0.05rem 0.3rem", borderRadius: 3,
              fontSize: "0.72rem", fontFamily: "'IBM Plex Mono',monospace", color: "#c7d2fe",
            }}>%USERPROFILE%\\Documents\\claude-references\\</code>
          </div>
        </div>

        {/* Usage steps */}
        <div style={{
          background: "#111113", border: "1px solid #1e1e22", borderRadius: 8,
          padding: "1rem 1.2rem", marginBottom: "1.5rem",
        }}>
          <div style={{ fontSize: "0.8rem", fontWeight: 700, color: "#e4e4e7", marginBottom: "0.6rem" }}>How to use</div>
          {[
            { num: "1", text: "Open PowerShell and cd into your project directory" },
            { num: "2", text: "Launch Claude Code with: claude" },
            { num: "3", text: "Attach the claude-code-guide.jsx file for reference context" },
            { num: "4", text: "Paste this superprompt and hit Enter" },
            { num: "5", text: "Review Phase 1 findings, then approve Phase 2 plan, then watch Phase 3 execute" },
          ].map((step) => (
            <div key={step.num} style={{ display: "flex", gap: "0.6rem", alignItems: "flex-start", margin: "0.25rem 0" }}>
              <span style={{
                fontSize: "0.65rem", fontWeight: 700, color: "#818cf8", fontFamily: "'IBM Plex Mono',monospace",
                background: "rgba(129,140,248,0.1)", borderRadius: 4, padding: "0.1rem 0.4rem", flexShrink: 0,
              }}>{step.num}</span>
              <span style={{ fontSize: "0.77rem", color: "#a1a1aa", lineHeight: 1.5 }}>{step.text}</span>
            </div>
          ))}
        </div>

        {/* Copy button */}
        <button onClick={handleCopy} style={{
          display: "flex", alignItems: "center", gap: "0.5rem",
          marginBottom: "1.25rem", padding: "0.65rem 1.3rem",
          background: copied ? "rgba(74,222,128,0.08)" : "rgba(245,158,11,0.08)",
          border: `1px solid ${copied ? "rgba(74,222,128,0.2)" : "rgba(245,158,11,0.2)"}`,
          color: copied ? "#4ade80" : "#fcd34d",
          fontFamily: "'IBM Plex Mono',monospace", fontSize: "0.8rem", fontWeight: 600,
          borderRadius: 5, cursor: "pointer", transition: "all .2s",
        }}>
          {copied ? (
            <><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round"><polyline points="20 6 9 17 4 12"/></svg>Copied to clipboard</>
          ) : (
            <><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>Copy superprompt</>
          )}
        </button>

        {/* Rendered prompt */}
        <div style={{
          background: "#0c0c0d", border: "1px solid #1e1e22", borderRadius: 8,
          overflow: "hidden",
        }}>
          <div style={{
            display: "flex", alignItems: "center", gap: "0.4rem",
            padding: "0.55rem 1rem", borderBottom: "1px solid #1e1e22", background: "#111113",
          }}>
            <span style={{width:8,height:8,borderRadius:"50%",background:"#27272a"}}/>
            <span style={{width:8,height:8,borderRadius:"50%",background:"#27272a"}}/>
            <span style={{width:8,height:8,borderRadius:"50%",background:"#27272a"}}/>
            <span style={{ fontSize:"0.66rem", color:"#52525b", marginLeft:"0.5rem", fontFamily:"'IBM Plex Mono',monospace" }}>
              superprompt — paste into Claude Code
            </span>
          </div>
          <div style={{ padding: "1.25rem 1.5rem", maxHeight: 600, overflowY: "auto" }}>
            {lines.map((line, i) => renderLine(line, i))}
          </div>
        </div>
      </div>
    </div>
  );
}
