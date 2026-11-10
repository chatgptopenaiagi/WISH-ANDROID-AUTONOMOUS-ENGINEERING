# Software capability registry

## Record design

Separate installation metadata from executable verification. Each capability needs an identifier, version, languages, logical environment, runtime/architecture, dependencies, use cases, limitations and evidence. Device-local records additionally resolve absolute executable/interpreter paths; portable repository examples use logical bindings.

M1 provides a bounded Python validator in `registry/catalog.py`, a JSON Schema in `registry/capability.schema.json`, and a synthetic fixture. Validation does not import packages or run software. It checks required fields, known evidence states, unique identifiers and coherent timestamped verification.

Evidence has a state (`metadata_only`, `passed`, `failed`, `proposed`), scope (`synthetic`, `reference_device`, `local_device`), device identifier, checked time, expiry and probe label. A positive result from the reference phone cannot establish capability on a new phone. A previously passed result past its expiry requires re-verification. Expiry durations depend on the operation and invalidation events; package/runtime changes invalidate relevant records immediately in the eventual service.

## Automatic selection

`registry.selection.select` normalizes Romanian diacritics and English text, matches capability hints, and ranks relevant records. A capability is ready only if its probe passed for the current local device, runtime and architecture, with unexpired evidence. Metadata-only or stale candidates require a probe; failed candidates require repair or an alternative. Unknown requests return no forced default and are left to Codex interpretation.

This function provides deterministic hints. It does not implement natural-language understanding by itself, install software, execute a tool, contact Codex or guarantee the best framework choice. Codex remains the engineering decision-maker and can revise a choice using evidence. The repository's example is synthetic and intentionally not executable readiness evidence.

## Inventory strategy to port

Read package databases, known Python prefixes and registered tool paths. Probe bounded operations with timeouts, memory/thread limits and explicit interpreters. Store source version, execution target, result, time and limitations. Use generation signatures and change-based refresh rather than repeated whole-device scans. Keep failed probes and previous generations.

Export only an explicitly curated capability summary. Raw package graphs can disclose usernames, paths, repositories and local state. Private device identifiers and session bindings must not enter GitHub.
