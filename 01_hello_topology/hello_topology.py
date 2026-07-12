"""Load a minimal topology.yaml, validate it, print the result."""

from pathlib import Path

from fieldworks.topology import load, validate

topology = load(Path(__file__).parent / "topology.yaml")
print(f"facility: {topology.facility.name} ({topology.facility.site_id})")
print(f"process areas: {len(topology.process_areas)}")
print(f"equipment types: {len(topology.equipment_types)}")
print(f"equipment instances: {len(topology.equipment_instances)}")

result = validate(topology)
print(f"valid: {result.valid}")
print(f"errors: {result.errors}")
print(f"warnings: {result.warnings}")
