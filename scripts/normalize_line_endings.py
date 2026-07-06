from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

TARGET_SUFFIXES = {
    ".py",
    ".md",
    ".toml",
    ".yaml",
    ".yml",
    ".csv",
    ".json",
    ".gitignore",
    ".gitattributes",
}

TARGET_NAMES = {
    "Dockerfile",
    ".gitignore",
    ".gitattributes",
}

EXCLUDED_PARTS = {
    ".git",
    ".venv",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "data/processed",
    "data/cache",
    "reports/markdown",
    "reports/html",
    "reports/json",
}


def is_excluded(path: Path) -> bool:
    rel = path.relative_to(ROOT).as_posix()
    return any(part in rel for part in EXCLUDED_PARTS)


def should_process(path: Path) -> bool:
    return (
        path.is_file()
        and not is_excluded(path)
        and (path.suffix in TARGET_SUFFIXES or path.name in TARGET_NAMES)
    )


def normalize_text_bytes(raw: bytes) -> bytes:
    # Decode as UTF-8. Repository text files should be UTF-8.
    text = raw.decode("utf-8")

    # If the file is a fake newline blob with many literal \n and very few real LF,
    # convert escaped newline markers into real line breaks.
    literal_newlines = text.count("\\n")
    real_lf = text.count("\n")
    if literal_newlines > 10 and real_lf < 5:
        text = text.replace("\\r\\n", "\n")
        text = text.replace("\\n", "\n")

    # Normalize CRLF and CR-only to LF.
    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    # Ensure exactly one final newline.
    text = text.rstrip("\n") + "\n"
    return text.encode("utf-8")


def main() -> None:
    changed = []
    checked = []

    for path in sorted(ROOT.rglob("*")):
        if not should_process(path):
            continue

        raw = path.read_bytes()
        new = normalize_text_bytes(raw)
        checked.append(path.relative_to(ROOT).as_posix())

        if new != raw:
            path.write_bytes(new)
            changed.append(path.relative_to(ROOT).as_posix())

    print("Checked files:")
    for item in checked:
        print(f"  {item}")

    print("\nChanged files:")
    for item in changed:
        print(f"  {item}")

    print(f"\nchecked_count={len(checked)}")
    print(f"changed_count={len(changed)}")


if __name__ == "__main__":
    main()
