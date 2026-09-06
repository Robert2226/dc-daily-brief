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
   publication and event dates where they differ. Label older background explicitly.
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
   If a reasonable research pass finds no material update, say so and still teach.
   More links are useful only when they add evidence, a perspective, or understanding.
7. Add exactly three opening takeaways linking to news sections. Put long learning on
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
   both latest pages, paired dates, archive, historical pages, mobile/dark presentation,
   keyboard navigation and recall. Content-only publishing uses `./publish.sh YYYY-MM-DD`
   from main. Structural launches include their full launch edition in the manual PR.

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
New sources use `format: 3`. Metadata `subjects` must contain three ordered entries with
unique slug `id`, `track` (physical/logical/pgpm), and reader-facing `title`. The optional
`synthesis: true` belongs on one technical subject. Format 2 remains readable unchanged.

```markdown
# DC Daily Brief — Sunday, September 6, 2026
_Covers September 5–6, 2026; since the previous edition._
<!-- edition: {"format":3,"coverage_start":"2026-09-05","coverage_end":"2026-09-06","subjects":[{"id":"cooling-capacity","track":"physical","title":"Physical · Cooling capacity"},{"id":"telemetry-replay","track":"logical","title":"Logical · Telemetry replay"},{"id":"pilot-to-fleet","track":"pgpm","title":"PgPM Growth · Pilot to fleet"}],"topics":["Cooling capacity","Telemetry replay"],"pgpm_topics":["Representative pilots — leadership","Progressive rollouts — leadership"],"case":"Hypothetical Hall A","research_log":"research/2026-09-06.md"} -->

## Today at a glance
- **Takeaway headline** — Why it matters. [Read](#dcos-dcim-bms-controls)
```

Add exactly three takeaways. Normal sections use:

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
same tab. Use `#section-slug` for news takeaways. Each technical source section contains
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
