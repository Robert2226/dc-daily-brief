# Editorial and generation guide

## Reader and intent
Robert is an established technical PgPM at Equinix: a full-stack data-center person
across physical facilities, logical systems, and program delivery. Teach technical
mechanisms and business/leadership judgment together. Do not assume internal Equinix
architectures or processes. PMP preparation is optional until Robert confirms its
current importance. Quality and depth matter more than a fixed reading time.

## Every on-demand run
1. Read AGENTS.md, this guide, SOURCES.md, the latest edition, the last 30 editions'
   learning topics, and edition-manifest.json. The manifest tracks teaching, not mastery.
2. Cover the previous edition's date through today's local date, inclusive: the
   previous run's exact research cutoff may be unknown. Deduplicate already covered
   stories; use the boundary-day overlap to catch later announcements. Record both
   publication and event dates where they differ. Also search the last seven calendar
   days (today plus six preceding dates) for worthwhile stories not previously covered.
   Label their actual dates; older useful reading is explicitly analysis or a case study.
3. Search the public web and read accessible newsrooms, release notes, technical
   publications, and independent reporting for all ten news categories. Search broad
   categories as well as named vendors, discovering players beyond the watchlist.
   Check all three Google sources and Crusoe homepage, newsroom and resource/blog
   pages each run. Research runs with the user request; no scheduled scraper or backend.
4. Open candidate source pages and verify the actual claims, dates, status (announced,
   preview, available, planned), and units. Search snippets alone are discovery aids.
   Independent articles repeating one original report are not separate confirmation.
   Use company-claim attribution where appropriate. Never fabricate a link or date.
5. Keep a concise research/YYYY-MM-DD.md log: queries, sources checked, selected
   stories, publication/event dates, duplication decisions, resource-to-lesson mapping,
   and access gaps. Do not copy full source articles. If inaccessible sources leave a
   material gap, explain it in the affected section; do not infer no news from failure.
6. Write briefs/YYYY-MM-DD.md using the format below. Preserve ten news sections in
   the AGENTS.md order, each with 1–2 worthwhile stories and one In Practice bite.
   Use the research breadth gate below before accepting a quiet section.
   More links are useful only when they add evidence, a perspective, or understanding.
7. Start directly with news; do not write opening takeaways or "Today at a glance".
   Put long learning on
   the separate Deep Dives page: exactly three subjects, physical, logical and PgPM.
   Each technical subject gets one 500–800-word deep dive with concrete examples and
   sources. Vary subjects each run based on prior coverage. Every fourth expanded
   edition (formats 2 and 3 together, starting September 5) marks one technical subject
   `synthesis: true`, explicitly revisiting earlier concepts. Recall answers are optional.
8. Invoke $build-pgpm-growth for the third subject. Keep two connected lessons, exactly
   six researched external links (three per lesson), a worked example and one optional
   time-boxed Daily Action. Link all three subjects to relevant news and news back to
   those subjects. Do not duplicate the news summary inside a lesson.
9. Run `python3 build.py briefs/YYYY-MM-DD.md` and `python3 -m unittest discover -s tests`.
   Validation checks structure and internal destinations, not factual truth. Inspect
   both latest pages, paired dates, archive, historical pages, desktop presentation,
   keyboard navigation and recall. Content-only publishing uses `./publish.sh YYYY-MM-DD`
   from main. Do not run mobile/phone-width checks; Robert reads on desktop.
   Structural launches include their full launch edition in the manual PR.

## Research breadth gate
For every category, run at least three distinct discovery angles: topic/mechanism,
companies/customers, and development types (deployments, releases, outages, financing,
standards, acquisitions or delivery case studies). Include searches without literal
calendar-date strings; apply recency filters and verify dates on the underlying pages.
Inspect relevant articles across multiple publishers, combining specialist/independent
reporting with primary announcements, filings, customer accounts and technical material.
Expand synonyms and regional coverage when the first pass returns duplicates or little
of value. Newsroom indexes and search snippets are discovery, not completed reporting.

Build a candidate pool before choosing the one or two items for each category. Record
queries/angles, candidates, publication/event dates, selected/rejected reasons, duplication
checks and access gaps. Syndicated copies count as one underlying report. Add productive
new sources to the watchlist through the manual-change workflow, not a content-only push.

Prefer news since the last run, then uncovered news from the seven-day window, then
clearly dated useful analysis or a case study that explains its relevance to Robert.
Do not substitute generic learning because the first searches were thin. “No new news”
is not a default story. Only after broader research finds nothing worthwhile, retain a
compact honest note and the short practice bite; never invent freshness or pad a quota.
Research depth is an editorial review, not something renderer tests can establish.

## Incident coverage and routing
The third section is **Incidents, Reliability & Remediation** beginning September 19.
Search provider status histories (AWS, Google Cloud and Azure explicitly), engineering
postmortems, regulator notices, local reporting and independent industry coverage every
run. Log the history interval checked, candidate events, material updates, negative
checks and access gaps. Check older open incidents for substantive findings or corrective
actions; present event dates and update dates separately. Do not infer an incident-free
period from a currently green dashboard or an inaccessible history.

Select consequential physical/environmental events, service outages, specific operational
risks and remediation. Exclude minor status blips and generic risk commentary. Every
incident story states impact, the source/status of causal claims, response, and unresolved
questions. A company's preliminary explanation is not a regulator's final finding; service
restoration is not proof that recurrence prevention or environmental cleanup is complete.
All operators' incidents belong here, including Equinix and Google. Cross-reference rather
than duplicate. Broad operator discovery continues, routing expansion/customer/financing
stories to Infrastructure, AI Demand or Cloud by main development.

