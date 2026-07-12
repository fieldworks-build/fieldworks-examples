# 02 — topology validation catches errors

**Proves:** validation actually rejects malformed input, not just that YAML parses — at both layers `fieldworks.topology` has. `load()` does hard structural validation (required fields, cross-references, type-specific constraints) and raises `ValueError` on failure. `validate()` is a separate, softer pass over an already-loaded topology that returns a `ValidationResult` with warnings instead of raising.

**Does not touch:** agents, prompts, aggregator config, memory.

**Depends on:** `fieldworks.topology`.

## Run

```bash
python topology_validation_catches_errors.py
```

## Expected output

```
--- hard error: load() rejects a bad cross-reference ---
rejected: Invalid topology.yaml:
1 validation error for TopologyConfig
  Value error, instance 'pump-102' references unknown type_id 'reciprocating_pump' [type=value_error, ...]

--- soft warning: validate() flags an incomplete tag binding ---
valid: True
warnings: ["instance 'pump-102': attribute 'running' has no tag binding (not instrumented)"]
```

`bad_reference.yaml` is otherwise identical to [`01_hello_topology`](../01_hello_topology/)'s fixture, except `pump-102` points at a `type_id` that doesn't exist — caught by the schema's cross-reference check before a `TopologyConfig` is ever constructed. `incomplete_bindings.yaml` is structurally valid — it loads fine — but `pump-102` is missing a tag binding for `running`, which `validate()` flags as a warning (not instrumented) rather than an error, since an unbound attribute doesn't make the topology invalid, just incomplete.
