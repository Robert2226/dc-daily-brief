#!/usr/bin/env bash
# Build today's edition and publish it. Invoked identically every day (no args,
# no embedded date) so the scheduled task's permission approval is stable and
# "Always allow" actually persists across runs — see CLAUDE.md.
set -euo pipefail
cd "$(dirname "$0")"

DATE="$(date +%F)"
BRIEF="briefs/${DATE}.md"

if [ ! -f "$BRIEF" ]; then
  echo "No brief found at $BRIEF — nothing to publish." >&2
  exit 1
fi

python3 build.py "$BRIEF"
git add -A
git commit -m "brief: ${DATE} edition" -q || echo "Nothing to commit."
git push origin main
git log --oneline -3
