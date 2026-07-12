# 09 — hello adapter

**Proves:** the protocol layer in isolation from everything else. This binary spins up an embedded MQTT broker, seeds one retained value, spawns the real `mqtt-mcp` server as a subprocess, and calls `connect` + `read_tag` on it over the MCP protocol — showing a genuine VQT (value/quality/timestamp) envelope come back from a real adapter, not a mock.

**Does not touch:** topology, agents, aggregator, trust, memory — this is the protocol layer alone. Not OPC-UA or any other adapter; MQTT is the reference implementation.

**Depends on:** the real `mqtt-mcp` binary (from the sibling `fieldworks-adapters` repo) plus, entirely within this crate: `rumqttd` (embedded broker), `rumqttc` (to seed a value), `rmcp` with `client`/`transport-child-process` features (to speak MCP to the spawned binary), `tokio`.

## Get `mqtt-mcp`

This crate doesn't vendor or path-depend on the adapter — it looks for an `mqtt-mcp` binary the same way a real deployment would.

```bash
cargo install --git https://github.com/fieldworks-build/fieldworks-adapters mqtt-mcp
```

For local iteration against an unreleased adapter change, build from a sibling checkout instead and point at it directly:

```bash
cd ../../adapters && cargo build -p mqtt-mcp
MQTT_MCP_BIN=../../adapters/target/debug/mqtt-mcp cargo run --manifest-path ../09_hello_adapter/Cargo.toml
```

## Run

```bash
cargo run
```

(Uses `mqtt-mcp` from `PATH` by default; set `MQTT_MCP_BIN` to override, as above.)

## Expected output

```
starting an embedded MQTT broker on 127.0.0.1:18830...
seeding a retained value on 'factory/pump01/flow_rate'...
spawning 'mqtt-mcp' as an MCP server over stdio...
calling connect...
calling read_tag('factory/pump01/flow_rate')...

VQT envelope:
{
  "quality": "good",
  "tag_id": "factory/pump01/flow_rate",
  "timestamp": "2026-07-12T22:08:55.457Z",
  "units": "gpm",
  "value": 312.7
}
```

## What this is actually proving

`mqtt-mcp` has no embedded test broker of its own — its integration tests require a live one via `MQTT_TEST_HOST`. This example provides that broker itself, in-process, via `rumqttd` (`Broker::new(config).start()` blocks, so it runs on a dedicated OS thread). It seeds a *retained* MQTT message before calling `read_tag`, because `read_tag` subscribes and waits up to 10 seconds for a message — retained delivery is what makes that deterministic instead of racing a live publish against the subscribe window.

The MCP side is the more novel part for this repo: every other example calls `fieldworks-core` in-process from Python. `mqtt-mcp` is a Rust binary that speaks MCP over stdio, so this example spawns it as a real subprocess (`rmcp::transport::TokioChildProcess`) and drives it as a genuine MCP client (`().serve(transport)`, then `call_tool`) — the same shape any real MCP host (an agent runtime, an aggregator) would use to talk to it. Nothing about the adapter is faked; only the broker and the seed value are.
