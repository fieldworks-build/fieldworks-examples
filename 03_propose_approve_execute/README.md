# 03 — propose / approve / execute

**Proves:** the trust/safety intercept pattern — a fake write action is proposed, intercepted, requires explicit approval before it executes, and the decision (including denial) is captured in the audit trail. No UI, no MCP server, no waterworks-ai.

**Does not touch:** ADVISORY/COLLABORATIVE/AUTONOMOUS trust modes — those don't exist anywhere yet (SUPERVISED only). No web backend, no SSE, no approval dialog UI.

**Depends on:** `fieldworks.trust` (`fieldworks-core[trust]` — pulls in `cryptography` for the hash-chained audit log). Uses `PendingActionRegistry`, `ProposedAction`, `AuditLog`, `ActionEventStore`.

**Status:** not yet written.

**Plan:** propose a fake action → intercept it via `PendingActionRegistry` → approve (and, in a second run, deny) → show the decision recorded with denial parity in both `AuditLog` and `ActionEventStore`. This is the highest-priority example in the set for framework credibility — it's the least-demonstrated, most differentiating architectural claim Fieldworks makes.
