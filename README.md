# DC Daily Brief

A personal, on-demand **morning newspaper** — one aggregated read covering the
data center industry, AI/compute, networking, backend/cloud, and the craft of
project management. Built so I read *one* well-designed brief each morning instead of
scanning a dozen sites, and learn something in every section.

**Live site:** https://robert2226.github.io/dc-daily-brief/

## What it is
- A **no-backend static site** (`index.html`) styled as an editorial newsletter.
- Regenerated when Robert asks Codex to run the day's brief; Codex searches the news,
  writes the edition, commits, and pushes — GitHub Pages redeploys.
- Each edition has numbered sections, and every section ends with an **"In Practice"**
  learning bite so the brief compounds into real knowledge over time.

## Sections
Equinix · Google · Competitors · DC Infrastructure · AI & Compute Demand · New AI
Models & Releases · Networking · Backend / Cloud & Data · Program & PM — each with an
*In Practice* explainer. Google is always section 2 and covers Google Cloud/GCP, Google
data centers, infrastructure, operations, partnerships, regions, and material platform
news.

## Structure
```
index.html      # the published newsletter (latest edition)
briefs/         # dated markdown archive of past editions (source of truth)
AGENTS.md       # authoritative Codex workflow and project rules
CLAUDE.md       # legacy-compatible copy of the project rules
README.md
.gitignore
```

## How it's produced
Robert initiates the workflow in Codex by asking it to run today's brief. Codex follows
the repository's `AGENTS.md` instructions and:
1. gathers news across the nine sections,
2. writes a dated markdown brief into `briefs/`,
3. renders `index.html` from it,
4. commits to `main` and pushes → GitHub Pages updates.

## Local preview
```
python3 -m http.server 8091 --directory .
# then open http://localhost:8091/index.html
```

## Contributing (just me, but disciplined)
See [AGENTS.md](AGENTS.md). The user-initiated daily content brief commits to `main`;
every manual workflow, documentation, design, or feature change goes through a branch →
PR → merge.
