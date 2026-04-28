#!/usr/bin/env bash
set -e

# =============================================================================
# drift-detection.sh — Governance Hook (I-2: Drift Is Debt)
# Version: 1.1.0
# Source:  knowledge-base/templates/governance-hooks/hooks/drift-detection.sh
# =============================================================================
#
# Enforces Invariant I-2 (Drift Is Debt): governance files in each project
# should stay aligned with the canonical governance templates. Sections marked
# with <!-- CUSTOM OVERRIDE: ... --> are excluded from comparison.
#
# Usage:
#   bash drift-detection.sh                         # auto-detect knowledge-base location
#   bash drift-detection.sh /path/to/template-root  # explicit template source
#
# Checked files: CLAUDE.md, AGENTS.md, GUIDELINES.md
#
# Configuration:
#   DRIFT_CHECK_INTERVAL — set per-project in .claude/hooks/config.env
#   (used by the scheduler/settings.json, not by this script directly)
# =============================================================================

# Source per-project configuration if it exists
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
if [ -f "$SCRIPT_DIR/config.env" ]; then
  # shellcheck source=/dev/null
  source "$SCRIPT_DIR/config.env"
fi

# Default: walk up from .claude/hooks/ to repo root, then to sibling knowledge-base
template_source=${1:-../../../knowledge-base}

# Resolve to absolute path if relative
if [[ ! "$template_source" = /* ]]; then
  template_source="$(cd "$(dirname "$0")" && cd "$template_source" 2>/dev/null && pwd)" || true
fi

drift_found=0

for file in CLAUDE.md AGENTS.md GUIDELINES.md; do
  if [ ! -f "$file" ]; then continue; fi
  if [ ! -f "$template_source/$file" ]; then continue; fi

  # Extract non-custom sections and compare
  grep -v "<!-- CUSTOM OVERRIDE" "$file" > /tmp/"$file".filtered 2>/dev/null || true
  grep -v "<!-- CUSTOM OVERRIDE" "$template_source/$file" > /tmp/"$file".template.filtered 2>/dev/null || true

  if ! diff -q /tmp/"$file".filtered /tmp/"$file".template.filtered > /dev/null 2>&1; then
    echo "DRIFT DETECTED in $file (non-custom sections differ from the template source)"
    echo "  Run: npx kohyr sync-template --dry-run"
    drift_found=1
  fi
done

if [ "$drift_found" -eq 0 ]; then
  echo "No governance drift detected."
fi
