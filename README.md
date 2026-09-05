# DC Daily Brief

[Read the latest edition](https://robert2226.github.io/dc-daily-brief/) ·
[Browse the archive](https://robert2226.github.io/dc-daily-brief/archive.html)

Robert's on-demand newspaper and learning companion: data-center facilities, logical
systems, and the craft of technical program delivery. Researched when requested,
usually every two days, with three takeaways, ten news categories, a rotating deep dive,
and progressive PgPM learning. Quality and depth come before a fixed reading time.

The dedicated **DCOS, DCIM, BMS & Controls** section spans the vendor ecosystem, software,
integrations, and relevant hardware. DCOS means Data Center Operating System; DCIM means
Data Center Infrastructure Management. Broad category discovery and vendor research run
each edition; AVEVA, FactoryTalk and Emerson are examples, not a closed list.

## Reading and generation
The site is static HTML/CSS with no backend, JavaScript requirement, or reader build step.
External Google Fonts have local fallbacks. Recall answers use native HTML disclosure.

- `AGENTS.md`: authoritative project and publishing rules.
- `EDITORIAL.md`: reader profile, editorial workflow and Markdown format.
- `SOURCES.md`: expandable research starting points.
- `briefs/`: original dated Markdown; `research/`: evidence and research-gap records.
- `build.py` and `template.html`: dependency-free rendering and shared design.
- `editions/`, `archive.html`, `index.html`, `latest.md`: generated reading surfaces.
- `edition-manifest.json`: stable issue numbers and topics taught, not reader progress.

```sh
python3 build.py briefs/YYYY-MM-DD.md
python3 -m unittest discover -s tests
python3 -m http.server 8091 --directory .
```

The build renders every dated edition and always selects the newest date for the
homepage. `--output-dir /tmp/brief-preview` isolates generated output for inspection.
Historical editions retain their content and are not fact-checked again by rendering.

Manual changes use branch → PR → review → merge. User-initiated content-only editions
publish from main with `./publish.sh YYYY-MM-DD` (defaults to today's local date).
Generation is not scheduled and publishing does not research or write the brief for you.
