# Registry module

`catalog.py` validates portable capability records; `selection.py` returns bilingual,
evidence-aware hints. Both use only Python's standard library. The example catalog
is synthetic. No command, inventory, package import, dependency installation or
Codex request is executed by these functions.

The JSON Schema describes the wire structure. The Python validator also enforces
unique IDs and cross-field timestamp/evidence rules. Full live inventory, absolute
interpreter binding, invalidation and durable storage remain M5 work.
