#!/usr/bin/env bash
# Publish a researched, user-initiated content edition from main.
set -euo pipefail
cd "$(dirname "$0")"
BRIEF_DATE="${1:-$(date +%F)}"
if [ "$#" -gt 0 ]; then shift; fi
BRIEF="briefs/${BRIEF_DATE}.md"
if [[ ! "$BRIEF_DATE" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]] || [ ! -f "$BRIEF" ]; then
  echo "Provide an existing dated brief (YYYY-MM-DD)." >&2
  exit 1
fi
if [ "$(git branch --show-current)" != main ]; then
  echo "Routine publishing runs from main." >&2
  exit 1
fi
if ! git diff --cached --quiet; then
  echo "Review and clear existing staged changes before publishing an edition." >&2
  exit 1
fi
# Related changes must be explicitly named; never sweep unrelated edits into the batch.
python3 - "$BRIEF_DATE" "$@" <<'PY'
import subprocess, sys
from pathlib import Path
allowed = {'index.html', 'deep-dives.html', 'latest.md', 'archive.html', 'edition-manifest.json',
           f'briefs/{sys.argv[1]}.md', f'research/{sys.argv[1]}.md'}
for name in sys.argv[2:]:
    path = Path(name)
    if path.is_absolute() or '..' in path.parts or '.git' in path.parts or not path.is_file() or path.is_symlink():
        sys.exit('Reviewed extras must be existing relative project files: ' + name)
    allowed.add(path.as_posix())
paths = subprocess.check_output(['git', 'diff', '--name-only', '-z']).decode().split('\0')
paths += subprocess.check_output(['git', 'ls-files', '--others', '--exclude-standard', '-z']).decode().split('\0')
bad = [p for p in paths if p and p not in allowed and not (p.startswith(('editions/', 'deep-dives/')) and p.endswith('.html'))]
if bad:
    sys.exit('Unreviewed non-edition changes: ' + ', '.join(bad))
latest = max(Path('briefs').glob('????-??-??.md')).stem
if sys.argv[1] != latest:
    sys.exit('Publish the newest dated edition; homepage never moves backward.')
PY
python3 build.py "$BRIEF"
python3 -m unittest discover -s tests
git diff --check
paths=("$BRIEF" index.html deep-dives.html latest.md archive.html edition-manifest.json editions)
paths+=("$@")
if [ -d deep-dives ]; then paths+=(deep-dives); fi
if [ -f "research/${BRIEF_DATE}.md" ]; then paths+=("research/${BRIEF_DATE}.md"); fi
git add -- "${paths[@]}"
if ! git diff --cached --quiet; then
  git commit -m "Publish ${BRIEF_DATE} daily brief" -m "Co-Authored-By: OpenAI Codex <noreply@openai.com>"
fi
git push origin main
