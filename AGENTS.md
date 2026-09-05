# DC Daily Brief — Project Rules

## What this is
A personal, no-backend **static newsletter** ("my morning newspaper") that aggregates
data center, AI, networking, backend/cloud, and project-management news + daily learning
into one well-designed page, regenerated on demand and hosted on GitHub Pages.
It serves double duty: stay current on my industry, and study/learn. I am an established
technical PgPM at Equinix, working across physical facilities, logical systems, and
program delivery.

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

## Content structure (new editions)
Follow [EDITORIAL.md](EDITORIAL.md) for research, Markdown, metadata and validation,
and [SOURCES.md](SOURCES.md) for the expandable research watchlist. Generation is
user-initiated, typically every two days; cover since the previous edition, not just
calendar-day headlines. Quality and depth take precedence over reading-time targets.

Start with three linked takeaways. The ten numbered news sections, in order, are:
`Equinix · Google · Competitors · DC Infrastructure · DCOS, DCIM, BMS & Controls ·
AI & Compute Demand · New AI Models & Releases · Networking · Backend / Cloud & Data ·
Program & PM`. Each has 1–2 worthwhile stories plus an In Practice learning bite. When
research finds no material news, explicitly say so and still teach. Use multiple
purposeful source links as needed; external links open in a new tab.

Include one rotating 500–800-word deep dive within a news section. Every fourth expanded
edition uses a synthesis deep dive. Track topics/cases in edition metadata, not inferred
reader mastery. Vary mechanisms, examples, comparisons, failure scenarios and judgment.

`PgPM Growth` is Section 11, immediately after Program & PM. Invoke the local
`$build-pgpm-growth` skill for two connected lessons, exactly six researched sources
(three per topic), a worked example and one short optional time-boxed Daily Action.
Historical editions keep their original content and section counts.

### DCOS, DCIM, BMS & Controls
DCOS means Data Center Operating System; DCIM means Data Center Infrastructure
Management. Cover their relationship to BMS, SCADA, electrical power monitoring,
historians and local controls without conflating these responsibilities. AVEVA,
Rockwell/FactoryTalk and Emerson are examples, not boundaries. Discover other vendors,
integrators, software and hardware through broad category and vendor searches on every
run. Cover releases, deployments, integration, lifecycle, acquisitions and relevant
security developments. Teach architecture, protocols, alarms, data quality, redundancy,
OT security, commissioning and handover; connect technology to delivery and lifecycle
tradeoffs. Hardware gets lighter coverage unless a development warrants a deep dive.
Do not invent Equinix-specific architecture, instructions or procedures.

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

### Crusoe monitoring
- Check Crusoe's homepage, newsroom, and resource pages during every daily research
  pass, along with general web searches for independent coverage.
- Use independent reporting such as Reuters, AP, Data Center Dynamics, Bloomberg,
  TechRadar, ITPro, and other credible outlets so coverage is not limited to Crusoe's
  own framing. Prefer independent confirmation for material capacity, financing,
  customer, schedule, and reliability claims.
- Route each Crusoe story by its primary angle: company strategy, financing,
  partnerships, market position, or capacity pipeline to `Competitors`; campuses,
  construction, power, UPS, cooling, batteries, manufacturing, or commissioning to
  `DC Infrastructure`; contracted capacity, GPU deployments, hyperscaler demand, or
  AI-factory growth to `AI & Compute Demand`; Crusoe Cloud, inference, fine-tuning,
  developer platforms, or managed services to `Backend / Cloud & Data`; and cluster
  networking or edge connectivity to `Networking`.
- Do not add a dedicated Crusoe section and do not repeat the same Crusoe story in
  multiple sections.

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
The user asks Codex to run the brief. Read this file, EDITORIAL.md, SOURCES.md, recent
editions and the manifest; research all ten categories including the mandatory Google
and Crusoe checks. Record research evidence and access gaps in research/YYYY-MM-DD.md.
Use `$build-pgpm-growth` for Section 11, write the dated Markdown with format-2 metadata,
then run `python3 build.py briefs/YYYY-MM-DD.md` and the tests. The builder produces the
latest homepage, dated HTML archive, latest.md and stable edition-manifest.json.
Content-only daily runs commit/push directly to main using publish.sh; structure,
styling, workflow, skill and documentation changes use the manual branch/PR process.

## Roadmap / not yet
- Optional topic index beyond the dated archive.
- Optional email delivery or scheduled generation only if explicitly requested later.
