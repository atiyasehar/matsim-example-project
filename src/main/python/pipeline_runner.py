"""Utilities to run the MATSim example pipeline from Python."""

from __future__ import annotations

import os
import subprocess
from pathlib import Path
from typing import Sequence


DEFAULT_CONFIG = "scenarios/equil/config.xml"
DEFAULT_JAR = "matsim-example-project-0.0.1-SNAPSHOT.jar"


def run_pipeline_end_to_end(
    config_path: str = DEFAULT_CONFIG,
    output_directory: str | None = None,
    last_iteration: int | None = None,
    clean_build: bool = True,
    extra_config_args: Sequence[str] | None = None,
) -> None:
    """Build and run MATSim in one function call.

    Parameters
    ----------
    config_path
        MATSim config file path.
    output_directory
        Optional MATSim output directory override.
    last_iteration
        Optional last iteration override for quick local runs.
    clean_build
        If True, executes ``clean package``. Otherwise executes ``package``.
    extra_config_args
        Additional MATSim command-line args, e.g.
        ``["--config:global.randomSeed", "4711"]``.
    """

    repo_root = Path(__file__).resolve().parents[3]
    resolved_config = repo_root / config_path
    if not resolved_config.exists():
        raise FileNotFoundError(f"Config file not found: {resolved_config}")

    maven_goal = "clean package" if clean_build else "package"
    mvnw_name = "mvnw.cmd" if os.name == "nt" else "./mvnw"
    _run_command(f"{mvnw_name} {maven_goal}", cwd=repo_root)

    jar_path = repo_root / DEFAULT_JAR
    if not jar_path.exists():
        raise FileNotFoundError(
            "Shaded jar was not produced at expected path: "
            f"{jar_path}. Run the Maven build manually and inspect output."
        )

    run_args: list[str] = [
        "java",
        "-cp",
        str(jar_path),
        "org.matsim.project.RunMatsim",
        str(resolved_config),
    ]

    if output_directory:
        run_args.extend(["--config:controler.outputDirectory", output_directory])

    if last_iteration is not None:
        run_args.extend(["--config:controler.lastIteration", str(last_iteration)])

    if extra_config_args:
        run_args.extend(extra_config_args)

    _run_command(run_args, cwd=repo_root)


def _run_command(command: str | Sequence[str], cwd: Path) -> None:
    subprocess.run(command, cwd=cwd, shell=isinstance(command, str), check=True)


if __name__ == "__main__":
    run_pipeline_end_to_end()
