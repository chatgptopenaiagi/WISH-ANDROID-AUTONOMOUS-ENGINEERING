import hashlib
from pathlib import Path
import tempfile
import unittest

from installer.plan import GIB, MIB, plan_install
from runtime.jobs import transition, verify_artifacts

ROOT = Path(__file__).resolve().parents[1]


class LifecycleTests(unittest.TestCase):
    def test_acceptance_execution_completion_are_separate(self):
        self.assertEqual(transition('prepared', 'queued', receipt_confirmed=True), 'queued')
        self.assertEqual(transition('queued', 'running', execution_confirmed=True), 'running')
        self.assertEqual(transition('running', 'complete', checks=['PASS'], artifacts_verified=True), 'complete')

    def test_no_receipt_no_queue_claim(self):
        with self.assertRaises(ValueError):
            transition('prepared', 'queued')

    def test_no_execution_confirmation_no_running_claim(self):
        with self.assertRaises(ValueError):
            transition('queued', 'running', receipt_confirmed=True)

    def test_unknown_delivery_and_completed_jobs_are_not_retried(self):
        self.assertEqual(transition('prepared', 'delivery_unknown'), 'delivery_unknown')
        for previous, following in [('delivery_unknown', 'queued'), ('complete', 'running'), ('queued', 'complete')]:
            with self.assertRaises(ValueError):
                transition(previous, following, receipt_confirmed=True, execution_confirmed=True)

    def test_completion_requires_all_checks_and_artifacts(self):
        for checks, verified in [([], True), (['PASS', 'FAIL'], True), (['PASS'], False)]:
            with self.assertRaises(ValueError):
                transition('running', 'complete', checks=checks, artifacts_verified=verified)


class ArtifactTests(unittest.TestCase):
    def setUp(self):
        (ROOT / '.local/tests').mkdir(parents=True, exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(dir=ROOT / '.local/tests')
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.project = self.root / 'project'
        self.project.mkdir()
        self.file = self.project / 'result.txt'
        self.file.write_text('Synthetic result')
        self.record = {'path': 'result.txt', 'sha256': hashlib.sha256(self.file.read_bytes()).hexdigest()}

    def test_real_file_hash(self):
        self.assertEqual(verify_artifacts(self.project, [self.record]), ['result.txt'])

    def test_tamper_is_detected(self):
        self.file.write_text('Changed')
        with self.assertRaises(ValueError):
            verify_artifacts(self.project, [self.record])

    def test_path_escape_and_absolute_paths_rejected(self):
        for name in ['../outside.txt', str(self.file.resolve()), 'C:\\private.txt', 'folder\\file.txt']:
            with self.assertRaises(ValueError):
                verify_artifacts(self.project, [{**self.record, 'path': name}])

    def test_symlink_escape_rejected(self):
        outside = self.root / 'outside.txt'
        outside.write_text('Outside project')
        link = self.project / 'escape.txt'
        try:
            link.symlink_to(outside)
        except OSError:
            self.skipTest('Symlinks unavailable in this test environment.')
        with self.assertRaises(ValueError):
            verify_artifacts(self.project, [{**self.record, 'path': 'escape.txt'}])

    def test_empty_artifacts_rejected(self):
        with self.assertRaises(ValueError):
            verify_artifacts(self.project, [])


class InstallerPlanningTests(unittest.TestCase):
    def plan(self, **overrides):
        values = dict(free_storage=20 * GIB, available_ram=1024 * MIB,
                      download_bytes=GIB, unpacked_bytes=2 * GIB, rollback_bytes=GIB)
        return plan_install(**{**values, **overrides})

    def test_peak_space_not_just_archive_size(self):
        result = self.plan()
        self.assertTrue(result['allowed_to_plan'])
        self.assertEqual(result['peak_storage_required'], 14 * GIB)
        self.assertFalse(result['installs_software'])

    def test_reserve_preserved(self):
        result = self.plan(free_storage=13 * GIB)
        self.assertFalse(result['allowed_to_plan'])
        self.assertIn('insufficient_storage', result['failures'])

    def test_memory_limit(self):
        self.assertIn('insufficient_ram', self.plan(available_ram=767 * MIB)['failures'])

    def test_invalid_resource_types_rejected(self):
        for value in [-1, True, 1.5]:
            with self.assertRaises(ValueError):
                self.plan(download_bytes=value)
