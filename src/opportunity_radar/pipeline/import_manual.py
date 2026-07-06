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
    records: list[dict[str, Any]] = []
    for path in sorted(root.iterdir()):
        if path.suffix.lower() in {".csv", ".yaml", ".yml"}:
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
        path = root / source["path"]
        source_records = load_records(path)
        for record in source_records:
            record.setdefault("source", source.get("name", "Manual Source"))
            record.setdefault("source_type", source.get("source_type", "manual"))
        records.extend(source_records)
    return records
