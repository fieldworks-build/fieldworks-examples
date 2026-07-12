"""Prove the aggregator's include_tools / default_args pattern actually
scopes what a specialist can see and how it calls it. No live model call,
no MCP server — just the config layer fieldworks-core provides today.
"""

from pathlib import Path

from fieldworks.aggregator import AggregatorConfig, load_aggregator_config

# Stand-in for what the real "control" MCP server would report if
# introspected — it actually exposes two tools.
SERVER_TOOLS = {
    "control": ["propose_action", "force_execute"],
}


def resolve_tools(server_name: str, config: AggregatorConfig) -> list[str]:
    """What a specialist is actually handed for a server: its full tool
    list, filtered by include_tools if set. fieldworks-core's config schema
    declares the scope; applying it is the host aggregator's job — this
    function is that handful of lines of enforcement."""
    server = config.get_server(server_name)
    available = SERVER_TOOLS[server_name]
    if server.include_tools is None:
        return available
    return [t for t in available if t in server.include_tools]


def call_args(server_name: str, config: AggregatorConfig, explicit_args: dict) -> dict:
    """default_args are merged in under whatever the caller passes explicitly."""
    server = config.get_server(server_name)
    return {**(server.default_args or {}), **explicit_args}


config = load_aggregator_config(Path(__file__).parent / "aggregator.json")

print(f"server actually exposes: {SERVER_TOOLS['control']}")
print(f"include_tools scope:     {config.get_server('control').include_tools}")

resolved = resolve_tools("control", config)
print(f"specialist actually sees: {resolved}")
assert "force_execute" not in resolved
print("force_execute is not in the resolved tool list — the specialist has no way to call it.")

print()
args = call_args("control", config, {"target": "Chlorine_01", "value": "2.8"})
print(f"propose_action call args, with default_args merged in: {args}")
