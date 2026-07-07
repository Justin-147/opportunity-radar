from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

FILES_TO_CHECK = [
    "README.md",
    "README.zh-CN.md",
    "CHANGELOG.md",
    "LICENSE",
    "pyproject.toml",
    ".gitignore",
    ".gitattributes",
    ".github/workflows/tests.yml",
    "config/report_template.md",
    "docs/methodology.md",
    "docs/input_schema.md",
    "src/opportunity_radar/main.py",
    "src/opportunity_radar/pipeline/validate_inputs.py",
    "src/opportunity_radar/pipeline/score.py",
    "src/opportunity_radar/writers/markdown_writer.py",
    "src/opportunity_radar/writers/html_writer.py",
    "src/opportunity_radar/dashboard/helpers.py",
    "tests/test_cli.py",
    "tests/test_datetime_parsing.py",
    "tests/test_validation.py",
    "tests/test_markdown_escaping.py",
    "tests/test_html_writer.py",
    "tests/test_dashboard_helpers.py",
    "scripts/run_demo.py",
    "examples/sample_reports/weekly_opportunity_radar_en.md",
]

MIN_LF_COUNTS = {
    "README.md": 80,
    "README.zh-CN.md": 80,
    "CHANGELOG.md": 10,
    "LICENSE": 15,
    "pyproject.toml": 20,
    ".gitignore": 15,
    ".gitattributes": 5,
    ".github/workflows/tests.yml": 15,
    "config/report_template.md": 100,
    "docs/methodology.md": 50,
    "docs/input_schema.md": 60,
    "src/opportunity_radar/main.py": 20,
    "src/opportunity_radar/pipeline/validate_inputs.py": 180,
    "src/opportunity_radar/pipeline/score.py": 10,
    "src/opportunity_radar/writers/markdown_writer.py": 240,
    "src/opportunity_radar/writers/html_writer.py": 50,
    "src/opportunity_radar/dashboard/helpers.py": 80,
    "tests/test_cli.py": 10,
    "tests/test_datetime_parsing.py": 25,
    "tests/test_validation.py": 35,
    "tests/test_markdown_escaping.py": 35,
    "tests/test_html_writer.py": 10,
    "tests/test_dashboard_helpers.py": 60,
    "scripts/run_demo.py": 45,
    "examples/sample_reports/weekly_opportunity_radar_en.md": 50,
}


def inspect_file(rel: str) -> tuple[int, int, int]:
    path = ROOT / rel
    raw = path.read_bytes()
    lf = raw.count(b"\n")
    cr = raw.count(b"\r")
    crlf = raw.count(b"\r\n")
    cr_only = cr - crlf
    literal_backslash_n = raw.count(b"\\n")
    return lf, cr_only, literal_backslash_n


def main() -> None:
    failed = False

    for rel in FILES_TO_CHECK:
        lf, cr_only, literal = inspect_file(rel)
        minimum = MIN_LF_COUNTS.get(rel, 1)
        print(f"{rel}: LF={lf} CR_ONLY={cr_only} LITERAL_BACKSLASH_N={literal}")

        if lf < minimum:
            print(f"  FAIL: LF count below expected minimum {minimum}")
            failed = True

        if cr_only != 0:
            print("  FAIL: CR-only line endings detected")
            failed = True

        if literal > 10:
            print("  FAIL: suspicious literal backslash-n count")
            failed = True

    if failed:
        raise SystemExit(1)

    print("line_ending_verification=passed")


if __name__ == "__main__":
    main()
