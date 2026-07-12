"""Propose/approve/execute: the SUPERVISED trust-mode intercept pattern.

No UI, no MCP server, no waterworks-ai — just fieldworks.trust driving a
fake write action through propose -> intercept -> operator decision ->
execute (or not), with both outcomes recorded with equal fidelity.
"""

import asyncio
from pathlib import Path

from fieldworks.trust.audit import AuditLog, AuditLogConfig
from fieldworks.trust.events import ActionEventStore, ActionEventStoreConfig
from fieldworks.trust.intercept import (
    PendingActionRegistry,
    ProposedAction,
    format_decision_result,
)

HERE = Path(__file__).parent
SESSION_ID = "demo-session-01"
OPERATOR_ID = "operator-01"


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
    )
    events.log_action_event(
        session_id=SESSION_ID,
        action_type=action.action_type,
        target=action.target,
        value=action.value,
        description=action.description,
        operator_id=OPERATOR_ID,
        decision="pending",
    )

    # The agent's propose_action call blocks here until an operator decides —
    # this is the intercept. There is no execution tool the agent can reach
    # in the meantime.
    wait_task = asyncio.create_task(registry.await_decision(action.action_id, timeout=5))
    await asyncio.sleep(0)  # let await_decision register before we resolve it
    print(f"operator decides: {operator_decision}")
    registry.resolve(action.action_id, operator_decision)
    decision = await wait_task

    audit.log("action_decided", action_id=action.action_id, decision=decision)
    events.log_action_event(
        session_id=SESSION_ID,
        action_type=action.action_type,
        target=action.target,
        value=action.value,
        description=action.description,
        operator_id=OPERATOR_ID,
        decision=decision,
        outcome=decision,
    )

    print(f"  {format_decision_result(action, decision)}")
    if decision == "approved":
        execute(action)
    else:
        print("    -> NOT executed. Denial recorded with the same fidelity as approval.")


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

    print("\n--- audit trail (hash-chained) ---")
    verify = audit.verify()
    print(f"verify: ok={verify.ok}, records={verify.record_count}")

    print("\n--- action events (denial parity, same table for both decisions) ---")
    for row in events.get_action_events(session_id=SESSION_ID):
        print(
            f"  {row['action_type']:<20} {row['target']:<12} "
            f"decision={row['decision']:<10} outcome={row['outcome']}"
        )


if __name__ == "__main__":
    asyncio.run(main())
