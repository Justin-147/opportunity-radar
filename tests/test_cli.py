import os
import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_cli_generate_command_works_with_mock():
    env = os.environ.copy()
    env["PYTHONPATH"] = str(PROJECT_ROOT / "src")
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "opportunity_radar.main",
            "generate",
            "--profile",
            "singapore_ai_fintech",
            "--mock",
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
