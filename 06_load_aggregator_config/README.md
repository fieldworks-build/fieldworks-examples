# 06 — load an aggregator config

**Proves:** `fieldworks.aggregator.load_aggregator_config()` parses a minimal `aggregator.json` in isolation — the JSON array of server definitions, `ServerDef`'s default `timeout_ms`, and the `AggregatorConfig.server_names()`/`get_server()` convenience lookups.

**Does not touch:** actual MCP backend connections, tool scoping (see [`05_scoped_tools`](../05_scoped_tools/)).

**Depends on:** `fieldworks.aggregator`.

## Run

```bash
python load_aggregator_config.py
```

## Expected output

```
server names: ['mqtt', 'opcua']

mqtt: http://localhost:8001 (timeout 5000ms)
  MQTT protocol adapter — nine-tool MCP surface.
opcua: http://localhost:8002 (timeout 10000ms)
  OPC-UA protocol adapter — nine-tool MCP surface.

get_server('opcua') -> ServerDef(name='opcua', url='http://localhost:8002', include_tools=None, default_args=None, timeout_ms=10000, description='OPC-UA protocol adapter — nine-tool MCP surface.')
```

`mqtt` doesn't set `timeout_ms`, so it falls back to the schema default (5000); `opcua` overrides it. Neither server here sets `include_tools`/`default_args` — that's deliberately the one thing this example doesn't show, since [`05_scoped_tools`](../05_scoped_tools/) already covers it in isolation.
