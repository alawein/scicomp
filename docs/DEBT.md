---
type: canonical
source: none
sla: on-change
last_updated: "2026-06-06"
audience: [ai-agents, contributors]
---

# Technical Debt Ledger

The accumulated cost of deliberate shortcuts. The goal is not zero debt, it is
zero untracked debt. Anything recorded here was a conscious choice with a known
fix. Add entries with `/debt-log`. Remove an entry when the debt is paid (note it
in the PR).

<!-- New entries are appended below, newest first. Format:

### <short title>
- **Date:** YYYY-MM-DD
- **Where:** <file/module/path>
- **What:** the shortcut and why the proper fix was not done
- **Risk if left:** what degrades over time
- **Suggested fix:** the path to doing it right
- **Owner:** <from CODEOWNERS or repo-framework ownership>

-->
