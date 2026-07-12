"""Write a specialist memory entry, then exit. Run read.py afterward, as
a genuinely separate process, to see it persist."""

from pathlib import Path

from fieldworks.memory.specialist import SpecialistMemory

memory = SpecialistMemory(Path(__file__).parent / "memory")
memory.append(
    "pumping",
    "Pump 102 showed early cavitation signs during afternoon peak demand — "
    "flagged for bearing inspection at next PM cycle.",
)
print("wrote a memory entry for 'pumping'. Now run: python read.py")
