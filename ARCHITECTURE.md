# Architecture

## Layers and trust boundaries

| Component | Responsibility | M1 status |
| --- | --- | --- |
| WISH Android Installer | Onboarding, device checks, supported provisioning route, permissions | Design; executable deployment is blocked on M2 |
| WISH Linux Runtime | Versioned userspace, process owner, explicit paths, bounded jobs | Reference patterns inspected; portable contracts only |
| WISH Codex Integration | Authentication and one managed session, availability, queue receipts | Reference verified; new adapter proposed |
| WISH Software Capability Registry | Package/tool metadata, ABI, provenance, bounded verification | Portable validator implemented |
| WISH Autonomous Tool Selection | Evidence-aware bilingual hints; Codex makes final decisions | Portable deterministic hint function implemented |
| WISH Python Engineering Environments | Independent dev/AI/math environments and interpreters | Reference verified; portable provisioning proposed |
| WISH Git/GitHub Integration | Optional per-user authentication, explicit repository operations | Design; no credential broker implemented |
| WISH Graphical Hub | Wish input, actual events, project/capability/resource views | Reference verified; new UI port proposed |
| WISH Project Manager | Project lifecycle, idempotency, checks and completion | Pure lifecycle/artifact contracts implemented |
| WISH Application Launcher | Fixed registrations, owned process and HTTP health checks | Reference verified; portable implementation proposed |
| WISH Artifact Delivery | Contained paths, integrity, browser downloads and Android export | Pure integrity contract implemented; Android export proposed |
| WISH Diagnostics and Recovery | Resource policy, redacted diagnostics, restart and repair | Pure budget planning implemented; full service proposed |

The APK executes Android framework code with its own UID. A Termux companion owns its own private Linux processes and files. WISH cannot read Termux private directories directly. Any bridge must use a supported, authenticated, narrowly scoped interface with explicit user consent. A localhost TCP connection alone is not an identity boundary between Android apps.

## Runtime route decision

**First prototype candidate:** WISH UI plus a supported Termux-owned runtime, using an explicit bridge, not a renamed copy of the Termux data tree. This is not implemented and requires M2 tests of supported intents/permissions and lifecycle behavior.

**Standalone APK candidate:** an app-owned execution substrate with packaged Android-compatible native components. Android execution policy, bionic/glibc separation, PRoot behavior and distribution/update constraints must be proven before this route is selected. Do not sidestep current target API requirements by quietly using an old target.

No route copies the reference device's installed prefixes or credentials. The shell's simulated root user is not Android root.

## Data and execution

The controller stores session bindings and authentication privately on-device. Repository examples are synthetic and use logical environment names. Runtime adapters resolve absolute interpreter paths locally and never mix Android bionic binaries, Linux glibc environments and workstation executables.

One coordination owner holds a process/session lease. Hub submission checks availability, validates the wish and idempotency key, performs a resource preflight and obtains a real queue receipt. A durable job ledger records transitions and append-only events. Observed child processes supplement the ledger but do not establish success.

Completion requires passing recorded checks and verified contained artifacts. An HTTP launcher accepts a registered application ID and an action; it never accepts an arbitrary command string from a browser. Exports use bounded project paths and attachment delivery. Android sharing will use a content URI or Storage Access Framework.

## Recovery and updates

Interrupted downloads use validated staging. A manifest is authenticated and includes hashes, sizes, ABI/libc/page requirements, source and licensing metadata. Successful activation changes a version pointer atomically. Checkpoints permit recovery without overwriting projects. App updates, runtime updates, Python package installs and Codex updates are independent operations; none is an implicit global upgrade.

M1 implements no downloader, package manager, terminal emulator, account login, Android service, remote job executor or APK build. See docs/ADR-0001-runtime-boundary.md for the feasibility decision and installer/README.md for the planning contract.
