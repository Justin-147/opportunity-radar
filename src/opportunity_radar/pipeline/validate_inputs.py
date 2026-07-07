from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pandas as pd
import yaml

from opportunity_radar.pipeline.normalize import clean_value, parse_datetime

KNOWN_CATEGORIES = {
    "job",
    "event",
    "policy",
    "project",
    "side_hustle",
    "company_signal",
    "learning",
}

KNOWN_SOURCE_TYPES = {
    "company_site",
    "policy",
    "event",
    "job_board",
    "news",
    "research",
    "community",
    "manual",
}

SUPPORTED_EXTENSIONS = {".csv", ".yaml", ".yml"}


@dataclass(frozen=True)
class ValidationIssue:
    level: str
    location: str
    field: str
    message: str


def _has_value(value: Any) -> bool:
    if isinstance(value, list):
        return any(clean_value(item) for item in value)
    return bool(clean_value(value))


def _read_csv(path: Path) -> list[Any]:
    frame = pd.read_csv(path, keep_default_na=False)
    return frame.to_dict(orient="records")


def _flatten_yaml_payload(payload: Any) -> list[Any]:
    if payload is None:
        return []
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        if isinstance(payload.get("items"), list):
            return payload["items"]
        for value in payload.values():
            if isinstance(value, list):
                return value
    raise ValueError("YAML input must be a list, an 'items' list, or a mapping containing a list.")


def _read_yaml(path: Path) -> list[Any]:
    with path.open("r", encoding="utf-8") as handle:
        payload = yaml.safe_load(handle)
    return _flatten_yaml_payload(payload)


def _read_records(path: Path) -> list[Any]:
    suffix = path.suffix.lower()
    if suffix == ".csv":
        return _read_csv(path)
    if suffix in {".yaml", ".yml"}:
        return _read_yaml(path)
    raise ValueError(f"Unsupported input file type: {path.suffix}")


def _record_location(path: Path, index: int) -> str:
    return f"{path.name}:record[{index + 1}]"


def _validate_record(
    record: Any,
    location: str,
    reference_time: datetime,
) -> list[ValidationIssue]:
    if not isinstance(record, dict):
        return [
            ValidationIssue(
                level="error",
                location=location,
                field="record",
                message="Record must be a mapping/object.",
            )
        ]

    issues: list[ValidationIssue] = []
    if not _has_value(record.get("title")):
        issues.append(ValidationIssue("error", location, "title", "Missing required title."))

    published_value = record.get("published_at")
    if _has_value(published_value):
        try:
            published_at = parse_datetime(published_value)
        except ValueError as exc:
            issues.append(ValidationIssue("error", location, "published_at", str(exc)))
        else:
            age_days = (reference_time.date() - published_at.date()).days
            if age_days > 180:
                issues.append(
                    ValidationIssue(
                        "warning",
                        location,
                        "published_at",
                        "Published date is older than 180 days.",
                    )
                )

    category = clean_value(record.get("category"))
    if category and category not in KNOWN_CATEGORIES:
        issues.append(
            ValidationIssue(
                "error",
                location,
                "category",
                f"Unknown category '{category}'.",
            )
        )

    url = clean_value(record.get("url"))
    if url and not (url.startswith("http://") or url.startswith("https://")):
        issues.append(
            ValidationIssue(
                "error",
                location,
                "url",
                "URL must start with http:// or https://.",
            )
        )

    source_type = clean_value(record.get("source_type"))
    if source_type and source_type not in KNOWN_SOURCE_TYPES:
        issues.append(
            ValidationIssue(
                "error",
                location,
                "source_type",
                f"Unknown source_type '{source_type}'.",
            )
        )

    for field in ["summary", "source", "keywords", "suggested_action"]:
        if not _has_value(record.get(field)):
            issues.append(
                ValidationIssue("warning", location, field, f"Missing recommended {field}.")
            )

    return issues


def validate_input_dir(input_dir: str | Path) -> list[ValidationIssue]:
    root = Path(input_dir)
    issues: list[ValidationIssue] = []
    if not root.exists():
        return [
            ValidationIssue(
                level="error",
                location=str(root),
                field="input_dir",
                message=f"Input directory does not exist: {root}",
            )
        ]
    if not root.is_dir():
        return [
            ValidationIssue(
                level="error",
                location=str(root),
                field="input_dir",
                message=f"Input path is not a directory: {root}",
            )
        ]

    paths = [path for path in sorted(root.iterdir()) if path.suffix.lower() in SUPPORTED_EXTENSIONS]
    if not paths:
        return [
            ValidationIssue(
                level="error",
                location=str(root),
                field="input_dir",
                message=f"No supported input files found in {root}. Expected .csv, .yaml, or .yml.",
            )
        ]

    reference_time = datetime.now(UTC).replace(tzinfo=None)
    for path in paths:
        try:
            records = _read_records(path)
        except Exception as exc:
            issues.append(
                ValidationIssue(
                    level="error",
                    location=str(path),
                    field="file",
                    message=f"Unable to read input file: {exc}",
                )
            )
            continue

        for index, record in enumerate(records):
            issues.extend(_validate_record(record, _record_location(path, index), reference_time))

    return issues
