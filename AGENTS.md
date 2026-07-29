# DC Daily Brief — Project Rules

## What this is
A personal, no-backend **static newsletter** ("my morning newspaper") that aggregates
data center, AI, networking, backend/cloud, and project-management news + daily learning
into one well-designed page, regenerated on demand each morning and hosted on GitHub
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
- **The user-initiated daily brief commits straight to `main`.** These are content-only
  commits; the user starts each run in Codex.
- **Every manual change** (structure, styling, features, docs) goes through:
  1. `git switch -c <type>/<short-desc>` off `main`  (types: `feat`, `fix`, `docs`, `chore`, `style`)
  2. commit (small, focused commits)
  3. `git push -u origin <branch>` → open a **PR** → review → **merge to `main`** → delete branch
- Commit messages: imperative subject line; end AI-assisted commits with the standard
  `Co-Authored-By` trailer.

## Content structure (each daily edition)
Numbered sections, each = 1–2 news items (headline + 2–3 sentence summary + source link)
**plus an "In Practice" learning bite**:
`Equinix · Google · Competitors · DC Infrastructure · AI & Compute Demand · New AI
Models & Releases · Networking · Backend / Cloud & Data · Program & PM`.
"In Practice" appears in every section every day (generated teaching content; vary the
topic daily so it compounds). All source links open in a new tab.

### Google section
- Place `Google` directly after `Equinix` in every new edition, beginning July 29, 2026.
- Include 1–2 current stories plus a role-specific "In Practice" learning bite.
- Check Google Cloud Press Corner (`https://www.googlecloudpresscorner.com/`), Google
  Data Centers latest news (`https://datacenters.google/discover-more/latest-news/`),
  and the Google Cloud Blog latest-news page
  (`https://cloud.google.com/blog/topics/inside-google-cloud/whats-new-google-cloud`).
  Also check independent reporting such as Reuters and Data Center Dynamics so the
  section is not limited to Google's framing.
- Cover Google corporate infrastructure, Google Cloud/GCP, data centers, power and
  cooling, TPU/AI infrastructure, outages, partnerships, regions, and material platform
  releases.
- Keep pure Gemini model launches in `New AI Models & Releases`; use `Google` when the
  important angle is GCP deployment, infrastructure, operations, or business impact.
- Do not repeat the same Google story under `Competitors`, `AI & Compute Demand`, `New
  AI Models & Releases`, or `Backend / Cloud & Data`.

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
The user starts the workflow in Codex by asking to run today's brief. Codex reads this
file as the workflow source of truth, reviews recent editions to avoid repetition,
researches the nine sections, writes a dated markdown brief to `briefs/`, renders
`index.html`, validates it, and commits/pushes the content-only edition to `main`.
Editing the look or structure remains a manual branch-and-PR change.

## Roadmap / not yet
- Archive/back-issues index page linking dated editions.
- Optional table of contents + per-section jump links.
- Optional email delivery (Gmail) and/or GitHub Actions cloud publishing for a
  guaranteed morning send independent of my Mac being awake.
