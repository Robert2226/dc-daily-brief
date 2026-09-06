import copy
import json
import re
import shutil
import tempfile
import unittest
from html.parser import HTMLParser
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import build

ROOT = build.ROOT


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.ids, self.links, self.tags, self.text = [], [], [], []
        self.feed(text)
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        self.tags.append(tag)
        if 'id' in a: self.ids.append(a['id'])
        if tag == 'a': self.links.append(a)
    def handle_data(self, text):
        self.text.append(text)


class RenderingTests(unittest.TestCase):
    def test_all_historical_headlines_and_sources_survive(self):
        for source in sorted((ROOT / 'briefs').glob('*.md')):
            md = source.read_text()
            doc = build.parse(md)
            if doc['meta'].get('format') == 3: continue
            page = Page(build.render(doc, 1, (ROOT / 'template.html').read_text()))
            text = ''.join(page.text)
            for title in re.findall(r'^- \*\*(.+?)\*\* — ', md, re.M):
                self.assertIn(title, text, source.name)
            for _, url in build.LINK.findall(md):
                self.assertTrue(any(a['href'] == url for a in page.links), (source.name, url))
            self.assertEqual(len(page.ids), len(set(page.ids)))

    def test_multiple_links_and_escaped_content(self):
        body, sources = build.sources('A <script> & fact [Primary](https://a.test/?x=1&y=2) [Analysis](https://b.test/)')
        page = Page(build.inline(body) + sources)
        self.assertEqual(len(page.links), 2)
        self.assertNotIn('script', page.tags)
        self.assertTrue(all(a['target'] == '_blank' and 'noopener' in a['rel'] for a in page.links))
        for url in ['javascript:alert', 'data:text/html,test', '//evil.test', 'https:bad']:
            with self.subTest(url=url), self.assertRaises(ValueError):
                build.inline(f'[Unsafe]({url})')

    def test_deep_dive_recall_and_paragraphs_retained(self):
        doc = build.parse((ROOT / 'briefs/2026-09-05.md').read_text())
        page = Page(build.render(doc, 37, (ROOT / 'template.html').read_text()))
        self.assertEqual(page.tags.count('details'), 2)
        self.assertEqual(page.tags.count('summary'), 2)
        self.assertIn('Begin with a physical measurement', ''.join(page.text))
        self.assertIn('Sensor → controller', ''.join(page.text))
        self.assertEqual([s['name'] for s in doc['sections']], build.SECTIONS)

    def test_invalid_expanded_edition_fails(self):
        base = build.parse((ROOT / 'briefs/2026-09-05.md').read_text())
        edits = [lambda d: d['sections'].pop(4), lambda d: d['takeaways'].pop(),
                 lambda d: d['meta'].update(coverage_start='2099-01-01'),
                 lambda d: d['sections'][-1]['blocks'].pop(0),
                 lambda d: d['sections'][0]['blocks'].pop(),
                 lambda d: d['meta'].clear()]
        for edit in edits:
            doc = copy.deepcopy(base); edit(doc)
            with self.assertRaises(ValueError): build.validate(doc, '2026-09-05')

    def test_unclosed_blocks_fail(self):
        for fragment in [':::deep-dive Topic\nText', '```text\nText', ':::']:
            with self.assertRaises(ValueError):
                build.parse('# DC Daily Brief — Test\n## Equinix\n' + fragment)

    def test_archive_links_latest_and_stable_numbers(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            shutil.copytree(ROOT / 'briefs', root / 'briefs')
            shutil.copytree(ROOT / 'research', root / 'research')
            shutil.copy(ROOT / 'template.html', root)
            build.build(root)
            before = json.loads((root / 'edition-manifest.json').read_text())
            homepage = (root / 'index.html').read_text()
            for pagefile in [root / 'index.html', root / 'archive.html', root / 'deep-dives.html', *(root / 'editions').glob('*.html'), *(root / 'deep-dives').glob('*.html')]:
                page = Page(pagefile.read_text())
                for a in page.links:
                    href = a['href']
                    if href.startswith('#'):
                        self.assertIn(href[1:], page.ids)
                    elif not href.startswith('http'):
                        target, _, anchor = href.partition('#')
                        targetfile = pagefile.parent / target
                        self.assertTrue(targetfile.is_file(), (pagefile, href))
                        if anchor: self.assertIn(anchor, Page(targetfile.read_text()).ids)
            (root / 'briefs/2026-01-01.md').write_text('# DC Daily Brief — January 1, 2026\n## Equinix\nHistorical backfill.')
            build.build(root)
            after = json.loads((root / 'edition-manifest.json').read_text())
            self.assertEqual(homepage, (root / 'index.html').read_text())
            for date in before:
                self.assertEqual(before[date]['issue'], after[date]['issue'])
            # Rebuilding is deterministic.
            manifest = (root / 'edition-manifest.json').read_text()
            build.build(root)
            self.assertEqual(manifest, (root / 'edition-manifest.json').read_text())

    def test_fourth_expanded_edition_requires_synthesis(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            shutil.copytree(ROOT / 'briefs', root / 'briefs')
            shutil.copytree(ROOT / 'research', root / 'research')
            shutil.copy(ROOT / 'template.html', root)
            base = (root / 'briefs/2026-09-05.md').read_text()
            for day in (6, 7, 8):
                date = build.dt.date(2026, 9, day)
                title = f'{date:%A, %B} {day}, 2026'
                text = base.replace('Saturday, September 5, 2026', title).replace('"coverage_end":"2026-09-05"', f'"coverage_end":"{date}"')
                (root / f'briefs/{date}.md').write_text(text)
            with self.assertRaisesRegex(ValueError, 'fourth'):
                build.build(root)
            last = root / 'briefs/2026-09-08.md'
            last.write_text(last.read_text().replace('"deep_dive_track":"controls"', '"deep_dive_track":"synthesis"'))
            build.build(root)
            self.assertIn('Tuesday, September 8, 2026', (root / 'index.html').read_text())

    def test_split_pages_preserve_content_and_pairing(self):
        with tempfile.TemporaryDirectory() as directory:
            out = Path(directory)
            build.build(output=out)
            news = Page((out / 'index.html').read_text())
            learning = Page((out / 'deep-dives.html').read_text())
            self.assertEqual(news.tags.count('section'), 10)
            self.assertEqual(learning.tags.count('section'), 3)
            self.assertEqual(news.tags.count('details'), 0)
            self.assertEqual(learning.tags.count('details'), 3)
            self.assertNotIn('Today at a glance', ''.join(learning.text))
            self.assertNotIn('Worked example · Hall A', ''.join(news.text))
            source = (ROOT / 'briefs/2026-09-06.md').read_text()
            for title in re.findall(r'^- \*\*(.+?)\*\* — ', source, re.M):
                self.assertIn(title, ''.join(news.text + learning.text))
            for _, url in build.LINK.findall(source):
                if url.startswith('https:'):
                    self.assertTrue(any(a['href'] == url for a in news.links + learning.links), url)
            for kind in ('editions', 'deep-dives'):
                page = Page((out / f'{kind}/2026-09-06.html').read_text())
                for expected in ('../index.html', '../deep-dives.html', '../archive.html',
                                 '../editions/2026-09-06.html', '../deep-dives/2026-09-06.html'):
                    self.assertIn(expected, [a['href'] for a in page.links])
            internal = [a for a in news.links + learning.links if not a['href'].startswith('https:')]
            self.assertTrue(all('target' not in a for a in internal))
            self.assertIn('Combined edition', (out / 'archive.html').read_text())
            self.assertFalse((out / 'deep-dives/2026-09-05.html').exists())

    def test_invalid_split_contracts(self):
        base = build.parse((ROOT / 'briefs/2026-09-06.md').read_text())
        edits = [lambda d: d['meta']['subjects'].pop(),
                 lambda d: d['meta']['subjects'][0].update(track='logical'),
                 lambda d: d['meta']['subjects'][0].update(id='telemetry-replay'),
                 lambda d: d['sections'][10]['blocks'][0]['blocks'].clear(),
                 lambda d: d['sections'][0]['blocks'].append(d['sections'][10]['blocks'][0]),
                 lambda d: d['sections'][1]['blocks'][0].update(text='[Bad](learn:missing)'),
                 lambda d: d['sections'][10]['blocks'][0]['blocks'][-1].update(text='No related news link')]
        for edit in edits:
            doc = copy.deepcopy(base); edit(doc)
            with self.assertRaises(ValueError): build.validate(doc, '2026-09-06')

    def test_cross_format_synthesis_cadence(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            shutil.copytree(ROOT / 'briefs', root / 'briefs')
            shutil.copytree(ROOT / 'research', root / 'research')
            shutil.copy(ROOT / 'template.html', root)
            base = (root / 'briefs/2026-09-06.md').read_text()
            for day in (7, 8):
                date = build.dt.date(2026, 9, day)
                text = base.replace('Sunday, September 6, 2026', f'{date:%A, %B} {day}, 2026').replace('"coverage_end":"2026-09-06"', f'"coverage_end":"{date}"')
                (root / f'briefs/{date}.md').write_text(text)
            with self.assertRaisesRegex(ValueError, 'fourth'): build.build(root)
            last = root / 'briefs/2026-09-08.md'
            last.write_text(last.read_text().replace('"track":"physical"', '"track":"physical","synthesis":true'))
            build.build(root)
            self.assertIn('September 8, 2026', (root / 'deep-dives.html').read_text())
            earlier = (root / 'deep-dives/2026-09-06.html').read_text()
            self.assertIn('../editions/2026-09-06.html#program-pm', earlier)
            self.assertNotIn('../editions/2026-09-08.html#program-pm', earlier)

    def test_generated_broken_links_rejected(self):
        for href in ('missing.html', '#missing', 'learn:unresolved'):
            with self.assertRaisesRegex(ValueError, 'Broken link'):
                build.validate_page_links({'index.html': f'<a href="{href}">Bad</a>'})

    def test_validation_precedes_output(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); (root / 'briefs').mkdir()
            (root / 'briefs/2026-09-05.md').write_text('# DC Daily Brief — Test\n## Equinix\n:::bad block')
            with self.assertRaises(ValueError): build.build(root)
            self.assertFalse((root / 'index.html').exists())

if __name__ == '__main__': unittest.main()
