# 09 — hello adapter

**Proves:** the protocol layer in isolation from everything else — a single MQTT read against a mock broker, showing the VQT (value/quality/timestamp) envelope come back.

**Does not touch:** topology, agents, aggregator, trust, memory. Pure adapter-core.

**Depends on:** the Rust adapter crates (`adapters/fieldworks-adapter-core`, `adapters/mqtt-mcp`) in the sibling `adapters` repo.

**Status:** blocked — waiting on Rust adapter readiness. Placeholder only.
