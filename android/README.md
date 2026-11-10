# Android product module — design stage

No Android application, manifest, Gradle wrapper, SDK download or APK is claimed
at M1. Kotlin/Compose is the proposed native interface. M2 must first establish
a compatible build tuple and execution/companion route on the Ryzen workstation.

Create the compatibility harness with supported tooling, commit exact versions
and wrapper hashes, and run it on an ARM64 device before adding provisioning.
Required probes: ABI/API/page size; packaged native execution; app-private
writable execution policy; supported companion permissions; process death;
loopback networking; export and low-storage recovery.

Do not paste Termux native libraries into a differently identified APK or assume
that a guest root user gives Android root. Packaging and redistribution review
must cover every transitive native dependency and runtime component.
