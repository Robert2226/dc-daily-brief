#!/usr/bin/env python3
"""Render all dated briefs, archive, and latest homepage without dependencies.

Usage: python3 build.py [briefs/YYYY-MM-DD.md] [--output-dir PATH]
The optional source is checked for existence; homepage always uses the newest date.
See EDITORIAL.md for the supported Markdown and edition metadata.
"""
import argparse
import copy
import posixpath
from html.parser import HTMLParser
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
SPLIT_SECTIONS = SECTIONS[:-1] + ['Physical Deep Dive', 'Logical Deep Dive', 'PgPM Growth']
LINK = re.compile(r'\[([^\]]+)\]\(([^\s)]+)\)')
META = re.compile(r'^<!-- edition: (.+) -->$')


def esc(value):
    return html.escape(str(value), quote=True)


def slug(text):
    return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')


def safe_url(url):
    if re.fullmatch(r'(learn|news):[a-z0-9]+(?:-[a-z0-9]+)*', url) or url.startswith('#') or (urlsplit(url).scheme in ('http', 'https') and urlsplit(url).netloc):
        return url
    raise ValueError(f'Unsupported link URL: {url}')


def inline(text, links=None):
    """Escape text first; only supported links/emphasis become markup."""
    out, pos = [], 0
    def emphasis(value):
        value = esc(value)
        value = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', value)
        return re.sub(r'\*(.+?)\*', r'<em>\1</em>', value)
    for m in LINK.finditer(text):
        out.append(emphasis(text[pos:m.start()]))
        url = safe_url(m[2])
        if url.startswith(('learn:', 'news:')):
            if links is None or url not in links:
                raise ValueError(f'Unresolved edition link: {url}')
            url = links[url]
        attrs = '' if not url.startswith(('http:', 'https:')) else ' target="_blank" rel="noopener noreferrer"'
        out.append(f'<a href="{esc(url)}"{attrs}>{emphasis(m[1])}</a>')
        pos = m.end()
    out.append(emphasis(text[pos:]))
    return ''.join(out)


