"""Pure lifecycle validation and contained on-disk artifact integrity checks."""
import hashlib
from pathlib import Path, PurePosixPath

TRANSITIONS = {
    'prepared': {'queued', 'delivery_unknown', 'delivery_failed'},
    'queued': {'running', 'interrupted'},
    'running': {'complete', 'failed', 'interrupted'},
    'delivery_unknown': set(), 'delivery_failed': set(),
    'complete': set(), 'failed': set(), 'interrupted': set(),
}


def transition(previous, following, *, receipt_confirmed=False, execution_confirmed=False,
               checks=(), artifacts_verified=False):
    if previous not in TRANSITIONS or following not in TRANSITIONS[previous]:
        raise ValueError('Invalid job transition; reconciliation is required.')
    if following == 'queued' and not receipt_confirmed:
        raise ValueError('Queue acceptance requires a receipt.')
    if following == 'running' and not execution_confirmed:
        raise ValueError('Execution must be confirmed separately from acceptance.')
    if following == 'complete' and (not checks or any(check != 'PASS' for check in checks) or not artifacts_verified):
        raise ValueError('Completion requires passing recorded checks and verified artifacts.')
    return following


def verify_artifacts(project, artifacts):
    root = Path(project).resolve(strict=True)
    if not root.is_dir() or not artifacts:
        raise ValueError('A project and nonempty artifact list are required.')
    verified = []
    for artifact in artifacts:
        name, expected = artifact.get('path'), artifact.get('sha256')
        if not isinstance(name, str) or not isinstance(expected, str) or len(expected) != 64:
            raise ValueError('Invalid artifact metadata.')
        relative = PurePosixPath(name)
        if relative.is_absolute() or '..' in relative.parts or '\\' in name or ':' in name:
            raise ValueError('Artifact must use a contained portable relative path.')
        target = root.joinpath(*relative.parts).resolve(strict=True)
        if not target.is_relative_to(root) or not target.is_file():
            raise ValueError('Artifact escapes project or is not a regular file.')
        digest = hashlib.sha256()
        with target.open('rb') as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b''):
                digest.update(chunk)
        if digest.hexdigest() != expected:
            raise ValueError('Artifact content does not match recorded hash.')
        verified.append(name)
    return verified
