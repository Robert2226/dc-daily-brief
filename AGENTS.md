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
calendar-day headlines. Prioritize developments since the previous edition, then select
previously uncovered stories from the last seven calendar days, clearly dated. Quality
and depth take precedence over reading-time targets. Follow the breadth requirements
in EDITORIAL.md before concluding that a category is quiet.

Start directly with the news; do not generate a "Today at a glance" summary.
The nine numbered news sections, in order, are:
`Equinix · Google · Incidents, Reliability & Remediation · DC Infrastructure · DCOS, DCIM, BMS & Controls ·
AI & Compute Demand · New AI Models & Releases · Networking · Backend / Cloud & Data`.
Program & PM is no longer a news section; professional development remains in PgPM Growth.
Each has 1–2 worthwhile stories plus an In Practice learning bite. When
fresh reporting is thin, select useful analysis or a deployment case study with its
actual date. Only after documented broader research finds nothing worthwhile, use a
compact honest note; do not default to a “no new news” headline. Use multiple
purposeful source links as needed; external links open in a new tab.

New editions dated September 20, 2026 onward use format 3 with
`news_profile: "lean-v1"`; September 19 uses `incidents-v1`. Earlier editions retain their original lineup and default
profile; never rewrite their content. One dated source generates separate News and Deep
Dives pages. News has the nine sections above, with short learning bites. Deep Dives has three
subjects: physical infrastructure, logical systems, and PgPM Growth. Each technical
subject contains one 500–800-word lesson, examples and useful sources. Every fourth
expanded edition (counting formats 2 and 3 together, starting September 5) uses one
technical subject for synthesis. Track topics/cases in metadata, not inferred mastery.
Vary mechanisms, examples, comparisons, failure scenarios and judgment.

Invoke the local `$build-pgpm-growth` skill for the third learning subject: two connected
lessons, exactly six researched sources (three per topic), a worked example and one
short optional time-boxed Daily Action. Keep the source heading `PgPM Growth`; it follows
`Physical Deep Dive` and `Logical Deep Dive`. Historical combined editions retain their
original content, section counts and URLs (including format-2 Section 11).

Every page has News | Deep Dives | Archive navigation. Latest routes are `index.html`
and `deep-dives.html`; paired dated routes are `editions/YYYY-MM-DD.html` and
`deep-dives/YYYY-MM-DD.html`. Do not add study links inside News. Deep Dives starts
with the lessons, without duplicate dated links or a subject contents list. Keep the
top News | Deep Dives | Archive navigation. Optional lesson-to-news references must be
genuinely useful; do not force a news connection for PgPM Growth. Historical links remain valid.
The archive labels earlier pages as combined editions.

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
  cooling, TPU/AI infrastructure, partnerships, regions, and material platform
  releases.
- Keep pure Gemini model launches in `New AI Models & Releases`; use `Google` when the
  important angle is GCP deployment, infrastructure, operations, or business impact.
- Route Google incidents to `Incidents, Reliability & Remediation`. Do not repeat the
  same story under `AI & Compute Demand`, `New AI Models & Releases`, or
  `Backend / Cloud & Data`.

### Incidents, Reliability & Remediation
Position three covers significant physical/environmental incidents, service outages,
concrete operational risks, postmortems and remediation across Equinix, Google, AWS,
Azure, other hyperscalers and colo operators. Route incidents here regardless of company;
use short cross-references elsewhere rather than duplicate stories. Exclude minor status
blips and generic risk commentary. Distinguish incident date from publication/update date,
impact, confirmed versus suspected cause, response and unresolved questions. Revisit older
incidents when findings or remediation materially change; label older missed coverage.

Every run must search provider status histories, engineering postmortems, regulators,
local reporting and independent industry sources. Record checks and access gaps in the
research log; a green dashboard is not evidence that the coverage interval was incident-free.
Use relevant incidents in physical, logical and PgPM lessons, separating reported facts
from hypothetical examples and engineering interpretations. Never infer unpublished causes.

Continue broad operator discovery: established colo operators, hyperscalers, regional
developers and emerging AI infrastructure providers. Route worthwhile expansion, financing,
partnership and customer developments to DC Infrastructure, AI & Compute Demand or
Backend / Cloud & Data according to the main development. Crusoe is one input, not the
boundary of research. Do not duplicate stories to fill sections.

### Crusoe monitoring
- Check Crusoe's homepage, newsroom, and resource pages during every daily research
  pass, along with general web searches for independent coverage.
- Use independent reporting such as Reuters, AP, Data Center Dynamics, Bloomberg,
  TechRadar, ITPro, and other credible outlets so coverage is not limited to Crusoe's
  own framing. Prefer independent confirmation for material capacity, financing,
  customer, schedule, and reliability claims.
- Route each Crusoe story by its primary angle: incidents, concrete operational risks and remediation to
  `Incidents, Reliability & Remediation`; campuses, capacity pipeline, related financing,
  construction, power, UPS, cooling, batteries, manufacturing, or commissioning to
  `DC Infrastructure`; contracted capacity, GPU deployments, hyperscaler demand, or
  AI-factory growth to `AI & Compute Demand`; Crusoe Cloud, inference, fine-tuning,
  developer platforms, or managed services to `Backend / Cloud & Data`; and cluster
  networking or edge connectivity to `Networking`.
- Do not add a dedicated Crusoe section and do not repeat the same Crusoe story in
  multiple sections.

## Design system (editorial newsletter)
- **Layout:** single centered column, ~760px, newspaper masthead + dateline + numbered
  sections + "In Practice" callout boxes + footer. Desktop reading is the target;
  retain existing responsive CSS, but do not run mobile/phone-width checks.
- **Type:** `Fraunces` (masthead/headlines, serif), `Newsreader` (body, serif),
  `JetBrains Mono` (kickers, labels, source tags, meta).
- **Palette:** light "newsprint" default + automatic dark mode via
  `prefers-color-scheme`. Single teal accent (`#0F766E` light / `#5FD3C4` dark) for
  kickers, links, and In Practice boxes. Keep it calm and readable — the content is the
  star, not chrome.
- Reuse the CSS variables already defined in `index.html`; don't hardcode new hex values.

## How it's generated
The user asks Codex to run the brief. Read this file, EDITORIAL.md, SOURCES.md, the latest
edition and topic metadata in the manifest; open older content only for relevant duplication checks.
Research all nine categories including the mandatory Google
and Crusoe checks. Record research evidence and access gaps in research/YYYY-MM-DD.md.
Use `$build-pgpm-growth` for the third learning subject, write the dated Markdown with format-3 metadata,
then use the lean validation/publication sequence in EDITORIAL.md. The builder produces the
latest News and Deep Dives pages, paired dated HTML pages, archive, latest.md and stable edition-manifest.json.
Content-only daily runs commit/push directly to main using publish.sh; structure,
styling, workflow, skill and documentation changes use the manual branch/PR process.

## Roadmap / not yet
- Optional topic index beyond the dated archive.
- Optional email delivery or scheduled generation only if explicitly requested later.
