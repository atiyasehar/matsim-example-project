from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import xml.etree.ElementTree as ET


@dataclass(frozen=True)
class ScenarioSummary:
    config_path: Path
    network_path: Path
    plans_path: Path
    total_links: int
    total_nodes: int
    total_persons: int


def _resolve_from_config(config_path: Path, group_name: str, param_name: str) -> Path:
    tree = ET.parse(config_path)
    root = tree.getroot()

    for module in root.findall("module"):
        if module.attrib.get("name") != group_name:
            continue
        for param in module.findall("param"):
            if param.attrib.get("name") == param_name:
                relative_path = param.attrib.get("value")
                if not relative_path:
                    raise ValueError(f"Empty value for {group_name}.{param_name} in {config_path}")
                return (config_path.parent / relative_path).resolve()

    raise KeyError(f"Missing {group_name}.{param_name} in {config_path}")


def summarize_scenario(config_path: str | Path) -> ScenarioSummary:
    resolved_config = Path(config_path).resolve()
    if not resolved_config.exists():
        raise FileNotFoundError(f"Config not found: {resolved_config}")

    network_path = _resolve_from_config(resolved_config, "network", "inputNetworkFile")
    plans_path = _resolve_from_config(resolved_config, "plans", "inputPlansFile")

    if not network_path.exists():
        raise FileNotFoundError(f"Network file not found: {network_path}")
    if not plans_path.exists():
        raise FileNotFoundError(f"Plans file not found: {plans_path}")

    network_root = ET.parse(network_path).getroot()
    nodes = network_root.findall(".//node")
    links = network_root.findall(".//link")

    plans_root = ET.parse(plans_path).getroot()
    persons = plans_root.findall("person")

    return ScenarioSummary(
        config_path=resolved_config,
        network_path=network_path,
        plans_path=plans_path,
        total_links=len(links),
        total_nodes=len(nodes),
        total_persons=len(persons),
    )
