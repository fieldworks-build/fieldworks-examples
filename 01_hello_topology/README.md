# 01 — hello topology

**Proves:** `fieldworks.topology.load()` and `validate()` work on a minimal, valid `topology.yaml` — two or three pieces of equipment, nothing more.

**Does not touch:** agents, prompts, aggregator config, memory. Schema and validator only.

**Depends on:** `fieldworks.topology` (`fieldworks-core` base install, no extras).

**Status:** not yet written.

**Plan:** a `topology.yaml` fixture in this directory + a script under ten lines that loads it, validates it, and prints the result. Companion to [`02_topology_validation_catches_errors`](../02_topology_validation_catches_errors/), which shows the failure path.
