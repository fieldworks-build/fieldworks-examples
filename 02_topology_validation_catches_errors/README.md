# 02 — topology validation catches errors

**Proves:** `validate()` actually rejects malformed input, not just that YAML parses. A broken `topology.yaml` (duplicate equipment ID, or a dangling reference) produces a `ValidationResult` with real errors.

**Does not touch:** agents, prompts, aggregator config, memory.

**Depends on:** `fieldworks.topology`.

**Status:** not yet written.

**Plan:** a deliberately-broken `topology.yaml` fixture + a script that runs `validate()` and prints the errors it returns. Companion to [`01_hello_topology`](../01_hello_topology/), which shows the happy path.
