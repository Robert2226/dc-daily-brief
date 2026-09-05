#!/usr/bin/env python3
"""Render all dated briefs, archive, and latest homepage without dependencies.

Usage: python3 build.py [briefs/YYYY-MM-DD.md] [--output-dir PATH]
The optional source is checked for existence; homepage always uses the newest date.
See EDITORIAL.md for the supported Markdown and edition metadata.
"""
import argparse
import datetime as dt
import html
import json
import re
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent
SECTIONS = ['Equinix', 'Google', 'Competitors', 'DC Infrastructure',
            'DCOS, DCIM, BMS & Controls', 'AI & Compute Demand',
            'New AI Models & Releases', 'Networking', 'Backend / Cloud & Data',
            'Program & PM', 'PgPM Growth']
LINK = re.compile(r'\[([^\]]+)\]\(([^\s)]+)\)')
META = re.compile(r'^<!-- edition: (.+) -->$')


def esc(value):
    return html.escape(str(value), quote=True)


def slug(text):
    return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')


def safe_url(url):
    if url.startswith('#') or (urlsplit(url).scheme in ('http', 'https') and urlsplit(url).netloc):
        return url
    raise ValueError(f'Unsupported link URL: {url}')


def inline(text):
    """Escape text first; only supported links/emphasis become markup."""
    out, pos = [], 0
    def emphasis(value):
        value = esc(value)
        value = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', value)
        return re.sub(r'\*(.+?)\*', r'<em>\1</em>', value)
    for m in LINK.finditer(text):
        out.append(emphasis(text[pos:m.start()]))
        url = safe_url(m[2])
        attrs = '' if url.startswith('#') else ' target="_blank" rel="noopener noreferrer"'
        out.append(f'<a href="{esc(url)}"{attrs}>{emphasis(m[1])}</a>')
        pos = m.end()
    out.append(emphasis(text[pos:]))
    return ''.join(out)


def sources(text):
    """Separate a run of trailing source links; retain inline links in prose."""
    found = []
    while True:
        m = re.search(r'\s*(\[[^\]]+\]\([^\s)]+\))\s*$', text)
        if not m:
            break
        found.insert(0, m[1])
        text = text[:m.start()].rstrip()
    return text, ('<div class="source">' + ' · '.join(inline(x) for x in found) + '</div>') if found else ''


def parse(md):
    doc = {'title': '', 'coverage': '', 'meta': {}, 'sections': [], 'takeaways': []}
    current, container, stack = None, None, []
    lines = md.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        i += 1
        if not line:
            continue
        match = META.match(line)
        if match:
            doc['meta'] = json.loads(match[1])
        elif line.startswith('# DC Daily Brief'):
            doc['title'] = line.split('—', 1)[-1].strip()
        elif line.startswith('_Covers'):
            doc['coverage'] = line.strip('_')
        elif line.startswith('## '):
            if stack:
                raise ValueError('Close ::: blocks before starting a section')
            name = line[3:]
            if name == 'Today at a glance':
                current = None
                container = doc['takeaways']
            else:
                current = {'name': name, 'blocks': []}
                doc['sections'].append(current)
                container = current['blocks']
        elif line.startswith(':::'):
            if container is None:
                raise ValueError('Block outside a section')
            if line == ':::':
                if not stack:
                    raise ValueError('Unexpected block closure')
                container = stack.pop()
            else:
                m = re.fullmatch(r':::(deep-dive|recall) (.+)', line)
                if not m or stack:
                    raise ValueError(f'Invalid or nested block: {line}')
                block = {'kind': m[1], 'title': m[2], 'blocks': []}
                container.append(block)
                stack.append(container)
                container = block['blocks']
        elif line.startswith('```'):
            if container is None:
                raise ValueError('Code outside a section')
            code = []
            while i < len(lines) and not lines[i].strip().startswith('```'):
                code.append(lines[i]); i += 1
            if i == len(lines):
                raise ValueError('Unclosed code fence')
            i += 1
            container.append({'kind': 'code', 'text': '\n'.join(code)})
        elif container is None:
            raise ValueError(f'Content outside a section: {line}')
        elif line.startswith('> '):
            value = line[2:]
            m = re.match(r'\*\*(.+?)\*\*\s*(.*)', value)
            container.append({'kind': 'practice', 'title': m[1].rstrip('.') if m else 'In Practice',
                              'text': m[2] if m else value})
        elif line.startswith('- **') and re.match(r'- \*\*(.+?)\*\* — (.*)', line):
            m = re.match(r'- \*\*(.+?)\*\* — (.*)', line)
            container.append({'kind': 'item', 'title': m[1], 'text': m[2]})
        elif line.startswith('- '):
            container.append({'kind': 'bullet', 'text': line[2:]})
        elif line == '---':
            container.append({'kind': 'rule'})
        elif line.startswith('### '):
            container.append({'kind': 'heading', 'text': line[4:]})
        else:
            container.append({'kind': 'paragraph', 'text': line})
    if stack:
        raise ValueError('Unclosed ::: block')
    if not doc['title'] or not doc['sections']:
        raise ValueError('Missing edition title or sections')
    return doc


