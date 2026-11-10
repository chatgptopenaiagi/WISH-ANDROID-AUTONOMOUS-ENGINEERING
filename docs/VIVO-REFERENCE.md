# Reusable Vivo reference components

Read-only inspection covers registered laboratory modules and selected reports.
It is not a whole-device scan. The original installation remains in place.
This repository contains design summaries and new portable code, not a copied lab.

| Reference component | Purpose and dependencies | Verification and portability work |
| --- | --- | --- |
| wish CLI and request ledger | Python, existing SENTINEL-managed launcher, local locks, JSON checks/artifacts | Real same-session submissions and completed software demonstrated; hard-coded bindings must become private runtime configuration |
| Environment helper | Explicit independent Conda interpreters and per-command variables | dev/AI/math and Miniforge Python execution verified; guest paths must be discovered locally |
| Registry inventory/probes | Package databases, Python metadata, bounded compiler/library operations | Package presence kept distinct from execution; curated evidence only is exported |
| Bilingual selection hints | Romanian normalization and deterministic keywords | Useful advisory mechanism; Codex interprets the actual objective; new evidence-aware module is implemented here |
| Hub backend | FastAPI 0.156.4, Uvicorn 0.54.0, Python SQLite, websockets 17.3 | 25 API tests, 13 real integration checks, 14 browser scenarios and an additional restart-button check archived |
| Hub UI | Buildless HTML/CSS/JavaScript, Romanian responsive browser UI | 390/360 px browser tests, simulated touch and Android Edge page/bootstrap contacts; Hub physical gestures not user-verified |
| Application manager | Fixed registrations, PID start identity and HTTP instance health | Generated demo launch, open, stop and restart tested; portable process ownership/lifecycle adapter needed |
| Artifact delivery | Contained project paths, hashes, attachment downloads | Real browser download tested; Android content-URI/SAF export still needs a product adapter |
| Mathematical simulation | Browser Canvas/worker and optional WebGL2; Python local server; numerical reference checks | Physical UI, Mandelbrot, WebGL2, pinch and PNG export USER-VERIFIED on Vivo |
| Text-statistics demonstration | Python standard library, local web UI, JSON export | Genuine Hub wish to implemented/tested/used software; six unit tests plus HTTP and browser checks |
| SENTINEL | Existing inventory, launch routing and coordination | Preserved in place; no source/runtime state exported; portable distribution/adapter review required |

## What must change for a product

Replace installation-specific roots, environment locations, session bindings,
socket discovery and Android activity helpers with versioned configuration and
supported runtime-owner APIs. Separate Windows build tools from device tools.
Keep authentication local to each owner and configure every interpreter explicitly.
Review source ownership and third-party redistribution before moving any code.

The existing Python environments are valuable capability templates, not binary
prefixes to copy into an APK. Prefer a minimal supported package set and add
dependencies only for an active engineering requirement. Anaconda/Miniforge,
their channels, Python wheels and native libraries need individual distribution
and compatibility review; their presence on the phone is not permission to bundle.

## Evidence handling

`evidence/vivo-reference.json` contains selected counts, named operations, package
versions and limitations. Source reports were inspected locally. Session IDs,
queue payloads, private logs, raw inventories, runtime addresses and absolute paths
are deliberately absent. Archived evidence does not establish current service
uptime or compatibility of a clean installation.
