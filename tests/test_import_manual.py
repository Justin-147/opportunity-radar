from pathlib import Path

from opportunity_radar.pipeline.import_manual import load_csv, load_yaml_records

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_csv_sample_input_loads():
    path = PROJECT_ROOT / "examples" / "sample_inputs" / "singapore_ai_fintech_jobs.csv"
    rows = load_csv(path)

    assert len(rows) == 12
    assert rows[0]["title"] == "AI Governance Analyst"


def test_yaml_sample_inputs_load():
    path = PROJECT_ROOT / "examples" / "sample_inputs" / "sample_policy_signals.yaml"
    rows = load_yaml_records(path)

    assert len(rows) == 4
    assert rows[0]["category"] == "policy"
