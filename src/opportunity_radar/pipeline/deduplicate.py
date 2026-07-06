from __future__ import annotations

import re

from opportunity_radar.models import OpportunityItem


def normalize_text_key(value: str | None) -> str:
    return re.sub(r"\s+", " ", (value or "").strip().lower())


def deduplicate_items(items: list[OpportunityItem]) -> list[OpportunityItem]:
    seen_urls: set[str] = set()
    seen_title_company: set[tuple[str, str]] = set()
    unique: list[OpportunityItem] = []

    for item in items:
        url_key = normalize_text_key(item.url)
        title_company_key = (
            normalize_text_key(item.title),
            normalize_text_key(item.company),
        )
        if url_key and url_key in seen_urls:
            continue
        if title_company_key in seen_title_company:
            continue
        seen_urls.add(url_key)
        seen_title_company.add(title_company_key)
        unique.append(item)
    return unique
