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
The first nine numbered sections each contain 1–2 news items (headline + 2–3 sentence
summary + source link) **plus an "In Practice" learning bite**:
`Equinix · Google · Competitors · DC Infrastructure · AI & Compute Demand · New AI
Models & Releases · Networking · Backend / Cloud & Data · Program & PM`.
"In Practice" appears in every section every day (generated teaching content; vary the
topic daily so it compounds). All source links open in a new tab.

Every new edition also ends with Section 10, `PgPM Growth`. Use the project-local
`$build-pgpm-growth` skill to create it. It teaches two connected topics that advance
Robert's professional development as a PgPM at Equinix in the data-center industry,
contains exactly six researched links (three per topic), and ends with one safe,
time-boxed `Daily Action`. This section is a progressive curriculum, not a news category.

### Google section
- Place `Google` directly after `Equinix` in every new edition, beginning July 29, 2026.
- Include 1–2 current stories plus a role-specific "In Practice" learning bite.
- Check Google Cloud Press Corner (`https://www.googlecloudpresscorner.com/`), Google
  Data Centers latest news (`https://datacenters.google/discover-more/latest-news/`),
  and the Google Cloud Blog latest-news page
  (`https://cloud.google.com/blog/topics/inside-google-cloud/whats-new-google-cloud`).
  Also check independent reporting such as Reuters and Data Center Dynamics.
- Cover Google corporate infrastructure, Google Cloud/GCP, data centers, power and
  cooling, TPU/AI infrastructure, outages, partnerships, regions, and material platform
  releases.
- Keep pure Gemini model launches in `New AI Models & Releases`; use `Google` when the
  important angle is GCP deployment, infrastructure, operations, or business impact.
- Do not repeat the same Google story in another section.

### Crusoe monitoring
- Check Crusoe's homepage, newsroom, and resource pages during every daily research
  pass, together with general web searches for independent coverage.
- Use independent reporting such as Reuters, AP, Data Center Dynamics, Bloomberg,
  TechRadar, ITPro, and other credible outlets. Prefer independent confirmation for
  material capacity, financing, customer, schedule, and reliability claims.
- Route Crusoe coverage by its primary angle: strategy, financing, partnerships,
  market position, or pipeline to `Competitors`; campuses, construction, power, UPS,
  cooling, batteries, manufacturing, or commissioning to `DC Infrastructure`;
  contracted capacity, GPU deployments, hyperscaler demand, or AI-factory growth to
  `AI & Compute Demand`; Crusoe Cloud and developer services to `Backend / Cloud &
  Data`; and cluster networking or edge connectivity to `Networking`.
- Do not add a dedicated Crusoe section or repeat one Crusoe story across sections.

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
The user starts the workflow in Codex by asking to run today's brief. `AGENTS.md` is the
authoritative workflow source; this file remains for legacy compatibility. Codex reviews
recent editions, researches the nine news sections, invokes `$build-pgpm-growth` for
Section 10, writes a dated markdown brief to `briefs/`, renders and validates
`index.html`, and commits/pushes the content-only
edition to `main`. Manual workflow or structure changes use a branch and PR.

## Roadmap / not yet
- Archive/back-issues index page linking dated editions.
- Optional table of contents + per-section jump links.
- Optional email delivery (Gmail) and/or GitHub Actions cloud publishing for a
  guaranteed morning send independent of my Mac being awake.
