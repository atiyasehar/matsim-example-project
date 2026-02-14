from pathlib import Path

from matsim_example_project.simulator import summarize_scenario


def test_summarize_equil_scenario_counts_are_positive() -> None:
    summary = summarize_scenario("scenarios/equil/config.xml")

    assert summary.config_path.name == "config.xml"
    assert summary.network_path.name == "network.xml"
    assert summary.plans_path.name == "plans100.xml"
    assert summary.total_nodes > 0
    assert summary.total_links > 0
    assert summary.total_persons == 100


def test_summarize_missing_config_raises() -> None:
    missing = Path("scenarios/equil/does-not-exist.xml")

    try:
        summarize_scenario(missing)
        raise AssertionError("Expected FileNotFoundError")
    except FileNotFoundError:
        pass
