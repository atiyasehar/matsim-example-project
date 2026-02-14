# matsim-example-project (Python Edition)

This repository has been fully migrated to a **Python-only** codebase.

## What it does

The CLI reads a MATSim scenario config and inspects referenced input files to produce a quick scenario summary:

- number of network nodes
- number of network links
- number of persons in plans

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
python main.py run --config scenarios/equil/config.xml
```

JSON output:

```bash
python main.py run --format json
```

## Tests

```bash
pytest
```

## Project layout

- `src/matsim_example_project/` – Python package and CLI
- `tests/` – unit tests
- `scenarios/` – MATSim scenario input data
- `original-input-data/` – raw source data placeholder
