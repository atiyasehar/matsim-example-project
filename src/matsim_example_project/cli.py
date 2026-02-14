from __future__ import annotations

import argparse
import json
from pathlib import Path

from .simulator import summarize_scenario


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Python-native MATSim example CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    run_parser = sub.add_parser("run", help="Inspect scenario files and print a compact summary")
    run_parser.add_argument(
        "--config",
        default="scenarios/equil/config.xml",
        help="Path to MATSim config.xml",
    )
    run_parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format",
    )

    return parser


def main() -> int:
    parser = _build_parser()
    args = parser.parse_args()

    if args.command == "run":
        summary = summarize_scenario(Path(args.config))
        payload = {
            "config": str(summary.config_path),
            "network": str(summary.network_path),
            "plans": str(summary.plans_path),
            "nodes": summary.total_nodes,
            "links": summary.total_links,
            "persons": summary.total_persons,
        }

        if args.format == "json":
            print(json.dumps(payload, indent=2))
        else:
            print("MATSim Python Scenario Summary")
            print(f"Config : {payload['config']}")
            print(f"Network: {payload['network']}")
            print(f"Plans  : {payload['plans']}")
            print(f"Nodes  : {payload['nodes']}")
            print(f"Links  : {payload['links']}")
            print(f"Persons: {payload['persons']}")

        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
