# Hardware compatibility

## Established scope

| Target | Evidence | Product conclusion |
| --- | --- | --- |
| Vivo V2450, Android 16, ARM64 with an existing Termux/Arch installation | Archived functional tests and physical user verification | Reference integration works on that installation |
| Fresh Vivo installation with WISH APK | Not tested | No installation claim |
| Other Android ARM64 phones/vendors | Not tested | M10 device matrix required |
| Ryzen Windows PC / PowerShell 7 | Intended workstation, not inspected | Build/setup guidance only |
| x86_64 emulator, other mobile ABIs, iOS | Future or test-only architecture | Separate validation, no support claim |

The reference exposes eight CPU cores and approximately 7.5 GiB RAM. Free storage and available RAM are observations, not a requirement met by every device. Archived CPU PyTorch execution does not establish usable CUDA, NPU or general-purpose Mali compute. The mathematical app's browser WebGL2 result is a distinct capability from Python GPU inference.

## Required M2 observations

- Android API level, supported ABIs, page size and native execution policy.
- Available internal storage, extraction/rollback budget, RAM and thermal behavior.
- App UID/storage boundaries and supported companion permissions.
- PRoot syscall compatibility, process lifecycle and kernel restrictions.
- Network availability, loopback access and browser/WebView behavior.
- Child process limits, cancellation, backgrounding, screen-off and restart recovery.
- Native loader/libc compatibility for every distributed binary, including transitive libraries.

Android `arm64-v8a`, Linux `aarch64` packages and Windows x64 build tools are different runtime targets. An ABI label alone is insufficient. Native components must be checked on 4 KiB and 16 KiB page configurations where supported. [NDK ABIs](https://developer.android.com/ndk/guides/abis), [Android page sizes](https://developer.android.com/guide/practices/page-sizes)

PRoot is path/syscall translation, not kernel virtualization or strong isolation. It provides no real root, cgroups, arbitrary namespace isolation or guarantee of a working service manager. Keep only individually supervised long-lived processes. [PRoot-Distro limitations](https://github.com/termux/proot-distro#limitations)

## Resource policy

Initially one executing engineering job, one numerical thread and at most two compiler workers. The reference policy reserves 10 GiB storage and checks at least 768 MiB available RAM before a job. These are prototype defaults, not universal installation requirements; large models/builds need a separate measured budget. M1 planning checks fail closed on insufficient resources.

## Future architectures

Investigate an independently packaged Android-native runtime only after its execution policy is proven. A remote Linux executor is another possible mode, with separate consent, network/privacy/cost requirements and an accurate remote label. x86_64 emulator work cannot substitute for ARM64 device validation. None of these modes is implemented here.
