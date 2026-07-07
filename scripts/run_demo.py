from __future__ import annotations

import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def run(command: list[str]) -> None:
    print(f"running: {' '.join(command)}")
    subprocess.run(command, cwd=PROJECT_ROOT, check=True)


def main() -> int:
    python = sys.executable
    commands = [
        [python, "-m", "compileall", "src", "tests", "scripts"],
        [python, "-m", "pytest"],
        [
            python,
            "-m",
            "opportunity_radar.main",
            "validate",
            "--input-dir",
            "examples/sample_inputs",
        ],
        [
            python,
            "-m",
            "opportunity_radar.main",
            "generate",
            "--profile",
            "singapore_ai_fintech",
            "--mock",
            "--as-of",
            "2026-07-06",
            "--output-root",
            ".tmp/demo",
        ],
        [python, "scripts/verify_line_endings.py"],
    ]
    for command in commands:
        run(command)
    print("demo_status=passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
