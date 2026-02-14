from __future__ import annotations

import argparse
import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
JAR_NAME = "matsim-example-project-0.0.1-SNAPSHOT.jar"


def run_command(command: list[str], cwd: Path) -> int:
    print("$", " ".join(command))
    completed = subprocess.run(command, cwd=cwd, check=False)
    return completed.returncode


def build_with_maven(skip_tests: bool) -> int:
    mvn_executable = "mvnw.cmd" if Path(REPO_ROOT, "mvnw.cmd").exists() else "./mvnw"
    command = [mvn_executable, "clean", "package"]
    if skip_tests:
        command.append("-DskipTests")
    return run_command(command, REPO_ROOT)


def run_jar() -> int:
    jar_path = REPO_ROOT / "target" / JAR_NAME
    if not jar_path.exists():
        print(
            "Jar not found. Build it first with `python main.py build` "
            "or `python main.py run --build`."
        )
        return 1

    return run_command(["java", "-jar", str(jar_path)], REPO_ROOT)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Python CLI wrapper for building and running the MATSim example project."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    build_parser = subparsers.add_parser("build", help="Build the Java artifact via Maven")
    build_parser.add_argument(
        "--skip-tests",
        action="store_true",
        help="Build with -DskipTests.",
    )

    run_parser = subparsers.add_parser("run", help="Run the built MATSim jar")
    run_parser.add_argument(
        "--build",
        action="store_true",
        help="Build before running.",
    )
    run_parser.add_argument(
        "--skip-tests",
        action="store_true",
        help="When used with --build, pass -DskipTests to Maven.",
    )

    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if args.command == "build":
        return build_with_maven(skip_tests=args.skip_tests)

    if args.command == "run":
        if args.build:
            build_exit_code = build_with_maven(skip_tests=args.skip_tests)
            if build_exit_code != 0:
                return build_exit_code
        return run_jar()

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
