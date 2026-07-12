# 09 — hello adapter

**Proves:** the protocol layer in isolation from everything else — a single MQTT read against a mock broker, showing the VQT (value/quality/timestamp) envelope come back.

**Does not touch:** topology, agents, aggregator, trust, memory. Pure adapter-core.

**Depends on:** the Rust adapter crates (`adapters/fieldworks-adapter-core`, `adapters/mqtt-mcp`) in the sibling `adapters` repo.

**Status:** placeholder only — but not actually blocked on the Rust side. Checked 2026-07-12: `mqtt-mcp` is complete, versioned 1.0.0, with 25 unit tests, builds and runs today. What's still undecided:

1. No embedded mock broker ships in the crate — its own integration tests require a *live* broker via `MQTT_TEST_HOST`. This example needs one stood up (mosquitto, or an embedded Rust broker like `rumqttd`) — real setup none of the other examples need.
2. `mqtt-mcp` speaks MCP over stdio as a Rust binary. Examples 01–08 all call `fieldworks-core` in-process from Python; this one needs an MCP client harness — either written in Rust, or Python spawning the compiled binary as a subprocess and speaking MCP stdio to it.

Next step is deciding those two things, not waiting on adapter code.
