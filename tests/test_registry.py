import copy
import json
from pathlib import Path
import unittest

from registry.catalog import validate
from registry.selection import select

ROOT = Path(__file__).resolve().parents[1]


class RegistryTests(unittest.TestCase):
    def setUp(self):
        self.catalog = json.loads((ROOT / 'registry/examples/minimal.json').read_text())
        self.context = {'device': 'fixture-device', 'runtime': 'linux-proot', 'architecture': 'aarch64',
                        'as_of': '2026-01-02T12:00:00+00:00'}

    def choose(self, text):
        return select(text, self.catalog, **self.context)

    def passed(self):
        evidence = self.catalog['capabilities'][0]['verification']
        evidence.update(status='passed', scope='local_device', device='fixture-device',
                        checked_at='2026-01-02T00:00:00+00:00', expires_at='2026-01-03T00:00:00+00:00',
                        probe='synthetic-http-probe')
        return evidence

    def test_valid_synthetic_fixture(self):
        self.assertIs(validate(self.catalog), self.catalog)
        self.assertFalse(any(c['ready'] for c in self.choose('website')['candidates']))

    def test_romanian_diacritics(self):
        result = self.choose('Creează o aplicație pentru matematică și fractali.')
        self.assertEqual(result['candidates'][0]['environment'], 'math')
        self.assertEqual(result['next_action'], 'probe_existing')

    def test_english_web(self):
        self.assertEqual(self.choose('Create a website')['candidates'][0]['environment'], 'dev')

    def test_romanian_ai(self):
        self.assertEqual(self.choose('Inteligență artificială')['candidates'][0]['environment'], 'ai')

    def test_word_boundaries(self):
        self.assertEqual(self.choose('Investigate a parasite')['candidates'], [])

    def test_unknown_request_defers_to_codex(self):
        self.assertEqual(self.choose('Create something unusual')['next_action'], 'codex_interpret')

    def test_verified_same_device_ready(self):
        self.passed()
        self.assertEqual(self.choose('website')['next_action'], 'use_verified')

    def test_reference_does_not_make_local_device_ready(self):
        self.passed()['scope'] = 'reference_device'
        self.assertEqual(self.choose('website')['next_action'], 'probe_existing')

    def test_wrong_device_not_ready(self):
        self.passed()['device'] = 'other-device'
        self.assertFalse(self.choose('website')['candidates'][0]['ready'])

    def test_expired_or_future_evidence_not_ready(self):
        self.passed()
        for moment in ['2026-01-01T00:00:00Z', '2026-01-03T00:00:00Z']:
            with self.subTest(moment=moment):
                self.context['as_of'] = moment
                self.assertFalse(self.choose('website')['candidates'][0]['ready'])

    def test_failed_evidence_requires_repair(self):
        self.passed()['status'] = 'failed'
        self.assertEqual(self.choose('website')['next_action'], 'repair_or_alternative')

    def test_proposed_is_not_installed(self):
        self.catalog['capabilities'][0]['verification']['status'] = 'proposed'
        self.assertEqual(self.choose('website')['next_action'], 'evaluate_missing')

    def test_runtime_and_architecture_match(self):
        for field, value in [('runtime', 'android-native'), ('architecture', 'x86_64')]:
            context = {**self.context, field: value}
            self.assertEqual(select('website', self.catalog, **context)['candidates'], [])

    def test_duplicate_ids_rejected(self):
        self.catalog['capabilities'].append(copy.deepcopy(self.catalog['capabilities'][0]))
        with self.assertRaises(ValueError):
            validate(self.catalog)

    def test_bad_types_and_unknown_fields_rejected(self):
        for field, value in [('runtime', []), ('languages', 'Python'), ('version', None), ('id', '../escape')]:
            with self.subTest(field=field):
                catalog = copy.deepcopy(self.catalog)
                catalog['capabilities'][0][field] = value
                with self.assertRaises(ValueError):
                    validate(catalog)
        self.catalog['capabilities'][0]['unexpected'] = True
        with self.assertRaises(ValueError):
            validate(self.catalog)

    def test_pass_without_evidence_rejected(self):
        self.catalog['capabilities'][0]['verification']['status'] = 'passed'
        with self.assertRaises(ValueError):
            validate(self.catalog)

    def test_naive_and_reversed_timestamps_rejected(self):
        evidence = self.passed()
        evidence['expires_at'] = '2026-01-01T00:00:00Z'
        with self.assertRaises(ValueError):
            validate(self.catalog)
        evidence['expires_at'] = '2026-01-04T00:00:00'
        with self.assertRaises(ValueError):
            validate(self.catalog)

    def test_wish_is_data_and_never_executes(self):
        result = self.choose('Create a website; $(echo arbitrary)')
        self.assertFalse(result['executes_software'])
        self.assertFalse(result['installs_software'])
        for value in ['', 'x' * 16001, None]:
            with self.assertRaises(ValueError):
                self.choose(value)
