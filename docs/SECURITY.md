# Security and publication boundaries

The Android sandbox protects app ownership; PRoot is not an additional strong
security boundary. Generated projects are isolated by directory and policy.
Untrusted generated code can affect its runtime owner's accessible files.
Do not claim VM-grade isolation or root privileges.

The runtime must expose a narrow authenticated interface. Browser mutations
require an exact allowed origin plus a token, and services bind only to loopback.
Other apps may reach loopback; local TCP is not a credential. Restrict Host, CORS,
redirects and WebView navigation. Do not expose a generic shell/RPC endpoint.

Project IDs resolve under one owned root. Reject traversal, escaping symlinks and
private file access. Verify artifact hashes at delivery and send browser files as
attachments. For Android sharing use scoped content URIs or the system picker.

Codex and GitHub authentication are separate, per-user, optional where applicable,
and kept outside Git and diagnostic exports. Diagnostics must redact session IDs,
account tokens, prompt contents and private process arguments. Exact local paths
can also disclose user/device information. Review an allowlisted summary before
export; do not recursively upload a device workspace.

Updates need authenticated manifests, hashes, bounded staging, rollback and a
record of what changed. Dependency installation is separate from APK and Codex
updates. Keep one coordination owner; uncertain delivery is reconciled rather
than automatically duplicated. No secret, package license grant or account is
provided by this repository.

The owner has explicitly selected PUBLIC repository visibility. Only reviewed
engineering source and curated evidence may be published. The publication guard scans the Git
index, not only .gitignore. Existing secrets must never be deliberately staged
as a test. Unit tests create synthetic token-like values in ignored temporary
fixtures and do not print their contents.
