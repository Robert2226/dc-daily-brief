# Editorial and generation guide

## Reader and intent
Robert is an established technical PgPM at Equinix: a full-stack data-center person
across physical facilities, logical systems, and program delivery. Teach technical
mechanisms and business/leadership judgment together. Do not assume internal Equinix
architectures or processes. PMP preparation is optional until Robert confirms its
current importance. Quality and depth matter more than a fixed reading time.

## Every on-demand run
1. Read AGENTS.md, this guide, SOURCES.md, the latest edition, and the last 30 editions'
   topic metadata in edition-manifest.json. Open older lessons only when a proposed
   topic overlaps and its action or sources need checking. Do not reread the whole archive.
   The manifest tracks teaching, not mastery.
2. Cover the previous edition's date through today's local date, inclusive: the
   previous run's exact research cutoff may be unknown. Deduplicate already covered
   stories; use the boundary-day overlap to catch later announcements. Record both
   publication and event dates where they differ. Also search the last seven calendar
   days (today plus six preceding dates) for worthwhile stories not previously covered.
   Label their actual dates; older useful reading is explicitly analysis or a case study.
3. Search the public web and read accessible newsrooms, release notes, technical
   publications, and independent reporting for all nine news categories. Search broad
   categories as well as named vendors, discovering players beyond the watchlist.
   Check all three Google sources and Crusoe homepage, newsroom and resource/blog
   pages each run. Research runs with the user request; no scheduled scraper or backend.
4. Open candidate source pages and verify the actual claims, dates, status (announced,
   preview, available, planned), and units. Search snippets alone are discovery aids.
   Independent articles repeating one original report are not separate confirmation.
   Use company-claim attribution where appropriate. Never fabricate a link or date.
5. Keep a compact research/YYYY-MM-DD.md log: selected sources and dates, required
   checks, meaningful duplication decisions, resource-to-lesson mapping and access gaps.
   Do not narrate every query or rejected candidate. If inaccessible sources leave a
   material gap, explain it in the affected section; do not infer no news from failure.
6. Write briefs/YYYY-MM-DD.md using the format below. Preserve nine news sections in
   the AGENTS.md order, each with 1–2 worthwhile stories and one In Practice bite.
   Use the research breadth gate below before accepting a quiet section.
   More links are useful only when they add evidence, a perspective, or understanding.
7. Start directly with news; do not write opening takeaways or "Today at a glance".
   Put long learning on
   the separate Deep Dives page: exactly three subjects, physical, logical and PgPM.
   From September 21 each technical subject gets 300–450 words: one mechanism, one
   worked example and one practical takeaway, with purposeful sources. Earlier editions
   retain 500–800 words. Keep PgPM Growth around 350–450 words total, including resources
   and action. Research liquid cooling each run and rotate focused cooling lessons into
   learning without adding a news section or a daily lesson quota. Vary subjects based
   on prior coverage. Every fourth expanded
   edition (formats 2 and 3 together, starting September 5) marks one technical subject
   `synthesis: true`, explicitly revisiting earlier concepts. Recall answers are optional.
8. Invoke $build-pgpm-growth for the third subject. Keep two connected lessons, exactly
   six researched external links (three per lesson), a worked example and one optional
   time-boxed Daily Action. Do not add study links inside News or force a news tie-in
   for professional growth. A lesson may reference relevant news when useful.
9. Use `./publish.sh YYYY-MM-DD [reviewed-related-file ...]` from main as the single normal
   build-and-test pass. Confirm deployment and the live date, with a quick desktop
   check of the new content. Rerun only after a correction or failed check. Automated
   tests cover structure and internal links, not factual truth. Do not recheck unchanged
   archives, historical pages, navigation, keyboard behavior or recall every run.
   Full affected-feature visual checks are for renderer/layout changes or a reported
   defect. No mobile checks. Routine related changes share one direct-main commit/push;
   reserve branches/PRs for larger or risky changes or an explicit request.

## Research breadth gate
Cover every category with targeted discovery; there is no minimum query count.
Batch related searches and reuse relevant results across categories without duplicating
stories. Expand topic, vendor, region or development-type searches when initial coverage
is weak, stale or one-sided. Stop when the selected story is adequately verified and
required source checks are complete. Verify dates on underlying pages.
Inspect relevant articles across multiple publishers, combining specialist/independent
reporting with primary announcements, filings, customer accounts and technical material.
Expand synonyms and regional coverage when the first pass returns duplicates or little
of value. Newsroom indexes and search snippets are discovery, not completed reporting.

Choose one strong item by default; add a second when it materially improves coverage.
Record selected evidence and important gaps, not exhaustive candidate narratives.
Syndicated copies count as one underlying report. Add productive
new sources to the watchlist as explicitly reviewed files in the same routine batch.

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
New sources use `format: 3` and, from September 20, `news_profile: "lean-v1"`.
This retains Incidents, Reliability & Remediation in position three and drops Program & PM
from News, leaving nine sections. September 19 uses `incidents-v1`. Earlier sources keep their historical
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

## Physical Deep Dive
:::deep-dive Cooling capacity
Write one focused technical lesson here (300–450 words for current editions).
[Related infrastructure news](news:dc-infrastructure)
:::

## Logical Deep Dive
:::deep-dive Telemetry replay
### Follow a delayed measurement
Write the second focused 300–450-word lesson. Add purposeful sources.
[Related controls story](news:dcos-dcim-bms-controls)
:::

:::recall If the supervisory server fails, must the local controller stop?
Revealable answer explaining the failure behavior.
:::
```

Only `deep-dive` and `recall` containers are supported; close each with `:::` and do
not nest them. Fenced code renders as escaped text, not executable diagrams. Bullets,
headings, and plain paragraphs are retained. External links open in a new tab; fragment
links remain in the page. Use `news:section-slug` from learning for optional paired-date
references. Do not use `learn:` links in new News.
Historical cross-links resolve to dated pages and stay in the
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
