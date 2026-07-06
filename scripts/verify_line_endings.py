from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

FILES_TO_CHECK = [
    "README.md",
    "README.zh-CN.md",
    "pyproject.toml",
    ".gitignore",
    ".gitattributes",
    ".github/workflows/tests.yml",
    "src/opportunity_radar/main.py",
    "src/opportunity_radar/pipeline/score.py",
    "tests/test_cli.py",
    "examples/sample_reports/weekly_opportunity_radar_en.md",
]

MIN_LF_COUNTS = {
    "README.md": 80,
    "README.zh-CN.md": 80,
    "pyproject.toml": 20,
    ".gitignore": 15,
    ".gitattributes": 5,
    ".github/workflows/tests.yml": 15,
    "src/opportunity_radar/main.py": 20,
    "src/opportunity_radar/pipeline/score.py": 10,
    "tests/test_cli.py": 10,
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
