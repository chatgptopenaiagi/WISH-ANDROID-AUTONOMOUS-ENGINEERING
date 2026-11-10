# ADR 0001 — prove the runtime owner before building the installer

Status: accepted as an M1 investigation decision; runtime implementation pending.

The reference environment demonstrates that an existing Termux/PRoot installation
can host the engineering workflow. A new APK has a distinct app UID and must obey
its own target API, execution and storage policy. It cannot inherit Termux's
private prefix simply by knowing its path. PRoot does not change these facts.

Investigate a supported Termux companion integration first. Keep WISH onboarding,
runtime ownership and the authenticated bridge explicit. The long-term independent
APK route remains contingent on an Android-native execution proof and a viable
distribution/update design. Do not reduce target API or weaken SELinux to declare
the problem solved.

Consequences: M2 is a blocking feasibility gate for M3/M7. No fake installer,
Gradle wrapper or successful APK claim is included in M1. The user journey must
acknowledge any companion requirement until a tested standalone route exists.

Sources: [Android execution policy](https://developer.android.com/about/versions/10/behavior-changes-10),
[Termux execution environment](https://github.com/termux/termux-packages/wiki/Termux-execution-environment).
