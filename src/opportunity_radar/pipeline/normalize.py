from __future__ import annotations

import hashlib
import re
from datetime import date, datetime, time
from typing import Any

from opportunity_radar.models import OpportunityItem
from opportunity_radar.pipeline.classify import infer_category


def clean_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, float) and value != value:
        return ""
    text = str(value).strip()
    return "" if text.lower() in {"nan", "none", "null"} else text


def parse_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [clean_value(item) for item in value if clean_value(item)]
    text = clean_value(value)
    if not text:
        return []
    parts = re.split(r"[,;|]", text)
    return [part.strip() for part in parts if part.strip()]


def parse_datetime(value: Any) -> datetime:
    if isinstance(value, datetime):
        return value
    if isinstance(value, date):
        return datetime.combine(value, time.min)
    text = clean_value(value)
    if not text:
        return datetime.utcnow()
    normalized = text.replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError:
        parsed_date = datetime.strptime(text[:10], "%Y-%m-%d")
        return parsed_date
    if parsed.tzinfo is not None:
        return parsed.replace(tzinfo=None)
    return parsed


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", text.lower()).strip("-")
    return slug or "opportunity"


def make_id(row: dict[str, Any]) -> str:
    base = "|".join(
        [
            clean_value(row.get("title")),
            clean_value(row.get("company")),
            clean_value(row.get("url")),
        ]
    )
    digest = hashlib.sha1(base.encode("utf-8")).hexdigest()[:8]
    return f"{slugify(clean_value(row.get('title')))}-{digest}"


def normalize_row(row: dict[str, Any]) -> OpportunityItem:
    category = clean_value(row.get("category")) or infer_category(row)
    title = clean_value(row.get("title")) or "Untitled Opportunity"
    source = clean_value(row.get("source")) or "Manual Source"
    url = clean_value(row.get("url")) or f"https://example.org/opportunity-radar/{slugify(title)}"
    company = clean_value(row.get("company")) or None
    role = clean_value(row.get("role")) or None
    summary = clean_value(row.get("summary")) or title

    return OpportunityItem(
        id=clean_value(row.get("id")) or make_id(row),
        title=title,
        url=url,
        source=source,
        source_type=clean_value(row.get("source_type")) or "manual",
        published_at=parse_datetime(row.get("published_at")),
        category=category,
        location=clean_value(row.get("location")) or "Singapore",
        company=company,
        role=role,
        summary=summary,
        keywords=parse_list(row.get("keywords")),
        target_audience=parse_list(row.get("target_audience")),
        required_skills=parse_list(row.get("required_skills")),
        nice_to_have_skills=parse_list(row.get("nice_to_have_skills")),
        seniority=clean_value(row.get("seniority")) or None,
        remote_option=clean_value(row.get("remote_option")) or None,
        fit_reason=clean_value(row.get("fit_reason")),
        suggested_action=clean_value(row.get("suggested_action")),
        source_notes=clean_value(row.get("source_notes")),
    )


def normalize_records(records: list[dict[str, Any]]) -> list[OpportunityItem]:
    return [normalize_row(record) for record in records]
