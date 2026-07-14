# DC Daily Brief — Project Rules

## What this is
A personal, no-backend **static newsletter** ("my morning newspaper") that aggregates
data center, AI, networking, backend/cloud, and project-management news + daily learning
into one well-designed page, regenerated automatically each morning and hosted on GitHub
Pages. It serves double duty: stay current on my industry, and study/learn (I'm a data
center ops engineer at Equinix moving into program/project management, targeting PMP).

## Golden rules (project hygiene)
- **This repo lives at `~/repos/dc-daily-brief`, OUTSIDE iCloud/OneDrive.** Never move a
  git repo into a cloud-sync folder — it corrupts `.git`.
- One project = one folder = one git repo. Never run `git` from `~` or a parent of
  multiple projects.
- Keep the site **self-contained and no-backend**: static HTML/CSS, no server, no build
  step required to view.

## Version control workflow
- **`main` is always deployable** (GitHub Pages serves it).
- **The daily automated brief commits straight to `main`** (the scheduled task can't
  review its own PR). These are content-only commits.
- **Every manual change** (structure, styling, features, docs) goes through:
  1. `git switch -c <type>/<short-desc>` off `main`  (types: `feat`, `fix`, `docs`, `chore`, `style`)
  2. commit (small, focused commits)
  3. `git push -u origin <branch>` → open a **PR** → review → **merge to `main`** → delete branch
- Commit messages: imperative subject line; end AI-assisted commits with the standard
  `Co-Authored-By` trailer.

## Content structure (each daily edition)
Numbered sections, each = 1–2 news items (headline + 2–3 sentence summary + source link)
**plus an "In Practice" learning bite**:
`Equinix · Competitors · DC Infrastructure · AI & Compute Demand · New AI Models &
Releases · Networking · Backend / Cloud & Data · Program & PM`.
"In Practice" appears in every section every day (generated teaching content; vary the
topic daily so it compounds). All source links open in a new tab.

## Design system (editorial newsletter)
- **Layout:** single centered column, ~760px, newspaper masthead + dateline + numbered
  sections + "In Practice" callout boxes + footer. Responsive (phone-first reading).
- **Type:** `Fraunces` (masthead/headlines, serif), `Newsreader` (body, serif),
  `JetBrains Mono` (kickers, labels, source tags, meta).
- **Palette:** light "newsprint" default + automatic dark mode via
  `prefers-color-scheme`. Single teal accent (`#0F766E` light / `#5FD3C4` dark) for
  kickers, links, and In Practice boxes. Keep it calm and readable — the content is the
  star, not chrome.
- Reuse the CSS variables already defined in `index.html`; don't hardcode new hex values.

## How it's generated
The generator is the Claude Code scheduled task
`~/.claude/scheduled-tasks/daily-industry-brief/SKILL.md` (runs ~7am local while the app
is open). It writes a dated markdown brief to `briefs/`, renders `index.html`, and
commits/pushes to `main`. Editing the *look/structure* = edit `index.html` here (on a
branch). Editing *what content is gathered* = edit that SKILL.md.

## Roadmap / not yet
- Archive/back-issues index page linking dated editions.
- Optional table of contents + per-section jump links.
- Optional email delivery (Gmail) and/or GitHub Actions cloud publishing for a
  guaranteed morning send independent of my Mac being awake.
