# 08 — add a fault mode and see it picked up

**Proves:** topology-as-source-of-truth, in both directions. Extending the baseline topology with a new fault mode changes what `build_specialist_prompt()` returns with no code changes — and a fault mode with an invalid reference (to an attribute that doesn't exist) is rejected by `load()`, the same way [`02_topology_validation_catches_errors`](../02_topology_validation_catches_errors/) demonstrates for equipment instances.

**Does not touch:** the reactive/monitoring loop that actually detects faults at runtime — this is purely about the topology → prompt → validation chain.

**Depends on:** `fieldworks.topology`, `fieldworks.agents`.

## Run

```bash
python fault_mode_topology_change.py
```

## Expected output

```
--- before: baseline topology (one fault mode) ---
  [WARNING] Cavitation: Flow rate dropping below normal while pump reports running.
  [WARNING] Cavitation: Flow rate dropping below normal while pump reports running.

--- after: topology_with_dry_run.yaml adds a fault mode ---
  [WARNING] Cavitation: Flow rate dropping below normal while pump reports running.
  [CRITICAL] Dry Run: Pump reports running with no flow at all — likely lost prime.
  [WARNING] Cavitation: Flow rate dropping below normal while pump reports running.
  [CRITICAL] Dry Run: Pump reports running with no flow at all — likely lost prime.

new in the prompt, with zero code changes: ['  [CRITICAL] Dry Run: ...', '  [CRITICAL] Dry Run: ...']

--- rejected: fault mode referencing an attribute that doesn't exist ---
rejected: Invalid topology.yaml:
1 validation error for TopologyConfig
equipment_types.0
  Value error, fault_mode 'bearing_wear' references unknown attribute 'vibration' [type=value_error, ...]
```

(Each fault mode line appears twice — both pump instances share the `centrifugal_pump` equipment type, and `build_specialist_prompt()` lists that type's fault modes once per instance section. Not a bug, just two pumps.)

Three fixtures here: `topology.yaml` (baseline, one fault mode — same as [`01_hello_topology`](../01_hello_topology/)), `topology_with_dry_run.yaml` (adds `dry_run`, nothing else changes), and `topology_invalid_fault_mode.yaml` (adds `bearing_wear`, which references `vibration` — an attribute nobody declared). No Python changed between the first two; the prompt changed anyway. The third never produces a `TopologyConfig` at all.
