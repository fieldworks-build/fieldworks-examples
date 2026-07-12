# 04 — build a specialist prompt

**Proves:** the core value of topology-driven agent configuration — the same minimal topology from [`01_hello_topology`](../01_hello_topology/) produces a specialist system prompt via `build_specialist_prompt()`, with no surrounding agent-loop infrastructure.

**Does not touch:** the agent loop itself, tool wiring, memory, orchestration.

**Depends on:** `fieldworks.agents` (`build_specialist_prompt`).

**Status:** not yet written.

**Plan:** reuse the `01_hello_topology` fixture, call `build_specialist_prompt()` for one process area, print the resulting prompt text.
