# 05 — scoped tools

**Proves:** the aggregator's `include_tools`/`default_args` pattern actually filters what a specialist can see. Two fake tools, one in scope and one out of scope — the example proves the out-of-scope tool never reaches the specialist's tool list.

**Does not touch:** a live model call. Filtering is proven at the aggregator/config layer (deterministic, free, no API key) rather than by having a real agent attempt and get rejected. That dramatic version is out of scope here — worth a separate, clearly-labeled bonus script if written later, since it costs real tokens and is flakier.

**Depends on:** `fieldworks.aggregator` (`ServerDef.include_tools`, `default_args`).

**Status:** not yet written.

**Plan:** a minimal `aggregator.json` with two fake tools scoped to one server, a script that loads the config and inspects the resolved tool list, printing that the out-of-scope tool is simply absent.
