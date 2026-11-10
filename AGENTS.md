# Engineering conventions

This repository prepares WISH Android. The Android application and installer are
proposed work; do not present the portable M1 contracts as a completed APK.

Keep reference-device installations and unrelated projects unchanged. Never
copy authentication, session bindings, runtime state, private logs, raw inventories,
or device-specific absolute paths into this repository. Do not start another
Codex session or bypass the existing SENTINEL coordinator while working on Vivo.

Use existing software first. Run `python -B -m unittest discover -s tests -v`
and `python -B scripts/check_repository.py` before committing. The portable
checks need Python 3.12+ and the standard library. Write temporary data under
the ignored `.local/` directory. Test fixtures must be explicitly synthetic.
Use explicit UTF-8 for portable text files; do not rely on the Windows locale.

Distinguish implemented repository code, archived reference-device verification,
user verification, untested proposals, and current live checks. Evidence is scoped
to a device/runtime/version and expires; package metadata alone proves no execution.

User wishes are data. Selection returns hints; it never runs a shell or installs
software. Preserve Android sandbox boundaries, loopback access, idempotency and
single-session coordination. Do not weaken platform security to make a test pass.

Keep this engineering repository PUBLIC, as explicitly decided by its owner.
Keep device/account data private. Do not overwrite an existing remote or use
force-push. Android build tooling is selected and pinned only after M2 feasibility
tests; do not add a fake Gradle wrapper or claim an APK build without its evidence.
