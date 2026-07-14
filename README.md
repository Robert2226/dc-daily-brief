# DC Daily Brief

A personal, auto-generated **morning newspaper** — one aggregated read covering the
data center industry, AI/compute, networking, backend/cloud, and the craft of
project management. Built so I read *one* well-designed brief each morning instead of
scanning a dozen sites, and learn something in every section.

**Live site:** https://robert2226.github.io/dc-daily-brief/

## What it is
- A **no-backend static site** (`index.html`) styled as an editorial newsletter.
- Regenerated automatically every morning by a local scheduled task, which searches
  the day's news, writes the brief, commits, and pushes — GitHub Pages redeploys.
- Each edition has numbered sections, and every section ends with an **"In Practice"**
  learning bite so the brief compounds into real knowledge over time.

## Sections
Equinix · Competitors · DC Infrastructure · AI & Compute Demand · New AI Models &
Releases · Networking · Backend / Cloud & Data · Program & PM — each with an
*In Practice* explainer.

## Structure
```
index.html      # the published newsletter (latest edition)
briefs/         # dated markdown archive of past editions (source of truth)
CLAUDE.md       # project + workflow rules for AI-assisted work
README.md
.gitignore
```

## How it's produced
The generator lives outside this repo, in the Claude Code scheduled task
`~/.claude/scheduled-tasks/daily-industry-brief/SKILL.md`. Each morning it:
1. gathers news (RSS backbone + web search) across the sections,
2. writes a dated markdown brief into `briefs/`,
3. renders `index.html` from it,
4. commits to `main` and pushes → GitHub Pages updates.

## Local preview
```
python3 -m http.server 8091 --directory .
# then open http://localhost:8091/index.html
```

## Contributing (just me, but disciplined)
See [CLAUDE.md](CLAUDE.md). The daily automated brief commits to `main`; every manual
change goes through a branch → PR → merge.
