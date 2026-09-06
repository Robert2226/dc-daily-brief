"""Exercise publishing refusal paths with a fake Git executable; never push."""
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class PublishTests(unittest.TestCase):
    def attempt(self, branch='main', staged='0', dirty=''):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            shutil.copy(ROOT / 'publish.sh', root)
            (root / 'briefs').mkdir()
            (root / 'briefs/2026-09-05.md').write_text('Test fixture')
            bindir = root / 'bin'; bindir.mkdir()
            fake = bindir / 'git'
            fake.write_text('''#!/usr/bin/env python3
import os, sys
from pathlib import Path
with Path(os.environ['CALL_LOG']).open('a') as f: f.write(' '.join(sys.argv[1:]) + '\\n')
a=sys.argv[1:]
if a == ['branch','--show-current']: print(os.environ['BRANCH'])
elif a == ['diff','--cached','--quiet']: sys.exit(int(os.environ['STAGED']))
elif a == ['diff','--name-only','-z']: sys.stdout.write(os.environ['DIRTY'] + ('\\0' if os.environ['DIRTY'] else ''))
elif a == ['ls-files','--others','--exclude-standard','-z']: pass
else: sys.exit('Unexpected Git operation in refusal test')
''')
            fake.chmod(0o755)
            log = root / 'calls'
            env = dict(os.environ, PATH=str(bindir) + os.pathsep + os.environ['PATH'],
                       BRANCH=branch, STAGED=staged, DIRTY=dirty, CALL_LOG=str(log))
            result = subprocess.run(['bash', str(root / 'publish.sh'), '2026-09-05'], env=env, capture_output=True, text=True)
            calls = log.read_text()
            self.assertNotEqual(result.returncode, 0)
            self.assertNotIn('push', calls)
            self.assertNotIn('add --', calls)
            return result.stderr

    def test_feature_branch_cannot_publish(self):
        self.assertIn('only from main', self.attempt(branch='feat/example'))

    def test_preexisting_staged_changes_cannot_publish(self):
        self.assertIn('existing staged changes', self.attempt(staged='1'))

    def test_structural_changes_require_pr(self):
        self.assertIn('Non-edition changes need a PR', self.attempt(dirty='template.html'))

    def test_split_outputs_are_staged_on_content_publish(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            shutil.copy(ROOT / 'publish.sh', root)
            for folder in ('briefs', 'research', 'editions', 'deep-dives', 'tests', 'bin'):
                (root / folder).mkdir()
            (root / 'briefs/2026-09-06.md').write_text('Fixture')
            (root / 'research/2026-09-06.md').write_text('Evidence fixture')
            (root / 'build.py').write_text('from pathlib import Path\nfor name in ["index.html", "deep-dives.html", "archive.html", "latest.md", "edition-manifest.json", "editions/2026-09-06.html", "deep-dives/2026-09-06.html"]: Path(name).write_text("Fixture")\n')
            (root / 'tests/test_fixture.py').write_text('import unittest\nclass Fixture(unittest.TestCase):\n    def test_fixture(self): self.assertTrue(True)\n')
            fake = root / 'bin/git'
            fake.write_text('''#!/usr/bin/env python3
import os, sys
from pathlib import Path
a=sys.argv[1:]
with Path(os.environ['CALL_LOG']).open('a') as f: f.write(' '.join(a) + '\\n')
if a == ['branch', '--show-current']: print('main')
elif a == ['diff', '--cached', '--quiet']: sys.exit(1 if Path('staged').exists() else 0)
elif a == ['diff', '--name-only', '-z']: sys.stdout.write('deep-dives.html\\0deep-dives/2026-09-06.html\\0')
elif a == ['ls-files', '--others', '--exclude-standard', '-z']: pass
elif a[0] == 'add': Path('staged').touch()
elif a[0] in ('commit', 'push'): pass
else: sys.exit('Unexpected Git operation')
''')
            fake.chmod(0o755)
            log = root / 'calls'
            env = dict(os.environ, PATH=str(root / 'bin') + os.pathsep + os.environ['PATH'], CALL_LOG=str(log))
            result = subprocess.run(['bash', str(root / 'publish.sh'), '2026-09-06'], env=env, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            calls = log.read_text()
            staged = next(x for x in calls.splitlines() if x.startswith('add --'))
            self.assertIn('deep-dives.html', staged)
            self.assertIn(' deep-dives ', staged)
            self.assertIn('research/2026-09-06.md', staged)
            self.assertIn('push origin main', calls)
