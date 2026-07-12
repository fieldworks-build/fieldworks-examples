# 07 — how to use memory

**Proves:** the specialist memory contract — write a memory entry, read it back in a fresh process, show it persisting across what would be separate sessions.

**Does not touch:** LadybugDB (graph memory) or DuckDB (analytical memory) — this example covers only file-based `SpecialistMemory`, the simplest of Fieldworks' memory stores. If you're looking for graph or analytical memory, look elsewhere in `fieldworks-core`; this is deliberately the narrow slice.

**Depends on:** `fieldworks.memory.specialist.SpecialistMemory`.

**Status:** not yet written.

**Plan:** two scripts — `write.py` writes a memory entry and exits; `read.py`, run as a genuinely separate process afterward, reads it back and prints it.
