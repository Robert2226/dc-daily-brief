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
7. Add exactly three opening takeaways linking to their relevant section. Include
   one 500–800-word deep dive within an existing news section. Rotate infrastructure,
   controls, networking/cloud/software, and program/business topics based on relevance
   and prior coverage. Every fourth format-2 edition uses track `synthesis`: revisit
   developments and earlier lessons with explicit links to original external sources.
   Include short recall questions with revealable answers when useful.
8. Invoke $build-pgpm-growth for Section 11. Use two connected lessons, six researched
   links (three per lesson), and a short optional time-boxed Daily Action with a worked
   example. Advance recurring hypothetical cases and explain what changed in the lesson.
9. Run `python3 build.py briefs/YYYY-MM-DD.md` and `python3 -m unittest discover -s tests`.
   Check sourcing manually: validation checks structure, not truth. Inspect the latest
   page, navigation, and archive. Publishing uses `./publish.sh YYYY-MM-DD` from main.

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
expanded edition begins a new four-edition synthesis cycle. Metadata `format` is 2.

```markdown
# DC Daily Brief — Saturday, September 5, 2026
_Covers September 3–5, 2026; since the previous edition._
<!-- edition: {"format":2,"coverage_start":"2026-09-03","coverage_end":"2026-09-05","deep_dive_track":"controls","topics":["Alarm path"],"pgpm_topics":["Configuration baselines — applied","Verification vs validation — applied"],"case":"Hypothetical Hall A cooling","research_log":"research/2026-09-05.md"} -->

## Today at a glance
- **Takeaway headline** — Why it matters. [Read](#dcos-dcim-bms-controls)
```

Add exactly three takeaways. Normal sections use:

```markdown
## DCOS, DCIM, BMS & Controls
- **Story headline** — Published September 4, 2026. Summary and interpretation. [Announcement](https://example.org/release) [Independent analysis](https://example.org/analysis)

Context paragraphs support **bold**, *italic*, and [inline links](https://example.org).

> **In Practice · A concrete lesson.** Explain the mechanism or use a worked example.

:::deep-dive From sensor to operator
### Follow the signal
Write paragraphs separated by blank lines. Add a fenced text diagram if it helps.
:::

:::recall If the supervisory server fails, must the local controller stop?
Revealable answer explaining why the actual control architecture determines behavior.
:::
```

Only `deep-dive` and `recall` containers are supported; close each with `:::` and do
not nest them. Fenced code renders as escaped text, not executable diagrams. Bullets,
headings, and plain paragraphs are retained. External links open in a new tab; fragment
links remain in the page. No raw HTML, scripts, or executable URL schemes are accepted.

## Archive and numbering
`build.py` renders all dated Markdown files to editions/YYYY-MM-DD.html, creates
archive.html, and chooses the newest filename for index.html and latest.md. Historical
content is preserved rather than retrofitted with new sections. Historical facts are
not re-verified by rendering. `edition-manifest.json` assigns issue numbers once; retain
it in version control so later editions or backfills never renumber published issues.
Use `--output-dir /tmp/brief-preview` for an isolated build. No build is needed to read
any generated HTML. Google Fonts are optional external enhancements with local fallbacks.
