"""Topology-as-source-of-truth, both directions: adding a valid fault mode
changes what build_specialist_prompt() returns with no code changes, and
a fault mode with a bad reference is rejected before it ever gets there.
"""

from pathlib import Path

from fieldworks.agents import build_specialist_prompt
from fieldworks.topology import load

here = Path(__file__).parent

print("--- before: baseline topology (one fault mode) ---")
before = load(here / "topology.yaml")
before_prompt = build_specialist_prompt("pumping", before)
before_faults = [line for line in before_prompt.splitlines() if line.startswith("  [")]
for line in before_faults:
    print(line)

print()
print("--- after: topology_with_dry_run.yaml adds a fault mode ---")
after = load(here / "topology_with_dry_run.yaml")
after_prompt = build_specialist_prompt("pumping", after)
after_faults = [line for line in after_prompt.splitlines() if line.startswith("  [")]
for line in after_faults:
    print(line)

new_lines = [line for line in after_faults if line not in before_faults]
print(f"\nnew in the prompt, with zero code changes: {new_lines}")

print()
print("--- rejected: fault mode referencing an attribute that doesn't exist ---")
try:
    load(here / "topology_invalid_fault_mode.yaml")
except ValueError as exc:
    print(f"rejected: {exc}")
