# 04 — build a specialist prompt

**Proves:** the core value of topology-driven agent configuration — the same topology from [`01_hello_topology`](../01_hello_topology/) (copied here for self-containment) produces a specialist system prompt via `build_specialist_prompt()`, with no agent loop, no tool wiring, no orchestration.

**Does not touch:** the agent loop itself, tool scoping, memory enrichment (`memory_client=`), orchestration (`build_orchestrator_system()`).

**Depends on:** `fieldworks.agents` (`build_specialist_prompt`), `fieldworks.topology`.

## Run

```bash
python build_specialist_prompt.py
```

## Expected output

```
You are a Specialist agent for the Pumping at Example Pump Station.

Your process area: Transfer pumps moving water from wet well to distribution.

## Equipment in this area

### Pump 101 (pump-101)
Type: Centrifugal Pump — Standard single-stage centrifugal transfer pump.

Monitored attributes:
  - Flow Rate (gpm): normal 50.0–500.0
  - Running (bool): normal state: true

Known fault modes for Centrifugal Pump:
  [WARNING] Cavitation: Flow rate dropping below normal while pump reports running.

### Pump 102 (pump-102)
Type: Centrifugal Pump — Standard single-stage centrifugal transfer pump.

Monitored attributes:
  - Flow Rate (gpm): normal 50.0–500.0
  - Running (bool): normal state: true

Known fault modes for Centrifugal Pump:
  [WARNING] Cavitation: Flow rate dropping below normal while pump reports running.

Diagnose using the available data. For any attribute marked NOT INSTRUMENTED,
state explicitly that the equipment lacks that sensor and adjust your diagnostic
scope accordingly. Do not invent readings for unbound attributes.
```

Every line here — equipment names, monitored attributes with units and normal ranges, fault modes, even the "don't invent readings" instruction — comes from `topology.yaml`, not from hand-authored prompt text. Add a third pump to the fixture and rerun: a third `###` section appears with no code changes. That's the whole claim of Part II of the Fieldworks spec in one script.
