# Installer planning contract

`plan.py` evaluates supplied resource values and reports peak storage accounting
for compressed download, unpacked data, rollback and reserve. It performs no I/O.
The caller must obtain current measurements and trustworthy sizes. A positive
plan is not Android compatibility, signature validation or installation success.

M3 must implement authenticated manifests, resumable staging, strict extraction,
hash/signature validation, runtime probes, atomic activation and rollback only
after M2 establishes a supported execution route. No install script or mutable
remote curl-to-shell command is provided at M1.
