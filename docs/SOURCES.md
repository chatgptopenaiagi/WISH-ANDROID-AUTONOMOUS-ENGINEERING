# Primary sources

Reviewed during M1 on 2026-11-10. Recheck platform and provider behavior at each
compatibility milestone. These sources document platform constraints, not a
successful WISH installation.

| Topic | Primary source | Design implication |
| --- | --- | --- |
| Modern app execution policy | [Android API 29 behavior](https://developer.android.com/about/versions/10/behavior-changes-10) | Do not assume executable downloads in app-private writable storage |
| App-private storage | [Android app-specific files](https://developer.android.com/training/data-storage/app-specific) | Separate owner UIDs, scoped export, uninstall/backup planning |
| Native interface | [Compose setup](https://developer.android.com/develop/ui/compose/setup) | Kotlin/Compose candidate, compatible workstation toolchain needed |
| ABI | [NDK ABIs](https://developer.android.com/ndk/guides/abis) | Check Android-native versus guest Linux targets |
| Native alignment | [Page sizes](https://developer.android.com/guide/practices/page-sizes) | Test 4 KiB/16 KiB native dependency compatibility |
| Lifetime | [Foreground service timeouts](https://developer.android.com/develop/background-work/services/fgs/timeout) | Checkpoint, stop and recover; no unlimited background guarantee |
| Local networking | [Network security configuration](https://developer.android.com/privacy-and-security/security-config) | Narrow loopback exceptions and authenticated local endpoints |
| Termux execution | [Termux execution environment](https://github.com/termux/termux-packages/wiki/Termux-execution-environment) | Prefix/app identity and execution mechanics must be respected |
| PRoot | [PRoot-Distro](https://github.com/termux/proot-distro) | No real root/kernel namespace isolation; no assumed systemd |
| Codex accounts | [Official authentication docs](https://learn.chatgpt.com/docs/auth) | Own supported account flow, no bundled credentials |
| Codex protocol | [Official App Server docs](https://learn.chatgpt.com/docs/app-server) | Version adapter, actual lifecycle receipts/events |
| GitHub creation | [GitHub CLI create](https://cli.github.com/manual/gh_repo_create) | Private creation requires an authenticated supported operation |
| GitHub metadata | [Repository REST API](https://docs.github.com/en/rest/repos/repos) | Verify existence, visibility and remote identity before publishing |

Local evidence sources were selected reference reports and source modules. Their
portable mapping is in VIVO-REFERENCE.md. Original files, session state and raw logs
remain private on the reference device.
