"""Inspect staged/tracked Git blobs; print rule names and paths, never secret values."""
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from registry.catalog import validate

PRIVATE_PARTS = {'.local', '.codex', '.sentinel', 'sessions', 'state', 'run', 'logs', 'caches',
                 'rootfs', 'prefix', 'sdk', '.venv', 'node_modules', '.gradle', '__pycache__', 'build', 'dist'}
PRIVATE_NAMES = {'auth.json', 'credentials.json', 'local.properties', 'google-services.json', 'id_rsa', 'id_ed25519'}
PATTERNS = {
    'github_token': re.compile(r'gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}'),
    'provider_key': re.compile(r'sk-[A-Za-z0-9_-]{20,}'),
    'private_key': re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),
    'session_identifier': re.compile(r'\b[0-9a-fA-F]{8}-(?:[0-9a-fA-F]{4}-){3}[0-9a-fA-F]{12}\b'),
    'device_home_path': re.compile(r'/(?:' + r'root|home' + r')/|[A-Za-z]:\\Users\\'),
    'android_private_path': re.compile(r'/data/(?:data|user)/'),
    'live_loopback_port': re.compile(r'127\.0\.0\.1:[0-9]{2,5}'),
}
REQUIRED = ['README.md', 'ARCHITECTURE.md', 'PRODUCT-VISION.md', 'ANDROID-INSTALLATION-DESIGN.md',
            'CODEX-INTEGRATION.md', 'SOFTWARE-CAPABILITY-REGISTRY.md', 'SENTINEL-INTEGRATION.md',
            'HARDWARE-COMPATIBILITY.md', 'DEVELOPMENT-ROADMAP.md', 'TESTING-STRATEGY.md',
            'docs/VIVO-REFERENCE.md', 'docs/M1-REPORT.md', 'android/README.md', 'runtime/jobs.py',
            'installer/plan.py', 'hub/README.md', 'registry/catalog.py', 'registry/capability.schema.json',
            'tests/test_registry.py', 'scripts/Test-Repository.ps1', 'evidence/vivo-reference.json',
            '.github/workflows/ci.yml', '.gitignore']


def findings(path, content):
    parts = Path(path).parts
    result = []
    if (any(part in PRIVATE_PARTS for part in parts) or Path(path).name in PRIVATE_NAMES
            or Path(path).name.startswith('.env') or re.search(r'\.(?:log|sqlite\w*|db|pem|key|keystore|jks|apk|aab)$', path)):
        result.append('private_or_generated_path')
    if len(content) > 1024 * 1024:
        result.append('oversized_unreviewed_blob')
    try:
        value = content.decode('utf-8')
    except UnicodeDecodeError:
        return result + ['binary_or_non_utf8_blob']
    result.extend(label for label, pattern in PATTERNS.items() if pattern.search(value))
    return result


def index_blobs(root):
    listing = subprocess.check_output(['git', 'ls-files', '--stage', '-z'], cwd=root)
    entries = []
    for entry in listing.split(b'\0'):
        if not entry:
            continue
        metadata, raw_path = entry.split(b'\t', 1)
        mode, digest, stage = metadata.decode().split()
        path = raw_path.decode('utf-8')
        if stage != '0' or mode not in {'100644', '100755'} or any(ord(c) < 32 for c in path):
            raise ValueError('Unmerged, symlink, submodule or invalid index path: ' + repr(path))
        entries.append((path, digest))
    if not entries:
        raise ValueError('No files in Git index; stage the reviewed source before checking.')
    output = subprocess.check_output(['git', 'cat-file', '--batch'], cwd=root,
                                     input=('\n'.join(digest for _, digest in entries) + '\n').encode())
    cursor = 0
    result = {}
    for path, expected in entries:
        end = output.index(b'\n', cursor)
        digest, kind, length = output[cursor:end].decode().split()
        if digest != expected or kind != 'blob':
            raise ValueError('Unexpected Git object.')
        start = end + 1
        cursor = start + int(length)
        result[path] = output[start:cursor]
        cursor += 1
    return result


def check(blobs):
    errors = [(path, rule) for path, content in blobs.items() for rule in findings(path, content)]
    errors.extend((path, 'required_file_missing') for path in REQUIRED if path not in blobs)
    for path, content in blobs.items():
        if not path.endswith('.md'):
            continue
        for link in re.findall(r'(?<!!)\[[^\]]+\]\(([^)]+)\)', content.decode('utf-8', errors='replace')):
            link = link.split('#', 1)[0]
            if not link or '://' in link or link.startswith('mailto:'):
                continue
            target = (ROOT / Path(path).parent / link).resolve()
            if not target.is_relative_to(ROOT) or str(target.relative_to(ROOT)).replace('\\', '/') not in blobs:
                errors.append((path, 'broken_local_link:' + link))
    try:
        validate(json.loads(blobs.get('registry/examples/minimal.json', b'null')))
    except (ValueError, TypeError) as error:
        errors.append(('registry/examples/minimal.json', type(error).__name__))
    return errors


def main():
    try:
        blobs = index_blobs(ROOT)
        errors = check(blobs)
    except (ValueError, subprocess.CalledProcessError) as error:
        print('Repository check failed:', str(error))
        return 1
    for path, rule in errors:
        print(path + ': ' + rule)
    print(json.dumps({'files_checked': len(blobs), 'findings': len(errors), 'source': 'Git index blobs'}))
    return bool(errors)


if __name__ == '__main__':
    raise SystemExit(main())
