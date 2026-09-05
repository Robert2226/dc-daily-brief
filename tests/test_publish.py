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
