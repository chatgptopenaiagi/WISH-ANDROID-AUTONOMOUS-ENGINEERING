# Windows / Ryzen development

The primary workstation target is Windows with an AMD Ryzen CPU and PowerShell 7.
It has not been accessed during the Vivo M1 work. These are future setup steps,
not a claim that the workstation already has an SDK or can build WISH.

## M1 source checks

With Git and Python 3.12+ already available:

```powershell
git clone https://github.com/chatgptopenaiagi/WISH-ANDROID-AUTONOMOUS-ENGINEERING.git
Set-Location WISH-ANDROID-AUTONOMOUS-ENGINEERING
./scripts/Test-Repository.ps1
```

Private repository cloning requires the user's supported GitHub authentication.
The script finds an existing Python interpreter and runs dependency-free tests
and repository checks. It installs nothing and starts no Codex process.

Read portable JSON/text as UTF-8 explicitly. The first GitHub Windows run exposed
a locale-dependent catalogue read that corrupted Romanian characters; the test
fixture loader now specifies UTF-8. A hosted Windows CI run is separate evidence
from validation on the owner's Ryzen workstation.

## M2 toolchain investigation

Record Windows version/architecture, PowerShell, JDK, Android Studio, SDK tools,
adb and device visibility. Select a mutually compatible AGP/Gradle/Kotlin/JDK/SDK
tuple from the official tooling documentation, record its exact versions and
checksums, and generate the wrapper with that toolchain. Do not assume a fixed
SDK directory, download unknown scripts or use Linux ARM64 build executables on
Windows x64.

Use adb only with explicit device authorization. Prefer a spare clean ARM64
device/profile for installation probes. Never reset the working Vivo laboratory.
An x86_64 emulator is useful for framework UI tests but does not validate ARM64
Linux/PRoot, vendor lifecycle policy or native binaries.

No signing key or release identity is created in M1. Keep eventual signing keys,
local.properties, account tokens, SDKs and build outputs outside version control.
Document the signing/update recovery policy before distributing a release.
