# Development roadmap

| Milestone | Deliverable | Exit evidence | Current state |
| --- | --- | --- | --- |
| M1 Repository and architecture | Public GitHub foundation, reviewed design, tested portable contracts | Committed file inventory, privacy checks, tests, verified remote | Local work in this delivery; remote status reported separately |
| M2 Android compatibility investigation | Ryzen toolchain lock and an ARM64 test harness, runtime route decision | Clean-device ABI/page-size/native-exec/companion/storage/lifecycle report | Next |
| M3 Linux userspace installation prototype | Signed-manifest staging, bounded extraction, activation and rollback | Repeated install, interrupted download, tamper and low-storage tests | Planned; depends on M2 go decision |
| M4 Codex integration prototype | Supported user authentication, one coordinator/session adapter | Receipt-versus-execution distinction, account expiry and duplicate protection | Planned; reference patterns verified |
| M5 Software capability registry | Targeted inventory service and bounded probes | Device-specific freshness/invalidation tests, no metadata-only readiness claims | Portable contracts in M1; live service planned |
| M6 WISH graphical interface | Android onboarding and adapted mobile Hub | Romanian/English wish, real events, artifacts, accessible controls | Reference Hub verified; product UI planned |
| M7 Android APK packaging | Reproducible signed ARM64 APK and update policy | Toolchain/build hashes, native page/ABI checks, redacted package scan | Planned |
| M8 Installation on a clean test device | Reproducible onboarding without pre-existing lab state | No-root install record, supported prompts, offline/interruption recovery | Planned |
| M9 End-to-end autonomous engineering demonstration | Wish to tested usable software through product UI | Full request/event/check/artifact chain; no fabricated progress | Reference demonstrated; clean WISH product pending |
| M10 Cross-device compatibility testing | Versioned support matrix and documented exclusions | Multiple vendors/API levels/page sizes, thermal/process/storage cases | Planned |

## Immediate next engineering work

M2 starts on the Ryzen workstation. Record Windows/PowerShell/JDK/SDK versions and select an internally compatible build tuple. Generate a small Android-native compatibility harness targeting current requirements. Test a packaged ARM64 executable, app-private writable execution behavior, a supported Termux bridge and process death recovery. Use a clean test device/profile where possible; do not reset or mutate the working Vivo lab.

The route decision must state what failed as well as what passed. If the companion bridge cannot meet the desired experience, explicitly revise the product flow before building the installer. Do not claim that more UI code resolves a platform execution restriction.

Each milestone keeps its own implementation status, automated evidence, user verification and remaining limitations. A green portable unit suite never promotes M2–M10 to complete.
