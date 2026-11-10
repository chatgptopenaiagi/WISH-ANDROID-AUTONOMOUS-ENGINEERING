# Android installation design

**Status: proposed. No clean-device installation or APK build is claimed.**

## Feasibility gate

Android apps targeting API 29+ cannot assume they can execute arbitrary files from a writable app home. Android's documented execution restrictions apply before PRoot is involved. A conventional untar-rootfs-and-exec installer is therefore not established for a new modern-target APK. [Android execution policy](https://developer.android.com/about/versions/10/behavior-changes-10)

Termux uses Android-native binaries and environment-specific execution support. Its package paths and behavior depend on its app identity. Reusing Termux packages in a differently named APK requires more than changing paths. Investigate a supported companion relationship first; an independent runtime is a separate feasibility project. [Termux execution environment](https://github.com/termux/termux-packages/wiki/Termux-execution-environment)

## Framework versus userspace

| Android framework / NDK | Linux userspace |
| --- | --- |
| Kotlin, Compose, Activity, permissions and lifecycle | Shell, Python, GCC, Node, Git and package metadata |
| App UID, app-specific storage, content URI export | Guest paths and independent interpreter prefixes |
| Android-compatible ARM64 native libraries using bionic | Selected glibc/musl userspace executables under a proven execution route |
| Notifications, supported foreground work, Keystore | Supervised processes without assuming systemd or real root |

An ARM64 ELF file is not automatically compatible with Android's ABI/libc, loader, page size or SELinux policy.

## Provisioning sequence to prototype

1. Inspect supported ABIs, API level, page size, execution capability, RAM and free storage using appropriate Android APIs. Present failures before downloads.
2. Choose a verified runtime route. For a companion, request supported integration permission explicitly and let the runtime owner create its own files.
3. Obtain a versioned runtime manifest over authenticated transport. Check signature, hashes, sizes, platform constraints and licensing before activation.
4. Stage downloads with space for extraction and rollback. Reject archive traversal, escaping links and decompression bombs; M1 does not implement extraction.
5. Run a minimal native probe, Python hello-world, filesystem test and loopback health check under the chosen owner.
6. Add minimal developer tools only for an active need. Resolve individual compatible packages, not an indiscriminate copy of Anaconda/Miniforge.
7. Configure the version-tested SENTINEL/Codex adapter without creating a competing session. The user authenticates their own Codex account.
8. Inventory verified capabilities, open the Hub and run a bounded example with a recorded result.

M1's `installer.plan` only evaluates a supplied memory/storage budget and creates a data plan. It downloads and installs nothing.

## Kotlin / Compose / Gradle strategy

Use Kotlin and Jetpack Compose for onboarding, diagnostics and native navigation. A browser Hub can be opened externally first. Evaluate an embedded WebView only after testing origin rules, navigation restrictions, file export and the absence of a broad JavaScript-to-shell bridge. [Compose setup](https://developer.android.com/develop/ui/compose/setup)

On the Ryzen workstation use Android Studio/SDK tools and a compatible JDK, with PowerShell 7 for repeatable commands. At M2/M7 select and record an exact AGP/Gradle/Kotlin/SDK/NDK tuple; then commit the generated Gradle wrapper and its checksum. No guessed build tuple or nonfunctional wrapper is included now. Package only `arm64-v8a` initially and validate native alignment and dependencies. [Android ABI guide](https://developer.android.com/ndk/guides/abis), [page-size compatibility](https://developer.android.com/guide/practices/page-sizes)

## Lifetime, storage and updates

Long-running engineering is subject to Android background and vendor battery policy. A foreground notification is not a guarantee of unlimited CPU time; choose a legitimate service type and implement cancellation/checkpoint/recovery. For example, applicable dataSync/mediaProcessing services have time limits; do not label arbitrary builds as media processing. [Service timeouts](https://developer.android.com/develop/background-work/services/fgs/timeout)

Keep runtime data private to its owning app, projects persistent, and disposable downloads/caches bounded. Export documents with the system picker or content URIs, not broad storage access. Explain that uninstall can remove app-private projects and provide an explicit export/backup path. [App-specific storage](https://developer.android.com/training/data-storage/app-specific)

Validate network security on the selected target. A local HTTP Hub must have a loopback-only exception where required, not globally permitted cleartext, and must authenticate mutating requests. Runtime components and account state are excluded from APK backups and repository exports. Do not silently update Codex or unrelated environments. [Network security configuration](https://developer.android.com/privacy-and-security/security-config)
