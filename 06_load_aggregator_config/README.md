# 06 — load an aggregator config

**Proves:** `fieldworks.aggregator.load_aggregator_config()` parses a minimal `aggregator.json` in isolation.

**Does not touch:** actual MCP backend connections, tool scoping (see [`05_scoped_tools`](../05_scoped_tools/)).

**Depends on:** `fieldworks.aggregator`.

**Status:** not yet written.

**Plan:** a minimal `aggregator.json` fixture + a script that loads it and prints the parsed `AggregatorConfig`.
