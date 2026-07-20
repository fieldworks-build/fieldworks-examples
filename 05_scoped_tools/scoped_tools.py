"""Prove the aggregator's include_tools / default_args pattern actually
scopes what a specialist can see and how it calls it. No live model call,
no MCP server — just the config layer fieldworks-core provides today.
"""

from pathlib import Path

from fieldworks.aggregator import load_aggregator_config, merge_call_args, resolve_tools

# Stand-in for what the real "control" MCP server would report if
# introspected — it actually exposes two tools.
SERVER_TOOLS = {
    "control": ["propose_action", "force_execute"],
}


config = load_aggregator_config(Path(__file__).parent / "aggregator.json")
server = config.get_server("control")

print(f"server actually exposes: {SERVER_TOOLS['control']}")
print(f"include_tools scope:     {server.include_tools}")

resolved = resolve_tools(server, SERVER_TOOLS["control"])
print(f"specialist actually sees: {resolved}")
assert "force_execute" not in resolved
print("force_execute is not in the resolved tool list — the specialist has no way to call it.")

print()
args = merge_call_args(server, {"target": "Chlorine_01", "value": "2.8"})
print(f"propose_action call args, with default_args merged in: {args}")
