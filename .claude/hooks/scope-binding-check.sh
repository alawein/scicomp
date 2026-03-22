#!/usr/bin/env bash
set -e

# =============================================================================
# scope-binding-check.sh — Governance Hook (I-4: Scope Binding)
# Version: 1.0.0
# Source:  _pkos/templates/governance-hooks/hooks/scope-binding-check.sh
# =============================================================================
#
# Enforces Invariant I-4 (Scope Binding): every commit should represent one
# logical unit of work. Warns (or errors) when a commit touches more files
# than the configured threshold, which often signals scope creep.
#
# Usage:
#   bash scope-binding-check.sh                # strict mode (exit 1 on violation)
#   bash scope-binding-check.sh --warn-only    # warn but allow commit
#
# Configuration:
#   SCOPE_THRESHOLD  — max files before warning (default: 3)
# =============================================================================

SCOPE_THRESHOLD="${SCOPE_THRESHOLD:-3}"
warn_only=${1:-false}

file_count=$(git diff --cached --name-only | wc -l)

if [ "$file_count" -gt "$SCOPE_THRESHOLD" ]; then
  msg="WARNING: About to commit changes to $file_count files (threshold: $SCOPE_THRESHOLD). Verify this is one logical unit, not scope creep (I-4)."
  if [ "$warn_only" = "--warn-only" ]; then
    echo "$msg"
  else
    echo "ERROR: $msg"
    exit 1
  fi
fi
