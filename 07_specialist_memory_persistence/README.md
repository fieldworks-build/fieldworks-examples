# 07 — how to use memory

**Proves:** the specialist memory contract — write a memory entry, read it back in a fresh process, show it persisting across what would be separate sessions.

**Does not touch:** LadybugDB (graph memory) or DuckDB (analytical memory) — this example covers only file-based `SpecialistMemory`, the simplest of Fieldworks' memory stores. If you're looking for graph or analytical memory, look elsewhere in `fieldworks-core`; this is deliberately the narrow slice.

**Depends on:** `fieldworks.memory.specialist.SpecialistMemory`.

## Run

```bash
python write.py
python read.py
```

Run them as two separate `python` invocations, not two calls in one script — the point is that `read.py` has no in-memory state left over from `write.py`, only the file on disk.

## Expected output

```
$ python write.py
wrote a memory entry for 'pumping'. Now run: python read.py

$ python read.py

## 2026-07-12 21:50 UTC
Pump 102 showed early cavitation signs during afternoon peak demand — flagged for bearing inspection at next PM cycle.
```

`SpecialistMemory` is one markdown file per specialist (`memory/pumping.md` here, gitignored — delete freely, it regenerates). `append()` timestamps and appends; `get()` just reads the whole file back as a string. Run `write.py` a second time before `read.py` and you'll see both entries — this is accumulation, not a single overwritten value.
