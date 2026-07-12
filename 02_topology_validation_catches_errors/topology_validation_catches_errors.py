"""Show both layers of topology validation rejecting bad input:
load() raises on structural errors; validate() warns on soft ones.
"""

from pathlib import Path

from fieldworks.topology import load, validate

here = Path(__file__).parent

print("--- hard error: load() rejects a bad cross-reference ---")
try:
    load(here / "bad_reference.yaml")
except ValueError as exc:
    print(f"rejected: {exc}")

print()
print("--- soft warning: validate() flags an incomplete tag binding ---")
topology = load(here / "incomplete_bindings.yaml")
result = validate(topology)
print(f"valid: {result.valid}")
print(f"warnings: {result.warnings}")
