# 03 — propose / approve / execute

**Proves:** the SUPERVISED trust-mode intercept pattern — a fake write action is proposed, blocked pending an operator decision, and only reaches `execute()` on approval. The denied path is recorded with identical fidelity to the approved path (denial parity) in both the hash-chained audit log and the queryable action-event store. No UI, no MCP server, no waterworks-ai.

**Does not touch:** ADVISORY/COLLABORATIVE/AUTONOMOUS trust modes — none of those exist anywhere yet, only SUPERVISED. No web backend, SSE, or approval dialog UI — the "operator" here is just a Python variable deciding synchronously. No AES-256-GCM encryption specifics — `AuditLogConfig.key` is left unset here (plaintext, with a warning), since encryption is a separate concern from the intercept mechanism itself.

**Depends on:** `fieldworks.trust` (`fieldworks-core[trust]`, pulls in `cryptography`). Uses `PendingActionRegistry`, `ProposedAction`, `format_decision_result`, `AuditLog`, `ActionEventStore`.

## Run

```bash
python propose_approve_execute.py
```

## Expected output

```
agent proposes: Reduce chlorine dose from 3.5 to 2.8 L/h — elevated vs turbidity trend
operator decides: approved
  Action approved by operator. Proceed with setpoint_adjustment on Chlorine_01.
    -> EXECUTED: setpoint_adjustment on Chlorine_01 = '2.8'

agent proposes: Clear cavitation fault on Pump 102 without inspection
operator decides: denied
  Action denied by operator (denied). No changes will be made to pump-102.
    -> NOT executed. Denial recorded with the same fidelity as approval.

--- audit trail (hash-chained) ---
verify: ok=True, records=4

--- action events (denial parity, same table for both decisions) ---
  fault_clear          pump-102     decision=denied     outcome=denied
  fault_clear          pump-102     decision=pending    outcome=pending
  setpoint_adjustment  Chlorine_01  decision=approved   outcome=approved
  setpoint_adjustment  Chlorine_01  decision=pending    outcome=pending
```

(You'll also see a `UserWarning` about the audit log being unencrypted — expected, since no key is configured. Also expected: `audit.jsonl` and `events.db` appear in this directory after running — both gitignored, delete freely, they regenerate.)

## What this is actually proving

The agent's `propose_action` call is the only tool it has for a write — it has no direct path to `execute()`. `PendingActionRegistry.await_decision()` blocks the calling coroutine until `resolve()` is called with the operator's decision; nothing the agent does can skip that wait or forge the result. Whether the decision is "approved" or "denied," it's written to `AuditLog` (tamper-evident: each record hashes the previous one, `verify()` walks the chain) and to `ActionEventStore` (a plain SQLite table meant for building UI/reporting on top of) with the same shape — denial isn't a second-class event.

This is the same mechanism `waterworks-ai`'s `control-mcp` implements over SSE and an approval-dialog modal — this example strips away the transport and the UI to show the primitive underneath.