def sources(text, links=None):
    """Separate a run of trailing source links; retain inline links in prose."""
    found = []
    while True:
        m = re.search(r'\s*(\[[^\]]+\]\([^\s)]+\))\s*$', text)
        if not m:
            break
        found.insert(0, m[1])
        text = text[:m.start()].rstrip()
    return text, ('<div class="source">' + ' · '.join(inline(x, links) for x in found) + '</div>') if found else ''


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
    """Historical editions remain readable; expanded editions satisfy their format contract."""
    version = doc['meta'].get('format')
    subjects = doc['meta'].get('subjects', [])
    destinations = {'learn:' + x.get('id', '') for x in subjects} | {'news:' + slug(x) for x in SECTIONS[:-1]}
    for block in walk(doc['takeaways'] + [b for s in doc['sections'] for b in s['blocks']]):
        for _, url in LINK.findall(block.get('text', '')):
            safe_url(url)
            if url.startswith(('learn:', 'news:')) and (version != 3 or url not in destinations):
                raise ValueError(f'Unknown edition link: {url}')
            if url.startswith('#') and url[1:] not in {slug(s['name']) for s in doc['sections']}:
                raise ValueError(f'Unknown section link: {url}')
    if version not in (2, 3):
        if any(s['name'] == SECTIONS[4] for s in doc['sections']):
            raise ValueError('Expanded controls section requires format-2 or format-3 metadata')
        return
    if [s['name'] for s in doc['sections']] != (SPLIT_SECTIONS if version == 3 else SECTIONS):
        raise ValueError('Expanded editions require their format-specific sections in editorial order')
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
    for field in ('topics', 'pgpm_topics', 'case', 'research_log') + (('deep_dive_track',) if version == 2 else ('subjects',)):
        if not doc['meta'].get(field):
            raise ValueError(f'Missing metadata: {field}')
    for section in doc['sections'][:10]:
        if len([b for b in section['blocks'] if b['kind'] == 'practice']) != 1:
            raise ValueError(f'One learning bite required: {section["name"]}')
    dives = [b for s in doc['sections'] for b in s['blocks'] if b['kind'] == 'deep-dive']
    if len(dives) != (2 if version == 3 else 1):
        raise ValueError('Incorrect number of technical deep dives')
    for dive in dives:
        words = sum(len(b.get('text', '').split()) for b in walk(dive['blocks']))
        if not 500 <= words <= 800:
            raise ValueError(f'Deep dive must be 500–800 words; found {words}')
    if version == 3:
        if len(subjects) != 3 or [x.get('track') for x in subjects] != ['physical', 'logical', 'pgpm']:
            raise ValueError('Three subjects required: physical, logical, pgpm')
        ids = [x.get('id', '') for x in subjects]
        if len(set(ids)) != 3 or any(not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', x) for x in ids):
            raise ValueError('Subject ids must be distinct slugs')
        if any(not x.get('title') for x in subjects) or subjects[-1].get('synthesis'):
            raise ValueError('Subject titles required; synthesis belongs to a technical subject')
        for section in doc['sections'][:10]:
            if not 1 <= sum(b['kind'] == 'item' for b in section['blocks']) <= 2:
                raise ValueError('News sections require one or two items')
            if any(b['kind'] in ('deep-dive', 'recall') for b in walk(section['blocks'])):
                raise ValueError('Long lessons and recall belong on Deep Dives')
            for b in walk(section['blocks']):
                for _, url in LINK.findall(b.get('text', '')):
                    if url.startswith('#') and url[1:] not in {slug(x) for x in SECTIONS[:-1]}:
                        raise ValueError('News anchors must stay on news; use learn: links')
        for section in doc['sections'][10:12]:
            if len([b for b in section['blocks'] if b['kind'] == 'deep-dive']) != 1:
                raise ValueError('One deep dive per technical subject required')
            if not any(u.startswith('https://') for b in walk(section['blocks']) for _, u in LINK.findall(b.get('text', ''))):
                raise ValueError('Technical subjects require sources')
        news_links = {u for sec in doc['sections'][:10] for b in walk(sec['blocks']) for _, u in LINK.findall(b.get('text', ''))}
        for section, subject in zip(doc['sections'][10:], subjects):
            if 'learn:' + subject['id'] not in news_links:
                raise ValueError('Each subject needs a related news link')
            if not any(u.startswith('news:') for b in walk(section['blocks']) for _, u in LINK.findall(b.get('text', ''))):
                raise ValueError('Each subject must link back to related news')
    growth = doc['sections'][-1]['blocks']
    items = [b for b in growth if b['kind'] == 'item']
    if len(items) != 6 or any(b['title'].startswith('Resource') for b in items[:2]) or not all(b['title'].startswith('Resource') for b in items[2:]):
        raise ValueError('PgPM Growth requires two lessons and four resources')
    urls = [u for b in walk(growth) for _, u in LINK.findall(b.get('text', '')) if not u.startswith(('news:', 'learn:', '#'))]
    if len(urls) != 6 or len(set(urls)) != 6 or any(not u.startswith('https://') for u in urls):
        raise ValueError('PgPM Growth requires six distinct HTTPS sources')
    if version == 3 and not any(b['kind'] == 'heading' and b['text'].startswith('Worked example') for b in growth):
        raise ValueError('PgPM Growth requires a worked example')
    actions = [b for b in growth if b['kind'] == 'practice' and b['title'].startswith('Daily Action')]
    if len(actions) != 1 or not re.search(r'\b\d+[ -]minute', actions[0]['text']):
        raise ValueError('One time-boxed Daily Action required')


def render_blocks(blocks, links=None):
    out = []
    for b in blocks:
        kind = b['kind']
        body, refs = sources(b.get('text', ''), links)
        if kind == 'item':
            out.append(f'<article class="item"><h3>{inline(b["title"], links)}</h3><p>{inline(body, links)}</p>{refs}</article>')
        elif kind == 'practice':
            out.append(f'<aside class="practice"><h3 class="label">{inline(b["title"], links)}</h3><p>{inline(body, links)}</p>{refs}</aside>')
        elif kind == 'deep-dive':
            out.append(f'<div class="deep-dive"><p class="eyebrow">Deep dive</p><h3>{inline(b["title"], links)}</h3>{render_blocks(b["blocks"], links)}</div>')
        elif kind == 'recall':
            out.append(f'<details class="recall"><summary>{inline(b["title"], links)}</summary>{render_blocks(b["blocks"], links)}</details>')
        elif kind == 'code':
            out.append(f'<pre><code>{esc(b["text"])}</code></pre>')
        elif kind == 'rule':
            out.append('<hr>')
        elif kind == 'heading':
            out.append(f'<h4>{inline(b["text"], links)}</h4>')
        elif kind == 'bullet':
            out.append(f'<ul class="reading-list"><li>{inline(b["text"], links)}</li></ul>')
        else:
            out.append(f'<p>{inline(body, links)}</p>{refs}')
    return '\n'.join(out)


def render(doc, number, template, prefix='', adjacent='', links=None, active='news', paired=''):
    nav = '<nav class="section-nav" aria-label="Edition sections">' + ''.join(
        f'<a href="#{s.get("id", slug(s["name"]))}">{esc(s["name"])}</a>' for s in doc['sections']) + '</nav>'
    takeaways = ('<aside class="takeaways"><h2>Today at a glance</h2>' + render_blocks(doc['takeaways'], links) + '</aside>') if doc['takeaways'] else ''
    content = paired + takeaways + nav
    for i, s in enumerate(doc['sections'], 1):
        content += f'<section class="section" id="{s.get("id", slug(s["name"]))}"><h2 class="section-head"><span class="section-num">{i:02}</span><span class="section-title">{esc(s["name"])}</span></h2>{render_blocks(s["blocks"], links)}</section>'
    values = {'DATE': doc['title'], 'DATELINE': doc['title'].replace(', ', ' · ', 1), 'ISSUE': f'{number:03}', 'COVERAGE': doc['coverage'], 'PAGE_KIND': {'news': 'News', 'learning': 'Deep Dives', 'archive': 'Archive'}[active]}
    for key, value in values.items():
        template = template.replace('{{' + key + '}}', esc(value))
    site_nav = '<nav class="site-nav" aria-label="Main navigation">' + ' '.join(
        f'<a href="{prefix}{path}"' + (' aria-current="page"' if active == key else '') + f'>{label}</a>'
        for key, path, label in [('news', 'index.html', 'News'), ('learning', 'deep-dives.html', 'Deep Dives'), ('archive', 'archive.html', 'Archive')]) + '</nav>'
    template = template.replace('<!-- SITE NAV -->', site_nav)
    return template.replace('{{ROOT}}', prefix).replace('<!-- SECTIONS -->', content).replace('<!-- ADJACENT -->', adjacent)


def validate_page_links(pages):
    """Reject broken generated paths and anchors before touching published files."""
    class Links(HTMLParser):
        def __init__(self, text):
            super().__init__()
            self.ids, self.hrefs = [], []
            self.feed(text)
        def handle_starttag(self, tag, attrs):
            attrs = dict(attrs)
            if 'id' in attrs: self.ids.append(attrs['id'])
            if tag == 'a': self.hrefs.append(attrs.get('href', ''))
    parsed = {path: Links(text) for path, text in pages.items() if path.endswith('.html')}
    for path, page in parsed.items():
        if len(page.ids) != len(set(page.ids)):
            raise ValueError(f'Duplicate anchors: {path}')
        for href in page.hrefs:
            url = urlsplit(href)
            if url.scheme in ('http', 'https'): continue
            target = posixpath.normpath(posixpath.join(posixpath.dirname(path), url.path)) if url.path else path
            if target not in parsed or (url.fragment and url.fragment not in parsed[target].ids):
                raise ValueError(f'Broken link in {path}: {href}')


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
        if doc['meta'].get('format') in (2, 3):
            log = root / doc['meta']['research_log']
            if log.resolve().parent != (root / 'research').resolve() or not log.is_file():
                raise ValueError('Research log must exist inside research/')
        if p.stem not in registry:
            next_number += 1
            registry[p.stem] = {'issue': next_number}
        if doc['meta'].get('format') in (2, 3):
            expanded_count += 1
            if expanded_count % 4 == 0 and not (doc['meta'].get('deep_dive_track') == 'synthesis' or any(x.get('synthesis') for x in doc['meta'].get('subjects', [])[:2])):
                raise ValueError('Every fourth expanded edition needs a synthesis deep dive')
        registry[p.stem].update({'title': doc['title'], **doc['meta']})
        documents[p.stem] = doc
    template = (root / 'template.html').read_text()
    pages = {}
    dates = list(documents)
    def edition_page(date, prefix='', learning=False, adjacent=''):
        doc = copy.deepcopy(documents[date])
        split = doc['meta'].get('format') == 3
        links = {}
        paired = ''
        if split:
            subjects = doc['meta']['subjects']
            links = {'learn:' + x['id']: f'{prefix}deep-dives/{date}.html#{x["id"]}' for x in subjects}
            links.update({'news:' + slug(x): f'{prefix}editions/{date}.html#{slug(x)}' for x in SECTIONS[:-1]})
            paired = f'<nav class="edition-nav" aria-label="Matching edition"><a href="{prefix}editions/{date}.html">{date} · News</a><a href="{prefix}deep-dives/{date}.html">{date} · Deep Dives</a></nav>'
            if learning:
                doc['takeaways'] = []
                doc['sections'] = doc['sections'][10:]
                for section, subject in zip(doc['sections'], subjects):
                    section.update(name=subject['title'], id=subject['id'])
                doc['coverage'] = 'Deep Dives · Physical infrastructure, logical systems, and PgPM Growth. Background teaching with hypothetical examples.'
            else:
                doc['sections'] = doc['sections'][:10]
        return render(doc, registry[date]['issue'], template, prefix, adjacent, links,
                      'learning' if learning else 'news', paired)

    split_dates = [d for d in dates if documents[d]['meta'].get('format') == 3]
    for i, date in enumerate(dates):
        links = []
        if i:
            links.append(f'<a href="{dates[i-1]}.html">← Previous edition</a>')
        if i + 1 < len(dates):
            links.append(f'<a href="{dates[i+1]}.html">Next edition →</a>')
        adjacent = '<nav class="edition-nav" aria-label="Adjacent editions">' + ' '.join(links) + '</nav>'
        pages[f'editions/{date}.html'] = edition_page(date, '../', adjacent=adjacent)
        if date in split_dates:
            j = split_dates.index(date)
            adjacent = '<nav class="edition-nav" aria-label="Adjacent learning editions">'
            if j:
                adjacent += f'<a href="{split_dates[j-1]}.html">← Previous Deep Dives</a>'
            if j + 1 < len(split_dates):
                adjacent += f'<a href="{split_dates[j+1]}.html">Next Deep Dives →</a>'
            pages[f'deep-dives/{date}.html'] = edition_page(date, '../', True, adjacent + '</nav>')
    latest = dates[-1]
    pages['index.html'] = edition_page(latest)
    if split_dates:
        pages['deep-dives.html'] = edition_page(split_dates[-1], learning=True)
    else:
        empty = {'title': 'Deep Dives', 'coverage': 'Earlier learning is included in combined editions in the archive.', 'sections': [], 'takeaways': []}
        pages['deep-dives.html'] = render(empty, registry[latest]['issue'], template, active='learning')
    rows = ''
    for date in reversed(dates):
        split = date in split_dates
        rows += f'<li><strong>{esc(documents[date]["title"])}</strong><span class="archive-meta">No. {registry[date]["issue"]:03}</span><a href="editions/{date}.html">' + ('News' if split else 'Combined edition') + '</a>'
        if split:
            rows += f' · <a href="deep-dives/{date}.html">Deep Dives</a><ul>'
            for subject in documents[date]['meta']['subjects']:
                rows += f'<li><a href="deep-dives/{date}.html#{subject["id"]}">{esc(subject["title"])}</a></li>'
            rows += '</ul>'
        rows += '</li>'
    archive = {'title': 'Archive', 'coverage': 'Past editions preserve their original reporting and may contain superseded information.', 'sections': [], 'takeaways': []}
    shell = render(archive, registry[latest]['issue'], template, active='archive')
    shell = shell.replace('<nav class="section-nav" aria-label="Edition sections"></nav>', '<section class="section"><h2>Past editions</h2><p>News and learning share an edition number. Older combined editions retain their original content.</p><ol class="archive-list">' + rows + '</ol></section>')
    pages['archive.html'] = shell
    validate_page_links(pages)
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
