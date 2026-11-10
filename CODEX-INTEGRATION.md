# Codex integration

## Verified reference boundary

The Vivo reference uses the existing SENTINEL-managed launcher and one already bound Codex session. The wish workflow queues a natural-language message, saves the original delivery receipt, records checks and verifies artifacts. The Hub checks the existing server's loaded-thread state through a read-only local control connection before accepting a submission. This is verified behavior of the installed reference version, not a promised stable API for every future Codex release.

No Codex upgrade, installation, new session or live model call is part of this repository's M1 checks. No native Codex binary, configuration, authentication file or session state is included.

## Portable adapter to implement

The runtime controller owns a single session lease. A version adapter detects the installed CLI and supported protocol, probes availability, and dispatches only through the selected SENTINEL execution path. Missing, stale or ambiguous session ownership disables submission and displays recovery instructions; process presence alone is insufficient.

Keep a transport interface separate from job policy. The current reference's queue command is an adapter detail, not a portable promise. A future supported app-server integration can expose structured lifecycle events, but must remain under the same coordination owner. Verify version-specific framing and capabilities before use. Do not start a second server/session as a connectivity test. [Official App Server documentation](https://learn.chatgpt.com/docs/app-server)

An accepted receipt produces `queued`, not `running` or `complete`. Timeouts can produce `delivery_unknown`; do not blindly retry. Reuse an idempotency key and inspect persisted delivery before another attempt. The M1 lifecycle module validates these distinctions without making a network connection.

## Authentication and account ownership

The user authenticates their own account through a supported Codex flow. Account access, model availability, quotas and internet access are separate from having a CLI binary. Never bundle a shared account or extract authentication from the Vivo reference. A third-party Android wrapper's exact sign-in experience must be validated against the supported product integration; this design does not implement an OAuth client or token exchange. [Official authentication documentation](https://learn.chatgpt.com/docs/auth)

Private credentials stay with the owning runtime and are excluded from logs, exports, backups and Git. An Android Keystore-backed bridge may protect app-owned secrets; it does not automatically make another app's private files accessible. GitHub authentication is separate and optional.

## Environment propagation

Activation in an interactive shell does not retroactively alter a running Codex process. Each command must receive an explicit interpreter/environment mapping. Keep dev, AI and math prefixes separate, suppress user-site/PYTHONPATH leakage, limit numerical threads, and record the actual interpreter used. Resolve mappings locally rather than committing device paths.

## Completion and recovery

Capture genuine execution/test events and preserve failed attempts. Report implementation failures, authentication expiry, process death and interrupted jobs honestly. Completion requires at least one current passing check and intact contained artifacts. Recover an existing session through its coordinator; a lost UI connection is not permission to spawn competing agents.
