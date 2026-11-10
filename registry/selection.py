"""Deterministic hints, never a shell, installer, model or authorization decision."""
import re
import unicodedata

from .catalog import instant, validate


def normalize(value):
    return ''.join(c for c in unicodedata.normalize('NFKD', value.casefold()) if not unicodedata.combining(c))


def select(wish, catalog, *, device, runtime, architecture, as_of):
    validate(catalog)
    if not isinstance(wish, str) or not wish.strip() or len(wish) > 16000:
        raise ValueError('Give a nonempty bounded wish.')
    moment = instant(as_of)
    clean = normalize(wish)
    candidates = []
    for record in catalog['capabilities']:
        if record['runtime'] != runtime or record['architecture'] != architecture:
            continue
        matched = [key for key in record['keywords']
                   if re.search(r'(?<!\w)' + re.escape(normalize(key)) + r'(?!\w)', clean)]
        if not matched:
            continue
        evidence = record['verification']
        ready = (evidence['status'] == 'passed' and evidence['scope'] == 'local_device'
                 and evidence['device'] == device and instant(evidence['checked_at']) <= moment
                 and moment < instant(evidence['expires_at']))
        action = 'use_verified' if ready else ('repair_or_alternative' if evidence['status'] == 'failed'
                                               else 'probe_existing')
        if evidence['status'] == 'proposed':
            action = 'evaluate_missing'
        candidates.append({'id': record['id'], 'environment': record['environment'], 'matched': matched,
                           'score': len(matched), 'ready': ready, 'next_action': action})
    candidates.sort(key=lambda item: (-item['score'], not item['ready'], item['id']))
    return {'candidates': candidates, 'next_action': candidates[0]['next_action'] if candidates else 'codex_interpret',
            'executes_software': False, 'installs_software': False}
