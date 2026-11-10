# Testing strategy

## Evidence classes

| Class | Meaning |
| --- | --- |
| repository_automated | Code executed for this repository under its stated interpreter/platform |
| reference_automated | Archived Vivo reference tests; no automatic claim for another device |
| user_verified | A human physically confirmed the named operation on a specified reference device |
| synthetic | Contract/test data, never a device capability assertion |
| proposed | A design or test plan with no implementation evidence |

All evidence needs scope, time, version and limitations. Installed metadata, an API receipt, simulated touch, physical touch and actual output are distinct. Failed attempts remain in local development evidence; publish only curated summaries.

## M1 automated checks

Use Python 3.12+ standard-library unittest. Cover strict catalog validation, bilingual hints, stale/foreign/failed evidence, runtime mismatch, valid lifecycle transitions, uncertain delivery, no completion without checks, artifact tampering/path escape and resource budgeting. Tests use repository-local temporary files and synthetic records; they never call Codex or install anything.

`scripts/check_repository.py` inspects Git's staged/tracked paths for private files, credentials, session identifiers and machine-specific absolute paths, checks required documentation and local Markdown links, and validates JSON fixtures. It reports paths/rule names without echoing secret values. It is a deterministic publication guard, not a proof that every possible secret is detectable.

The GitHub workflow runs portable checks on Linux and Windows, with read-only repository permissions and pinned action revisions. PowerShell helper execution is checked by the Windows job. Until that job executes, workstation behavior remains unverified. CI does not build an APK or authenticate Codex.

## Android gates

M2/M3: native execution, ABI/libc/page size, companion permission denial, storage boundaries, signature/hash failures, interrupted extraction, rollback, uninstall/export behavior and no-root operation.

M4/M5: availability failure, stale binding, one session under concurrent requests, uncertain receipt, account expiry, explicit interpreter propagation, capability invalidation and failed probe preservation.

M6/M9: actual mobile browser/WebView automation, narrow viewport, input language, real event stream, duplicate taps, error recovery, registered application ownership/HTTP health and artifact download/export. Physical touchscreen verification is separate. A small bounded wish must produce software that runs and passes checks, not only source files.

M7/M8/M10: reproducible workstation build, signed-package provenance, clean install, reboot/process death, background policy, screen-off, low memory/storage, thermal pressure and multiple ARM64 vendors/API/page configurations. No universal support claim before the matrix exists.

## Preservation

During M1, compare selected reference source/configuration hashes before and after read-only inspection. Keep that detailed private baseline outside tracked files. Curated summaries may record the result and count, without device paths or account state. Do not touch DRAGONHYDRA or start additional agents/sessions.
