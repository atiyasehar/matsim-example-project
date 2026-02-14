from __future__ import annotations

import sys
from pathlib import Path

PYTHON_SRC = Path(__file__).resolve().parent / "src" / "main" / "python"
sys.path.insert(0, str(PYTHON_SRC))

from matsim_example_project.cli import main


if __name__ == "__main__":
    raise SystemExit(main())