def walk(blocks):
    for block in blocks:
        yield block
        yield from walk(block.get('blocks', []))


def validate(doc, date):
    """Historical editions remain readable; v2 editions satisfy the new contract."""
    for block in walk(doc['takeaways'] + [b for s in doc['sections'] for b in s['blocks']]):
        for _, url in LINK.findall(block.get('text', '')):
            safe_url(url)
            if url.startswith('#') and url[1:] not in {slug(s['name']) for s in doc['sections']}:
                raise ValueError(f'Unknown section link: {url}')
    if doc['meta'].get('format') != 2:
        if any(s['name'] == SECTIONS[4] for s in doc['sections']):
            raise ValueError('Expanded controls section requires format-2 metadata')
        return
    if [s['name'] for s in doc['sections']] != SECTIONS:
        raise ValueError('Expanded editions require the eleven sections in editorial order')
    if len(doc['takeaways']) != 3:
        raise ValueError('Exactly three opening takeaways required')
    edition_date = dt.date.fromisoformat(date)
    expected_title = f'{edition_date:%A, %B} {edition_date.day}, {edition_date.year}'
    if doc['title'] != expected_title:
        raise ValueError('Edition title must match the filename date and weekday')
    start = dt.date.fromisoformat(doc['meta']['coverage_start'])
    end = dt.date.fromisoformat(doc['meta']['coverage_end'])
    if start > end or end != dt.date.fromisoformat(date):
        raise ValueError('Invalid coverage interval')
    for field in ('deep_dive_track', 'topics', 'pgpm_topics', 'case', 'research_log'):
        if not doc['meta'].get(field):
            raise ValueError(f'Missing metadata: {field}')
    for section in doc['sections'][:-1]:
        if len([b for b in section['blocks'] if b['kind'] == 'practice']) != 1:
            raise ValueError(f'One learning bite required: {section["name"]}')
    dives = [b for s in doc['sections'] for b in s['blocks'] if b['kind'] == 'deep-dive']
    if len(dives) != 1:
        raise ValueError('Exactly one deep dive required')
    words = sum(len(b.get('text', '').split()) for b in walk(dives[0]['blocks']))
    if not 500 <= words <= 800:
        raise ValueError(f'Deep dive must be 500–800 words; found {words}')
    growth = doc['sections'][-1]['blocks']
    items = [b for b in growth if b['kind'] == 'item']
    if len(items) != 6 or any(b['title'].startswith('Resource') for b in items[:2]) or not all(b['title'].startswith('Resource') for b in items[2:]):
        raise ValueError('PgPM Growth requires two lessons and four resources')
    urls = [u for b in walk(growth) for _, u in LINK.findall(b.get('text', ''))]
    if len(urls) != 6 or len(set(urls)) != 6 or any(not u.startswith('https://') for u in urls):
        raise ValueError('PgPM Growth requires six distinct HTTPS sources')
    actions = [b for b in growth if b['kind'] == 'practice' and b['title'].startswith('Daily Action')]
    if len(actions) != 1 or not re.search(r'\b\d+[ -]minute', actions[0]['text']):
        raise ValueError('One time-boxed Daily Action required')


def render_blocks(blocks):
    out = []
    for b in blocks:
        kind = b['kind']
        body, refs = sources(b.get('text', ''))
        if kind == 'item':
            out.append(f'<article class="item"><h3>{inline(b["title"])}</h3><p>{inline(body)}</p>{refs}</article>')
        elif kind == 'practice':
            out.append(f'<aside class="practice"><h3 class="label">{inline(b["title"])}</h3><p>{inline(body)}</p>{refs}</aside>')
        elif kind == 'deep-dive':
            out.append(f'<div class="deep-dive"><p class="eyebrow">Deep dive</p><h3>{inline(b["title"])}</h3>{render_blocks(b["blocks"])}</div>')
        elif kind == 'recall':
            out.append(f'<details class="recall"><summary>{inline(b["title"])}</summary>{render_blocks(b["blocks"])}</details>')
        elif kind == 'code':
            out.append(f'<pre><code>{esc(b["text"])}</code></pre>')
        elif kind == 'rule':
            out.append('<hr>')
        elif kind == 'heading':
            out.append(f'<h4>{inline(b["text"])}</h4>')
        elif kind == 'bullet':
            out.append(f'<ul class="reading-list"><li>{inline(b["text"])}</li></ul>')
        else:
            out.append(f'<p>{inline(body)}</p>{refs}')
    return '\n'.join(out)


