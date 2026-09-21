# DC Daily Brief

[Read News](https://robert2226.github.io/dc-daily-brief/) ·
[Read Deep Dives](https://robert2226.github.io/dc-daily-brief/deep-dives.html) ·
[Browse the archive](https://robert2226.github.io/dc-daily-brief/archive.html)

Robert's on-demand newspaper and learning companion: data-center facilities, logical
systems, and the craft of technical program delivery. Researched when requested,
usually every two days, with nine news categories, a separate learning page with physical and logical deep dives,
and progressive PgPM learning. Quality and depth come before a fixed reading time.

The dedicated **DCOS, DCIM, BMS & Controls** section spans the vendor ecosystem, software,
integrations, and relevant hardware. DCOS means Data Center Operating System; DCIM means
Data Center Infrastructure Management. Broad category discovery and vendor research run
each edition; AVEVA, FactoryTalk and Emerson are examples, not a closed list.

From September 19, 2026, **Incidents, Reliability & Remediation** replaces Competitors
in position three. It follows significant facility and service failures, concrete risks,
postmortems and corrective work across operators. Format-3 editions declare
`news_profile: "incidents-v1"`; earlier editions retain their original lineup and links.
Relevant incident cases also inform the learning curriculum.

The latest News page starts directly with section navigation and news, without a
"Today at a glance" summary. New editions from September 20 omit that summary;
older dated editions retain their original content.

From September 20, `news_profile: "lean-v1"` drops Program & PM news while retaining
PgPM Growth learning. Latest pages adopt the lean presentation immediately: no study
links in News, no duplicate date navigation, and no subject contents list on Deep Dives.
The top News | Deep Dives | Archive navigation remains. Historical dated pages are preserved.

Daily work uses targeted research without a search quota, manifest-first topic review,
compact evidence notes, one normal publish/build/test pass and a quick desktop content
check. Full layout/archive/keyboard checks are reserved for relevant structural changes;
mobile checks are not required. Mandatory Google, Crusoe and incident checks remain.

## Reading and generation
The site is static HTML/CSS with no backend, JavaScript requirement, or reader build step.
External Google Fonts have local fallbacks. Recall answers use native HTML disclosure.

- `AGENTS.md`: authoritative project and publishing rules.
- `EDITORIAL.md`: reader profile, editorial workflow and Markdown format.
- `SOURCES.md`: expandable research starting points.
- `briefs/`: original dated Markdown; `research/`: evidence and research-gap records.
- `build.py` and `template.html`: dependency-free rendering and shared design.
- `editions/`, `deep-dives/`, `archive.html`, `index.html`, `deep-dives.html`, `latest.md`: generated reading surfaces.
- `edition-manifest.json`: stable issue numbers and topics taught, not reader progress.

```sh
python3 build.py briefs/YYYY-MM-DD.md
python3 -m unittest discover -s tests
python3 -m http.server 8091 --directory .
```

The build renders every dated edition and always selects the newest date for the
homepage. `--output-dir /tmp/brief-preview` isolates generated output for inspection.
Historical editions retain their content and are not fact-checked again by rendering.

Routine work uses one reviewed commit and push directly to main, without a PR.
Publish with `./publish.sh YYYY-MM-DD` (defaults to today's local date). To include
related workflow/docs/layout changes in that same batch, append their explicit file paths:
`./publish.sh YYYY-MM-DD AGENTS.md EDITORIAL.md`. Unlisted unrelated edits are refused.
Reserve branches/PRs for larger or risky changes or when requested.
Generation is not scheduled and publishing does not research or write the brief for you.

New editions share one date and issue across News and Deep Dives. Top navigation opens
the latest pages; optional lesson-to-news references stay on the same date. Older
combined editions keep their URLs and original content. Each technical deep dive runs
300–450 words from September 21 onward (historical lessons remain unchanged); PgPM Growth
is the third learning subject, with two connected lessons in roughly 350–450 words total.
Each technical lesson focuses on one mechanism, one example and one takeaway. Liquid
cooling is researched each run within the existing news categories and recurs in focused
learning; it does not add another section.
