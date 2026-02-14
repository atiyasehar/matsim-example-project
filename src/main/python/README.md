# Python Code

This directory contains Python utilities for orchestrating MATSim runs.

## Run the pipeline end-to-end

Use `pipeline_runner.py` to build the project and launch `org.matsim.project.RunMatsim`.

```bash
python src/main/python/pipeline_runner.py
```

You can also import the function in your own scripts:

```python
from src.main.python.pipeline_runner import run_pipeline_end_to_end

run_pipeline_end_to_end(
    config_path="scenarios/equil/config.xml",
    output_directory="scenarios/equil/output-local",
    last_iteration=5,
)
```
