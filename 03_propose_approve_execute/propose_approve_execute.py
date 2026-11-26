"""Propose/approve/execute: the SUPERVISED trust-mode intercept pattern.

No UI, no MCP server, no waterworks-ai — just fieldworks.trust driving a
fake write action through propose -> intercept -> operator decision ->
execute (or not), with both outcomes recorded with equal fidelity. A third
action runs under AUTONOMOUS to show how the record tells the mode's
approval from a person's.
"""

import asyncio
from pathlib import Path

from fieldworks.trust.audit import AuditLog, AuditLogConfig
from fieldworks.trust.events import ActionEventStore, ActionEventStoreConfig
from fieldworks.trust.identity import dispatch_approver
from fieldworks.trust.intercept import (
    PendingActionRegistry,
    ProposedAction,
    format_decision_result,
)
from fieldworks.trust.modes import TrustMode, resolve_disposition

HERE = Path(__file__).parent
SESSION_ID = "demo-session-01"
# Who decides, and how the deployment knows (spec Part I, Operator identity).
# The decisions here stand in for one person at a console who signed in as
# "alice". A real host records the person it actually authenticated, or a
# documented shared value such as "shared-token" with auth_method
# "shared_credential" when everyone approves with one credential. Never a
# placeholder person like "operator-01".
OPERATOR = {"operator_id": "alice", "auth_method": "user"}


def execute(action: ProposedAction) -> None:
    """Stand-in for the real write — a fake MCP tool call the agent would
    make after approval. Never called on the denied path."""
    print(f"    -> EXECUTED: {action.action_type} on {action.target} = {action.value!r}")


async def run_proposal(
    registry: PendingActionRegistry,
    audit: AuditLog,
    events: ActionEventStore,
    args: dict,
    operator_decision: str,
) -> None:
    action = ProposedAction.from_tool_input(args)
    print(f"\nagent proposes: {action.description}")

    audit.log(
        "action_proposed",
        action_id=action.action_id,
        action_type=action.action_type,
        target=action.target,
        value=action.value,
        **OPERATOR,
    )
    # The pending row names the operator the proposal now waits on.
    events.log_action_event(
        session_id=SESSION_ID,
        action_type=action.action_type,
        target=action.target,
        value=action.value,
        description=action.description,
        decision="pending",
        **OPERATOR,
    )

    # The agent's propose_action call blocks here until an operator decides —
    # this is the intercept. There is no execution tool the agent can reach
    # in the meantime.
    wait_task = asyncio.create_task(registry.await_decision(action.action_id, timeout=5))
    await asyncio.sleep(0)  # let await_decision register before we resolve it
    print(f"operator decides: {operator_decision}")
    registry.resolve(action.action_id, operator_decision)
    decision = await wait_task

    # Both sinks get the same three fields, so they agree on who decided.
    audit.log(
        "action_decided", action_id=action.action_id, decision=decision, **OPERATOR
    )
    events.log_action_event(
        session_id=SESSION_ID,
        action_type=action.action_type,
        target=action.target,
        value=action.value,
        description=action.description,
        outcome=decision,
        decision=decision,
        **OPERATOR,
    )

    print(f"  {format_decision_result(action, decision)}")
    if decision == "approved":
        execute(action)
    else:
        print("    -> NOT executed. Denial recorded with the same fidelity as approval.")


def run_autonomous(audit: AuditLog, events: ActionEventStore, args: dict) -> None:
    """AUTONOMOUS: dispatch approves without a person, so there is no
    intercept. The record names the mode, never a person:
    operator_id="trust-mode:autonomous", auth_method="trust_mode"."""
    action = ProposedAction.from_tool_input(args)
    mode = TrustMode.AUTONOMOUS
    approver = dispatch_approver(mode, resolve_disposition(mode))
    print(f"\nagent proposes: {action.description}")
    print(f"trust mode {mode.value} decides: {approver['decision']}")

    audit.log("action_decided", action_id=action.action_id, **approver)
    events.log_action_event(
        session_id=SESSION_ID,
        action_type=action.action_type,
        target=action.target,
        value=action.value,
        description=action.description,
        outcome=approver["decision"],
        **approver,
    )
    print(f"  {format_decision_result(action, approver['decision'])}")
    execute(action)


async def main() -> None:
    registry = PendingActionRegistry()
    audit = AuditLog(AuditLogConfig(log_path=HERE / "audit.jsonl"))
    events = ActionEventStore(ActionEventStoreConfig(db_path=HERE / "events.db"))

    await run_proposal(
        registry,
        audit,
        events,
        args={
            "description": (
                "Reduce chlorine dose from 3.5 to 2.8 L/h — elevated vs turbidity trend"
            ),
            "action_type": "setpoint_adjustment",
            "target": "Chlorine_01",
            "value": "2.8",
        },
        operator_decision="approved",
    )

    await run_proposal(
        registry,
        audit,
        events,
        args={
            "description": "Clear cavitation fault on Pump 102 without inspection",
            "action_type": "fault_clear",
            "target": "pump-102",
        },
        operator_decision="denied",
    )

    run_autonomous(
        audit,
        events,
        args={
            "description": "Raise backwash pump speed to 60%",
            "action_type": "setpoint_adjustment",
            "target": "Backwash_01",
            "value": "60",
        },
    )

    print("\n--- audit trail (hash-chained) ---")
    verify = audit.verify()
    print(f"verify: ok={verify.ok}, records={verify.record_count}")

    print("\n--- action events (denial parity, same table for both decisions) ---")
    for row in events.get_action_events(session_id=SESSION_ID):
        print(
            f"  {row['target']:<12} decision={row['decision']:<14} "
            f"by {row['operator_id']} ({row['auth_method']})"
        )


if __name__ == "__main__":
    asyncio.run(main())
