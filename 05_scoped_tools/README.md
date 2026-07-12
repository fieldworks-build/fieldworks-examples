# 05 — scoped tools

**Proves:** the aggregator's `include_tools`/`default_args` pattern actually filtering what a specialist can see and how it calls it. A fake "control" server exposes two tools (`propose_action`, `force_execute`); `include_tools` scopes it down to one. The specialist's resolved tool list simply never contains `force_execute` — it isn't rejected at call time, it was never offered.

**Does not touch:** a live model call. This is proven at the config/dispatch layer (deterministic, free, no API key) rather than by having a real agent attempt `force_execute` and get refused. `fieldworks-core`'s `aggregator` module only provides the declarative schema (`ServerDef.include_tools`, `default_args`) — it doesn't yet ship a `resolve_tools()` runtime helper, so `resolve_tools()`/`call_args()` here are a few lines standing in for what a host aggregator applies. `SERVER_TOOLS` is a stand-in for what introspecting the real MCP server would return.

**Depends on:** `fieldworks.aggregator` (`load_aggregator_config`, `ServerDef.include_tools`, `default_args`).

## Run

```bash
python scoped_tools.py
```

## Expected output

```
server actually exposes: ['propose_action', 'force_execute']
include_tools scope:     ['propose_action']
specialist actually sees: ['propose_action']
force_execute is not in the resolved tool list — the specialist has no way to call it.

propose_action call args, with default_args merged in: {'operator_id': 'operator-01', 'target': 'Chlorine_01', 'value': '2.8'}
```

This is one of the strongest architectural claims Fieldworks makes: a specialist's tool scope isn't a prompt-level instruction the model could ignore or be jailbroken past — it's a filtered list the model's context never contains `force_execute` in. `default_args` shows the complementary half: values like `operator_id` are injected by the aggregator config, not left for the specialist to supply (or omit) itself.
