from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from opportunity_radar.models import AudienceProfile


def get_project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def load_yaml(path: str | Path) -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    if not isinstance(data, dict):
        raise ValueError(f"Expected YAML mapping in {path}")
    return data


def load_audience_profiles(project_root: Path | None = None) -> dict[str, AudienceProfile]:
    root = project_root or get_project_root()
    raw = load_yaml(root / "config" / "audience_profiles.yaml")
    profiles = {}
    for profile_id, payload in raw.get("profiles", {}).items():
        profiles[profile_id] = AudienceProfile(id=profile_id, **payload)
    return profiles


def load_profile(profile_id: str, project_root: Path | None = None) -> AudienceProfile:
    profiles = load_audience_profiles(project_root)
    if profile_id not in profiles:
        known = ", ".join(sorted(profiles)) or "none"
        raise KeyError(f"Unknown profile '{profile_id}'. Known profiles: {known}")
    return profiles[profile_id]


def load_scoring_rules(project_root: Path | None = None) -> dict[str, Any]:
    root = project_root or get_project_root()
    return load_yaml(root / "config" / "scoring_rules.yaml")


def load_sources(project_root: Path | None = None) -> list[dict[str, Any]]:
    root = project_root or get_project_root()
    raw = load_yaml(root / "config" / "sources.yaml")
    return list(raw.get("sources", []))
