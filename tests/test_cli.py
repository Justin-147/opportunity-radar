import os
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_cli_generate_command_works_with_mock_and_output_root(tmp_path):
    env = os.environ.copy()
    env["PYTHONPATH"] = str(PROJECT_ROOT / "src")
    output_root = tmp_path / "outputs"
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "opportunity_radar.main",
            "generate",
            "--profile",
            "singapore_ai_fintech",
            "--mock",
            "--as-of",
            "2026-07-06T09:00:00",
            "--output-root",
            str(output_root),
        ],
        cwd=PROJECT_ROOT,
        env=env,
        capture_output=True,
        text=True,
        timeout=90,
    )

    assert result.returncode == 0, result.stderr
    assert "top_opportunities: 10" in result.stdout
    assert "markdown_en:" in result.stdout
    assert (output_root / "data" / "processed" / "2026-07-06_singapore_ai_fintech.json").exists()


def test_cli_validate_command_passes_samples():
    env = os.environ.copy()
    env["PYTHONPATH"] = str(PROJECT_ROOT / "src")
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "opportunity_radar.main",
            "validate",
            "--input-dir",
            "examples/sample_inputs",
        ],
        cwd=PROJECT_ROOT,
        env=env,
        capture_output=True,
        text=True,
        timeout=90,
    )

    assert result.returncode == 0, result.stderr
    assert "validation_errors: 0" in result.stdout
    assert "status: passed" in result.stdout


def test_cli_validate_command_fails_for_missing_title(tmp_path):
    input_dir = tmp_path / "inputs"
    input_dir.mkdir()
    (input_dir / "bad.csv").write_text(
        "title,url,published_at,category\n,https://example.org,2026-07-01,job\n",
        encoding="utf-8",
    )
    env = os.environ.copy()
    env["PYTHONPATH"] = str(PROJECT_ROOT / "src")
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "opportunity_radar.main",
            "validate",
            "--input-dir",
            str(input_dir),
        ],
        cwd=PROJECT_ROOT,
        env=env,
        capture_output=True,
        text=True,
        timeout=90,
    )

    assert result.returncode == 1
    assert "validation_errors: 1" in result.stdout
