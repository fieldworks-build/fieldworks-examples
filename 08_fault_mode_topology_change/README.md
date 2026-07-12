# 08 — add a fault mode and see it picked up

**Proves:** topology-as-source-of-truth, in both directions. Extending the minimal topology with a fault mode changes what `build_specialist_prompt()` returns with no code changes — and a fault mode with an invalid reference (to equipment that doesn't exist) is rejected by `validate()`, the same way [`02_topology_validation_catches_errors`](../02_topology_validation_catches_errors/) demonstrates for equipment.

**Does not touch:** the reactive/monitoring loop that actually detects faults at runtime — this is purely about the topology → prompt → validation chain.

**Depends on:** `fieldworks.topology`, `fieldworks.agents`.

**Status:** not yet written.

**Plan:** start from the `01_hello_topology` fixture, add a valid fault mode and show the prompt diff, then add an invalid one and show it rejected.
