# 01 — hello topology

**Proves:** `fieldworks.topology.load()` and `validate()` work on a minimal, valid `topology.yaml` — one process area, one equipment type, two instances.

**Does not touch:** agents, prompts, aggregator config, memory. Schema and validator only.

**Depends on:** `fieldworks.topology` (`fieldworks-core` base install, no extras).

## Run

```bash
python hello_topology.py
```

## Expected output

```
facility: Example Pump Station (example-01)
process areas: 1
equipment types: 1
equipment instances: 2
valid: True
errors: []
warnings: []
```

`load()` does the hard structural validation (required fields, cross-references, type-specific constraints) and raises `ValueError` on failure. `validate()` is a separate, softer pass — mainly tag-binding completeness — that returns a `ValidationResult` instead of raising. Both instances here have every attribute tag-bound, so `validate()` comes back clean.

See [`02_topology_validation_catches_errors`](../02_topology_validation_catches_errors/) for what each layer looks like when it actually rejects something.
