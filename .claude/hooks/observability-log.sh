#!/usr/bin/env bash
set -e

# =============================================================================
# observability-log.sh — Governance Hook (I-3: Observability)
# Version: 1.1.0
# Source:  knowledge-base/templates/governance-hooks/hooks/observability-log.sh
# =============================================================================
#
# Enforces Invariant I-3 (Observability): every mutation must leave a trace.
# Appends a row to the session log after each commit, recording the timestamp,
# commit message, file count, and approximate lines changed.
#
# Usage:
#   bash observability-log.sh                                    # default log path
#   bash observability-log.sh --log-to docs/operations/session-log.md
#
# Configuration:
#   --log-to <path>  — override the default log file location
#   Default log:       docs/operations/session-log.md
#   LOG_ROTATION_SIZE — set per-project in .claude/hooks/config.env
# =============================================================================

# Source per-project configuration if it exists
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
if [ -f "$SCRIPT_DIR/config.env" ]; then
  # shellcheck source=/dev/null
  source "$SCRIPT_DIR/config.env"
fi

LOG_FILE="docs/operations/session-log.md"

# Parse arguments: support both positional and --log-to flag
while [[ $# -gt 0 ]]; do
  case $1 in
    --log-to)
      LOG_FILE="$2"
      shift 2
      ;;
    *)
      # Treat as positional argument for backward compatibility
      LOG_FILE="$1"
      shift
      ;;
  esac
done

timestamp=$(date '+%Y-%m-%d %H:%M')
commit_sha=$(git log -1 --pretty=%h)
commit_msg=$(git log -1 --pretty=%B)
file_count=$(git diff HEAD~1 --name-only 2>/dev/null | wc -l)
lines_changed=$(git diff HEAD~1 --numstat 2>/dev/null | awk '{sum+=$1+$2} END {print sum+0}')

# Ensure log directory exists
mkdir -p "$(dirname "$LOG_FILE")"

# Initialize log file with header if it doesn't exist
if [ ! -f "$LOG_FILE" ]; then
  echo "# Session Log" > "$LOG_FILE"
  echo "" >> "$LOG_FILE"
  echo "| Timestamp | Commit | Message | Files | Lines Changed |" >> "$LOG_FILE"
  echo "|-----------|--------|---------|-------|---------------|" >> "$LOG_FILE"
fi

# Sanitize commit message (remove pipes to prevent markdown table corruption)
commit_msg=$(echo "$commit_msg" | tr '|' ' ' | head -1)

echo "| $timestamp | $commit_sha | $commit_msg | $file_count files | ~$lines_changed lines |" >> "$LOG_FILE"
