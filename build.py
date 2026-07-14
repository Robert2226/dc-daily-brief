#!/usr/bin/env python3
"""
build.py — render a DC Daily Brief markdown edition into the styled index.html.

Usage:  python3 build.py briefs/YYYY-MM-DD.md

No dependencies. Deterministic styling: reads template.html, injects the sections,
writes index.html. The markdown file is the source of truth.

Expected markdown format (see any file in briefs/):
    # DC Daily Brief — <Weekday, Month D, YYYY>
    _Covers news through <coverage>._

    ## <Section Name>
    - **<headline>** — <summary ...> [<source label>](<url>)
    > **In Practice · <Topic>.** <teaching text> [optional source](url)
"""
import sys, os, re, html, glob

ROOT = os.path.dirname(os.path.abspath(__file__))
LINK_END = re.compile(r'\s*\[([^\]]+)\]\(([^)]+)\)\s*$')

def esc(s):
    return html.escape(s, quote=False)

def inline(s):
    """Escape, then convert **bold** and *italic* to HTML."""
    s = esc(s)
    s = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)
    s = re.sub(r'\*(.+?)\*', r'<em>\1</em>', s)
    return s

def split_source(text):
    """Peel a trailing [label](url) off `text`; return (body, source_html)."""
    m = LINK_END.search(text)
    if not m:
        return text.rstrip(), ''
    label, url = m.group(1), m.group(2)
    body = text[:m.start()].rstrip()
    src = ('<div class="source"><a target="_blank" rel="noopener" '
           f'href="{esc(url)}">{esc(label)}</a></div>')
    return body, src

def parse(md):
    date_text, coverage, sections, cur = '', '', [], None
    for ln in md.splitlines():
        if ln.startswith('# DC Daily Brief'):
            date_text = ln.split('—', 1)[1].strip() if '—' in ln else ln.lstrip('# ').strip()
        elif ln.startswith('_Covers'):
            coverage = ln.strip().strip('_').rstrip('.') + '.'
        elif ln.startswith('## '):
            cur = {'name': ln[3:].strip(), 'items': [], 'practice': None}
            sections.append(cur)
        elif ln.startswith('- **') and cur is not None:
            m = re.match(r'- \*\*(.+?)\*\* — (.*)$', ln)
            if m:
                body, src = split_source(m.group(2))
                cur['items'].append((m.group(1), body, src))
        elif ln.startswith('> ') and cur is not None:
            content = ln[2:].strip()
            pm = re.match(r'\*\*(.+?)\*\*\s*(.*)$', content)
            label, text = (pm.group(1), pm.group(2)) if pm else ('In Practice', content)
            text, src = split_source(text)
            cur['practice'] = (label.rstrip('.'), text, src)
    return date_text, coverage, sections

def render_sections(sections):
    out = []
    for i, sec in enumerate(sections, 1):
        out.append('  <section class="section">')
        out.append(f'    <div class="section-head"><span class="section-num">{i:02d}</span>'
                   f'<span class="section-title">{inline(sec["name"])}</span></div>')
        for headline, body, src in sec['items']:
            out.append(f'    <div class="item"><h3>{inline(headline)}</h3>'
                       f'<p>{inline(body)}</p>{src}</div>')
        if sec['practice']:
            label, text, src = sec['practice']
            out.append('    <div class="practice">'
                       f'<span class="label">{inline(label)}</span>'
                       f'<p>{inline(text)}</p>{src}</div>')
        out.append('  </section>')
    return '\n'.join(out)

def main():
    if len(sys.argv) < 2:
        sys.exit('usage: python3 build.py briefs/YYYY-MM-DD.md')
    md_path = sys.argv[1]
    with open(md_path, encoding='utf-8') as f:
        date_text, coverage, sections = parse(f.read())

    dateline = date_text.replace(', ', ' · ', 1)
    issue = f'{len(glob.glob(os.path.join(ROOT, "briefs", "*.md"))):03d}'

    with open(os.path.join(ROOT, 'template.html'), encoding='utf-8') as f:
        tmpl = f.read()

    out = (tmpl
           .replace('{{DATE}}', esc(date_text))
           .replace('{{DATELINE}}', esc(dateline))
           .replace('{{ISSUE}}', issue)
           .replace('{{COVERAGE}}', esc(coverage))
           .replace('<!-- SECTIONS -->', render_sections(sections)))

    with open(os.path.join(ROOT, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(out)
    print(f'built index.html — edition No. {issue}, {len(sections)} sections, dated {date_text}')

if __name__ == '__main__':
    main()