When pertinent, use sourced incidents in all three learning subjects. Label reported facts,
engineering interpretations and hypothetical examples distinctly. Do not infer an unpublished
root cause or internal Equinix design. Teach mechanisms and judgment, not speculative blame.

## Writing
Each story explains what changed and why it matters. Include a mechanism or concrete
example where useful. Vary learning bites among comparisons, calculations, architecture,
failure scenarios, and leadership judgment; avoid a daily succession of ownership and
acceptance checklists. Define unfamiliar acronyms on first use. Link continuing stories
back to earlier coverage in prose where practical; source URLs remain direct links.
Use plain paragraphs and purposeful sources, not uniform word quotas for every story.
Hardware coverage in controls is normally light, but deserves depth when consequential.

## Supported Markdown (no raw HTML)
The title and coverage line retain their historical format. Add one single-line JSON
metadata comment. `coverage_start` is the previous edition date; `coverage_end` matches
the filename. `topics` and `pgpm_topics` describe what was taught, not completed study.
`research_log` is the relative path to the corresponding research record. The first
expanded edition (September 5, format 2) begins the four-edition synthesis cycle.
New sources use `format: 3`. Editions dated September 19, 2026 onward must also set
`news_profile: "incidents-v1"`, replacing Competitors with Incidents, Reliability &
Remediation in position three. Earlier sources without a profile keep their historical
lineup. Validation, section navigation and `news:` destinations follow the edition profile;
use `news:incidents-reliability-remediation` for the new section. The September 6 example
below illustrates the historical profile and must not be copied without adding the new
profile for a current edition. Metadata `subjects` must contain three ordered entries with
unique slug `id`, `track` (physical/logical/pgpm), and reader-facing `title`. The optional
`synthesis: true` belongs on one technical subject. Format 2 remains readable unchanged.

```markdown
# DC Daily Brief — Sunday, September 6, 2026
_Covers September 5–6, 2026; since the previous edition._
<!-- edition: {"format":3,"coverage_start":"2026-09-05","coverage_end":"2026-09-06","subjects":[{"id":"cooling-capacity","track":"physical","title":"Physical · Cooling capacity"},{"id":"telemetry-replay","track":"logical","title":"Logical · Telemetry replay"},{"id":"pilot-to-fleet","track":"pgpm","title":"PgPM Growth · Pilot to fleet"}],"topics":["Cooling capacity","Telemetry replay"],"pgpm_topics":["Representative pilots — leadership","Progressive rollouts — leadership"],"case":"Hypothetical Hall A","research_log":"research/2026-09-06.md"} -->

```

New editions dated September 20, 2026 onward omit opening takeaways. Historical dated
editions retain them; the latest homepage omits them even when showing an older edition.
Normal sections use:

```markdown
## DCOS, DCIM, BMS & Controls
- **Story headline** — Published September 4, 2026. Summary and interpretation. [Announcement](https://example.org/release) [Independent analysis](https://example.org/analysis)

Context paragraphs support **bold**, *italic*, and [inline links](https://example.org).

> **In Practice · A concrete lesson.** Explain the mechanism or use a worked example.

[Study the relevant lesson](learn:telemetry-replay)

## Physical Deep Dive
:::deep-dive Cooling capacity
Write the first technical lesson here (500–800 words plus purposeful sources).
[Related infrastructure news](news:dc-infrastructure)
:::

## Logical Deep Dive
:::deep-dive Telemetry replay
### Follow a delayed measurement
Write the second 500–800-word lesson. Add sources and a fenced diagram if helpful.
[Related controls story](news:dcos-dcim-bms-controls)
:::

:::recall If the supervisory server fails, must the local controller stop?
Revealable answer explaining the failure behavior.
:::
```

Only `deep-dive` and `recall` containers are supported; close each with `:::` and do
not nest them. Fenced code renders as escaped text, not executable diagrams. Bullets,
headings, and plain paragraphs are retained. External links open in a new tab; fragment
links remain in the page. Use `learn:subject-id` from news and `news:section-slug`
from learning for paired-date cross-links. These resolve to dated pages and stay in the
same tab. Historical news takeaways use `#section-slug`. Each technical source section contains
exactly one deep-dive block; PgPM Growth follows both technical sections using its skill.
The three source sections become three numbered subjects on the learning page. No raw HTML, scripts, or executable URL schemes are accepted.

## Archive and numbering
`build.py` renders all dated sources to editions/YYYY-MM-DD.html. Format-3 sources also
produce deep-dives/YYYY-MM-DD.html. The newest source supplies index.html and latest.md;
the newest split edition supplies deep-dives.html. One issue number covers both pages.
Top navigation opens latest News, latest Deep Dives or Archive. Matching-edition links
and story/lesson links stay on the same date. Learning previous/next links traverse
only split editions; news previous/next links traverse all dates. Historical combined
content retains its URL and is labeled in the archive. When building only legacy sources,
the learning landing page explains that earlier learning lives in combined editions.

The manifest assigns issue numbers once; keep it in version control. Backfills never
renumber published editions. All documents, subject contracts and generated internal
paths/anchors are validated before output is written. External links require manual
source review. Use `--output-dir /tmp/brief-preview` for isolated output. No build is
needed to read HTML; Google Fonts have local fallbacks. Publishing stages both latest
pages and both dated directories while refusing unrelated structural edits.
