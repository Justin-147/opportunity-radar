from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from opportunity_radar.models import OpportunityReport


def report_to_dict(report: OpportunityReport) -> dict[str, Any]:
    if hasattr(report, "model_dump"):
        return report.model_dump(mode="json")
    return json.loads(report.json())


def write_json_report(report: OpportunityReport, output_path: str | Path) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(report_to_dict(report), handle, ensure_ascii=False, indent=2)
    return path
