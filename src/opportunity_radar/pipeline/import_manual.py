from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd
import yaml


def load_csv(path: str | Path) -> list[dict[str, Any]]:
    frame = pd.read_csv(path, keep_default_na=False)
    records = frame.to_dict(orient="records")
    for record in records:
        record.setdefault("source_file", str(path))
    return records


def _flatten_yaml_payload(payload: Any) -> list[dict[str, Any]]:
    if payload is None:
        return []
    if isinstance(payload, list):
        return [row for row in payload if isinstance(row, dict)]
    if isinstance(payload, dict):
        if isinstance(payload.get("items"), list):
            return [row for row in payload["items"] if isinstance(row, dict)]
        for value in payload.values():
            if isinstance(value, list):
                return [row for row in value if isinstance(row, dict)]
    raise ValueError("YAML input must contain a list of records")


def load_yaml_records(path: str | Path) -> list[dict[str, Any]]:
    with Path(path).open("r", encoding="utf-8") as handle:
        payload = yaml.safe_load(handle)
    records = _flatten_yaml_payload(payload)
    for record in records:
        record.setdefault("source_file", str(path))
    return records


def load_records(path: str | Path) -> list[dict[str, Any]]:
    resolved = Path(path)
    suffix = resolved.suffix.lower()
    if suffix == ".csv":
        return load_csv(resolved)
    if suffix in {".yaml", ".yml"}:
        return load_yaml_records(resolved)
    raise ValueError(f"Unsupported manual input type: {resolved}")


def load_manual_inputs(input_dir: str | Path) -> list[dict[str, Any]]:
    root = Path(input_dir)
    if not root.exists():
        raise ValueError(f"Input directory does not exist: {root}")
    if not root.is_dir():
        raise ValueError(f"Input path is not a directory: {root}")

    supported_files = [
        path for path in sorted(root.iterdir()) if path.suffix.lower() in {".csv", ".yaml", ".yml"}
    ]
    if not supported_files:
        raise ValueError(
            f"No supported input files found in {root}. Expected .csv, .yaml, or .yml."
        )

    records: list[dict[str, Any]] = []
    for path in supported_files:
        records.extend(load_records(path))
    return records


def load_records_from_sources(
    sources: list[dict[str, Any]], project_root: str | Path
) -> list[dict[str, Any]]:
    root = Path(project_root)
    records: list[dict[str, Any]] = []
    for source in sources:
        if not source.get("enabled", True):
            continue
        source_name = source.get("name", "Unnamed source")
        if not source.get("path"):
            raise ValueError(f"Source '{source_name}' is missing required path field.")
        path = root / source["path"]
        if not path.exists():
            raise ValueError(f"Source '{source_name}' file does not exist: {path}")
        try:
            source_records = load_records(path)
        except Exception as exc:
            raise ValueError(f"Failed to load source '{source_name}' from {path}: {exc}") from exc
        for record in source_records:
            record.setdefault("source", source.get("name", "Manual Source"))
            record.setdefault("source_type", source.get("source_type", "manual"))
        records.extend(source_records)
    return records
