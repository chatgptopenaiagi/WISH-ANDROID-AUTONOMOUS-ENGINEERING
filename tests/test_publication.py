from pathlib import Path
import tempfile
import subprocess
import unittest

from scripts.check_repository import findings, index_blobs

ROOT = Path(__file__).resolve().parents[1]


class PublicationTests(unittest.TestCase):
    def test_synthetic_secrets_are_rejected_without_echo(self):
        samples = [('gh' + 'p_' + 'x' * 32, 'github_token'),
                   ('sk-' + 'x' * 32, 'provider_key'),
                   ('a' * 8 + '-' + '-'.join(['a' * 4] * 3) + '-' + 'a' * 12, 'session_identifier')]
        for value, rule in samples:
            result = findings('docs/example.md', value.encode())
            self.assertIn(rule, result)
            self.assertNotIn(value, ' '.join(result))

    def test_machine_paths_rejected(self):
        for value in ['/' + 'root' + '/private/file', '/' + 'data' + '/data/private/file']:
            self.assertTrue(findings('docs/example.md', value.encode()))

    def test_private_files_and_binary_outputs_rejected(self):
        for name in ['.local/state.json', 'auth.json', '.env', 'sessions/turn.json', 'build/app.apk']:
            self.assertIn('private_or_generated_path', findings(name, b'{}'))
        self.assertIn('binary_or_non_utf8_blob', findings('image.bin', b'\xff\xfe'))

    def test_plain_synthetic_document_allowed(self):
        self.assertEqual(findings('docs/example.md', b'No device configuration here.'), [])

    def test_index_content_is_scanned_even_when_worktree_changes(self):
        (ROOT / '.local/tests').mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=ROOT / '.local/tests') as folder:
            subprocess.run(['git', 'init', '-q', folder], check=True)
            path = Path(folder) / 'sample.md'
            secret = ('gh' + 'p_' + 'x' * 32).encode()
            path.write_bytes(secret)
            subprocess.run(['git', 'add', 'sample.md'], cwd=folder, check=True)
            path.write_text('Changed only in worktree')
            blobs = index_blobs(folder)
            self.assertEqual(blobs['sample.md'], secret)
            self.assertIn('github_token', findings('sample.md', blobs['sample.md']))
