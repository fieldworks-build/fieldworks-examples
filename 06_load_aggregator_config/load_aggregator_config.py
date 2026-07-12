"""Load a minimal aggregator.json, print the parsed config."""

from pathlib import Path

from fieldworks.aggregator import load_aggregator_config

config = load_aggregator_config(Path(__file__).parent / "aggregator.json")

print(f"server names: {sorted(config.server_names())}")
print()
for server in config.servers:
    print(f"{server.name}: {server.url} (timeout {server.timeout_ms}ms)")
    if server.description:
        print(f"  {server.description}")

print()
opcua = config.get_server("opcua")
print(f"get_server('opcua') -> {opcua!r}")
