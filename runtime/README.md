# Runtime contracts

`jobs.py` implements pure state-transition checks and real file/hash validation.
It is not a shell executor, queue, session lease manager or runtime service.
No transition is inferred from a timer or fake percentage. Unknown delivery needs
explicit reconciliation; completed jobs cannot be moved back into execution.

Runtime provisioning, stable interpreter bindings, bounded subprocess execution,
application registrations, supervision and Android lifecycle recovery are future
adapters informed by the preserved Vivo reference.
