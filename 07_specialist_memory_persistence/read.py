"""Read back a specialist's accumulated memory. Run write.py first, in
a separate process — this script has no idea that one ever ran."""

from pathlib import Path

from fieldworks.memory.specialist import SpecialistMemory

memory = SpecialistMemory(Path(__file__).parent / "memory")
content = memory.get("pumping")
if not content:
    print("no memory found for 'pumping' — run write.py first")
else:
    print(content)
