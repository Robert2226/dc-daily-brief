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
            for pagefile in [root / 'index.html', root / 'archive.html', *(root / 'editions').glob('*.html')]:
                page = Page(pagefile.read_text())
                for a in page.links:
                    href = a['href']
                    if href.startswith('#'):
                        self.assertIn(href[1:], page.ids)
                    elif not href.startswith('http'):
                        self.assertTrue((pagefile.parent / href).is_file(), (pagefile, href))
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

    def test_validation_precedes_output(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); (root / 'briefs').mkdir()
            (root / 'briefs/2026-09-05.md').write_text('# DC Daily Brief — Test\n## Equinix\n:::bad block')
            with self.assertRaises(ValueError): build.build(root)
            self.assertFalse((root / 'index.html').exists())

if __name__ == '__main__': unittest.main()
