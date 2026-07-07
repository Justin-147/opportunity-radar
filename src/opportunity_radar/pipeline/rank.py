from __future__ import annotations

from opportunity_radar.models import OpportunityItem


def sort_by_score(items: list[OpportunityItem]) -> list[OpportunityItem]:
    return sorted(items, key=lambda item: (item.final_score, item.published_at), reverse=True)


def top_n(items: list[OpportunityItem], limit: int) -> list[OpportunityItem]:
    return sort_by_score(items)[:limit]


def filter_category(
    items: list[OpportunityItem], category: str, limit: int
) -> list[OpportunityItem]:
    return top_n([item for item in items if item.category == category], limit)
