# Product vision

## Experience to deliver

Install WISH, open it, inspect device capabilities, prepare a supported Linux userspace, authenticate the user's own Codex account, optionally connect GitHub, and describe a creative wish. The person should receive a usable application or artifact with an explanation of how to open it.

The desired onboarding is a product objective, not implemented behavior. Android permission prompts, account authentication, optional companion installation and consequential external operations remain visible human decisions. The user does not have to choose a language, framework, compiler or Python environment.

## Engineering responsibility

The executor inspects existing functionality before adding dependencies, makes routine technical decisions, works in isolated project directories, records actual events, tests outputs and repairs failures. Progress is evidence, not an invented percentage. Queue acceptance, actual execution and verified completion are separate states.

Routine local edits and bounded tests belong to normal engineering. Publishing externally, spending money, deleting user data, granting accounts or changing platform security requires appropriate authorization. Projects are separate directories, not a strong OS security sandbox.

## Intended product journey

1. Discover ABI, Android API, page size, storage, memory and execution constraints.
2. Explain which runtime route is supported on this device, before downloading packages.
3. Provision only compatible, verified, versioned components into the supported runtime owner.
4. Bind one managed Codex session and obtain the user's own authentication.
5. Inventory software and verify relevant capabilities with bounded probes.
6. Accept a wish in the graphical Hub and show genuine events.
7. Deliver project files, tests and a working opening/export path.
8. Recover honestly after process death, account expiry or an interrupted installation.

## Initial scope

Android ARM64, foreground interactive engineering, local browser applications and files. Vivo is one reference device. Romanian and English are initial input/UI targets. Git/GitHub support augments local work and does not gate it.

Universal smartphone support, indefinite background computation, root privileges, CUDA, arbitrary cross-app filesystem access and fully offline Codex inference are outside established capability. Optional future architectures are listed separately in HARDWARE-COMPATIBILITY.md.
