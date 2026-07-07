from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd


def discover_report_paths(project_root: Path) -> list[Path]:
    search_dirs = [
        project_root / "data" / "processed",
        project_root / "reports" / "json",
        project_root / "examples" / "sample_outputs",
    ]
    reports: list[Path] = []
    seen: set[Path] = set()
    for directory in search_dirs:
        for path in sorted(directory.glob("*.json"), reverse=True):
            if path not in seen:
                reports.append(path)
                seen.add(path)
    return reports


def load_report(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"Expected JSON object in report file: {path}")
    return data


def item_frame(items: list[dict[str, Any]]) -> pd.DataFrame:
    rows = []
    for item in items:
        keywords = item.get("keywords") or []
        if isinstance(keywords, list):
            keyword_text = ", ".join(str(keyword) for keyword in keywords)
        else:
            keyword_text = str(keywords)
        rows.append(
            {
                "title": item.get("title"),
                "category": item.get("category"),
                "company": item.get("company") or item.get("source"),
                "score": item.get("final_score"),
                "location": item.get("location"),
                "summary": item.get("summary"),
                "keywords": keyword_text,
                "suggested_action": item.get("suggested_action"),
                "url": item.get("url"),
            }
        )
    return pd.DataFrame(rows)


def category_options(frame: pd.DataFrame) -> list[str]:
    if frame.empty or "category" not in frame.columns:
        return []
    return sorted(str(value) for value in frame["category"].dropna().unique())


def markdown_path_for(report_path: Path, language: str, project_root: Path) -> Path:
    stem = report_path.stem
    if "examples" in report_path.parts and "sample_outputs" in report_path.parts:
        return project_root / "examples" / "sample_reports" / f"{stem}_{language}.md"
    return project_root / "reports" / "markdown" / f"{stem}_{language}.md"


def filter_frame(
    frame: pd.DataFrame,
    categories: list[str] | None = None,
    min_score: float = 0.0,
    keyword: str = "",
) -> pd.DataFrame:
    if frame.empty:
        return frame

    filtered = frame.copy()
    if categories:
        filtered = filtered[filtered["category"].isin(categories)]
    filtered = filtered[pd.to_numeric(filtered["score"], errors="coerce").fillna(0.0) >= min_score]

    query = keyword.strip().lower()
    if query:
        search_columns = [
            "title",
            "category",
            "company",
            "summary",
            "keywords",
            "suggested_action",
        ]
        mask = (
            filtered[search_columns]
            .fillna("")
            .astype(str)
            .apply(
                lambda row: query in " ".join(row).lower(),
                axis=1,
            )
        )
        filtered = filtered[mask]
    return filtered