def render(doc, number, template, prefix='', adjacent=''):
    nav = '<nav class="section-nav" aria-label="Edition sections">' + ''.join(
        f'<a href="#{slug(s["name"])}">{esc(s["name"])}</a>' for s in doc['sections']) + '</nav>'
    takeaways = ('<aside class="takeaways"><h2>Today at a glance</h2>' + render_blocks(doc['takeaways']) + '</aside>') if doc['takeaways'] else ''
    content = takeaways + nav
    for i, s in enumerate(doc['sections'], 1):
        content += f'<section class="section" id="{slug(s["name"])}"><h2 class="section-head"><span class="section-num">{i:02}</span><span class="section-title">{esc(s["name"])}</span></h2>{render_blocks(s["blocks"])}</section>'
    values = {'DATE': doc['title'], 'DATELINE': doc['title'].replace(', ', ' · ', 1), 'ISSUE': f'{number:03}', 'COVERAGE': doc['coverage']}
    for key, value in values.items():
        template = template.replace('{{' + key + '}}', esc(value))
    return template.replace('{{ROOT}}', prefix).replace('<!-- SECTIONS -->', content).replace('<!-- ADJACENT -->', adjacent)


def build(root=ROOT, output=None):
    root, output = Path(root), Path(output or root)
    files = sorted((root / 'briefs').glob('????-??-??.md'))
    if not files:
        raise ValueError('No dated briefs')
    registry_path = root / 'edition-manifest.json'
    registry = json.loads(registry_path.read_text()) if registry_path.exists() else {}
    numbers = [v['issue'] for v in registry.values()]
    if any(not isinstance(n, int) or n < 1 for n in numbers) or len(numbers) != len(set(numbers)):
        raise ValueError('Manifest issue numbers must be distinct positive integers')
    next_number = max(numbers, default=0)
    documents = {}
    expanded_count = 0
    for p in files:
        dt.date.fromisoformat(p.stem)
        doc = parse(p.read_text())
        validate(doc, p.stem)
        if doc['meta'].get('format') == 2:
            log = root / doc['meta']['research_log']
            if log.resolve().parent != (root / 'research').resolve() or not log.is_file():
                raise ValueError('Research log must exist inside research/')
        if p.stem not in registry:
            next_number += 1
            registry[p.stem] = {'issue': next_number}
        if doc['meta'].get('format') == 2:
            expanded_count += 1
            if expanded_count % 4 == 0 and doc['meta']['deep_dive_track'] != 'synthesis':
                raise ValueError('Every fourth expanded edition needs a synthesis deep dive')
        registry[p.stem].update({'title': doc['title'], **doc['meta']})
        documents[p.stem] = doc
    template = (root / 'template.html').read_text()
    pages = {}
    dates = list(documents)
    for i, date in enumerate(dates):
        links = []
        if i:
            links.append(f'<a href="{dates[i-1]}.html">← Previous edition</a>')
        if i + 1 < len(dates):
            links.append(f'<a href="{dates[i+1]}.html">Next edition →</a>')
        adjacent = '<nav class="edition-nav" aria-label="Adjacent editions">' + ' '.join(links) + '</nav>'
        pages[f'editions/{date}.html'] = render(documents[date], registry[date]['issue'], template, '../', adjacent)
    latest = dates[-1]
    pages['index.html'] = render(documents[latest], registry[latest]['issue'], template)
    rows = ''.join(f'<li><a href="editions/{date}.html">{esc(documents[date]["title"])}</a><span class="archive-meta">No. {registry[date]["issue"]:03}' + (' · ' + esc(registry[date]['deep_dive_track']) if registry[date].get('deep_dive_track') else '') + '</span></li>' for date in reversed(dates))
    archive = {'title': 'Archive', 'coverage': 'Past editions preserve their original reporting and may contain superseded information.', 'sections': [], 'takeaways': []}
    shell = render(archive, len(dates), template)
    shell = shell.replace('<nav class="section-nav" aria-label="Edition sections"></nav>', '<section class="section"><h2>Past editions</h2><p>Browse by date. Earlier reporting has not been re-verified.</p><ol class="archive-list">' + rows + '</ol></section>')
    pages['archive.html'] = shell
    pages['latest.md'] = files[-1].read_text()
    pages['edition-manifest.json'] = json.dumps(registry, indent=2, ensure_ascii=False) + '\n'
    # Validate all documents before writing any output.
    for path, content in pages.items():
        dest = output / path
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(content)
    return len(dates)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', nargs='?')
    parser.add_argument('--output-dir', type=Path)
    args = parser.parse_args()
    if args.source and Path(args.source).resolve() not in (ROOT / 'briefs').glob('????-??-??.md'):
        parser.error('Source must be an existing dated Markdown file in briefs/')
    try:
        count = build(output=args.output_dir)
    except (ValueError, KeyError) as error:
        parser.exit(1, f'Build failed: {error}\n')
    print(f'Built {count} dated editions, archive, manifest, and latest homepage')

if __name__ == '__main__':
    main()
