# fieldworks-examples

Small, standalone scripts that each prove one piece of the Fieldworks framework (`fieldworks-core`) in isolation. No agents, no servers, no UI, nothing waterworks-specific — just the primitive, minimal enough to read top to bottom in under a minute.

If you want to see Fieldworks *used*, look at `waterworks-ai`. If you want to see how a single piece of it *works*, you're in the right place.

## Install

```bash
pip install -r requirements.txt
```

Each example also documents its own dependencies in its README — most need nothing beyond `fieldworks-core`.

## Examples

| # | Example | Proves | Status |
|---|---|---|---|
| 01 | [`hello_topology`](01_hello_topology/) | `topology.load()` + `validate()` happy path | written |
| 02 | [`topology_validation_catches_errors`](02_topology_validation_catches_errors/) | `load()`/`validate()` actually reject bad input | written |
| 03 | [`propose_approve_execute`](03_propose_approve_execute/) | trust/safety intercept pattern (`fieldworks.trust`) | written |
| 04 | [`build_specialist_prompt`](04_build_specialist_prompt/) | topology → specialist system prompt | written |
| 05 | [`scoped_tools`](05_scoped_tools/) | aggregator `include_tools` filtering | written |
| 06 | [`load_aggregator_config`](06_load_aggregator_config/) | `aggregator.json` parsing | written |
| 07 | [`specialist_memory_persistence`](07_specialist_memory_persistence/) | file-based specialist memory across processes | not yet written |
| 08 | [`fault_mode_topology_change`](08_fault_mode_topology_change/) | topology-as-source-of-truth, both directions | not yet written |
| 09 | [`hello_adapter`](09_hello_adapter/) | protocol layer in isolation (MQTT read → VQT envelope) | blocked on Rust adapter readiness |

## Conventions

- Every example is self-contained: one directory, one script (plus fixtures), one README.
- Every README states what the example proves, what it deliberately does **not** touch, and the expected output.
- No example should take more than a minute to run from a clean checkout.
- Examples depend on published `fieldworks-core`, not on being run from inside the monorepo. Point `requirements.txt` at `-e ../core` only for local iteration against unreleased core changes.
