# SENTINEL integration

SENTINEL remains the execution and coordination layer of the reference installation. WISH is an interface and engineering product around that boundary. It must preserve monitoring, launch routing, capability records and session ownership.

## Responsibilities

- Provide a fresh session brief and targeted registered-root capability inventory.
- Keep execution evidence distinct from installed-package metadata.
- Coordinate the one bound Codex session and expose honest health/recovery state.
- Select existing absolute interpreters locally and preserve independent runtime prefixes.
- Reconcile relevant records after authorized runtime changes without erasing evidence.

## Adapter contract

At startup, read generation/time/error indicators and verify freshness. Look up an existing capability before proposing a dependency. A stale relevant probe must be rechecked through the installed coordinator before relying on it. A metadata refresh does not prove functional behavior.

The Android port needs a versioned adapter returning structured session status, queue receipts and capability evidence. The bridge must authenticate its caller and expose a narrow operation set. It must not offer an arbitrary browser-supplied shell string, raw unrestricted RPC forwarding or a second independent scheduler.

Reference source patterns are described in docs/VIVO-REFERENCE.md. SENTINEL source, runtime files, session brief contents, socket locations and private configuration are not copied here. No global Sentinel record is refreshed or changed by M1.

The portable runtime contracts in this repository do not implement SENTINEL. Integration tests against the real coordinator belong to M4/M9 and must preserve the existing launcher. Distribution rights, supported versioning and provisioning of a reusable coordinator require explicit review before APK packaging.
