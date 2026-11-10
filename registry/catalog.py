"""Validate small portable catalogues without importing or executing their tools."""
from datetime import datetime
import re

STATES = {'metadata_only', 'passed', 'failed', 'proposed'}
SCOPES = {'synthetic', 'reference_device', 'local_device'}
RUNTIMES = {'linux-proot', 'android-native', 'windows'}
FIELDS = {'id', 'name', 'version', 'runtime', 'architecture', 'environment', 'languages',
          'dependencies', 'use_cases', 'limitations', 'keywords', 'verification'}
EVIDENCE_FIELDS = {'status', 'scope', 'device', 'checked_at', 'expires_at', 'probe'}


def instant(value):
    if not isinstance(value, str):
        raise ValueError('Expected an ISO timestamp.')
    try:
        result = datetime.fromisoformat(value)
    except ValueError as error:
        raise ValueError('Invalid ISO timestamp.') from error
    if result.tzinfo is None or result.utcoffset() is None:
        raise ValueError('Timestamp must include timezone.')
    return result


def text(value):
    return isinstance(value, str) and bool(value.strip()) and len(value) <= 2000


def validate(catalog):
    if not isinstance(catalog, dict) or set(catalog) != {'schema_version', 'generation', 'capabilities'}:
        raise ValueError('Invalid catalogue envelope.')
    if type(catalog['schema_version']) is not int or catalog['schema_version'] != 1 or not text(catalog['generation']):
        raise ValueError('Unsupported catalogue version/generation.')
    records = catalog['capabilities']
    if not isinstance(records, list) or len(records) > 10000:
        raise ValueError('Capabilities must be a bounded list.')
    seen = set()
    for record in records:
        if not isinstance(record, dict) or set(record) != FIELDS:
            raise ValueError('Invalid capability fields.')
        identifier = record['id']
        if not isinstance(identifier, str) or not re.fullmatch(r'[a-z][a-z0-9_.-]{0,79}', identifier):
            raise ValueError('Invalid capability ID.')
        if identifier in seen:
            raise ValueError('Duplicate capability ID.')
        seen.add(identifier)
        for field in ['name', 'version', 'architecture', 'environment']:
            if not text(record[field]):
                raise ValueError('Invalid capability text: ' + field)
        if not isinstance(record['runtime'], str) or record['runtime'] not in RUNTIMES:
            raise ValueError('Unknown execution runtime.')
        for field in ['languages', 'dependencies', 'use_cases', 'limitations', 'keywords']:
            values = record[field]
            if not isinstance(values, list) or len(values) > 200 or not all(text(item) for item in values):
                raise ValueError('Invalid capability list: ' + field)
        evidence = record['verification']
        if not isinstance(evidence, dict) or set(evidence) != EVIDENCE_FIELDS:
            raise ValueError('Invalid evidence fields.')
        if (not isinstance(evidence['status'], str) or evidence['status'] not in STATES
                or not isinstance(evidence['scope'], str) or evidence['scope'] not in SCOPES or not text(evidence['device'])):
            raise ValueError('Invalid evidence status/scope/device.')
        for field in ['checked_at', 'expires_at']:
            if evidence[field] is not None:
                instant(evidence[field])
        if evidence['probe'] is not None and not text(evidence['probe']):
            raise ValueError('Invalid probe label.')
        if evidence['status'] in {'passed', 'failed'} and (evidence['checked_at'] is None or not text(evidence['probe'])):
            raise ValueError('Execution evidence requires a timestamp and probe.')
        if evidence['status'] == 'passed' and evidence['expires_at'] is None:
            raise ValueError('Passing evidence requires an expiry.')
        if evidence['expires_at'] is not None:
            if evidence['checked_at'] is None or instant(evidence['expires_at']) <= instant(evidence['checked_at']):
                raise ValueError('Expiry must follow verification time.')
    return catalog
