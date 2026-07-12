"""Topology in, specialist system prompt out — no agent loop required."""

from pathlib import Path

from fieldworks.agents import build_specialist_prompt
from fieldworks.topology import load

topology = load(Path(__file__).parent / "topology.yaml")
print(build_specialist_prompt("pumping", topology))
