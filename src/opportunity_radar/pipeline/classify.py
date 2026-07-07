from __future__ import annotations

from typing import Any

from opportunity_radar.models import OpportunityItem

VALID_CATEGORIES = {
    "job",
    "event",
    "policy",
    "project",
    "side_hustle",
    "company_signal",
    "learning",
}


def infer_category(payload: dict[str, Any] | OpportunityItem) -> str:
    if isinstance(payload, OpportunityItem):
        current = payload.category
        text = " ".join(
            [
                payload.title,
                payload.summary,
                payload.role or "",
                payload.company or "",
                " ".join(payload.keywords),
            ]
        ).lower()
    else:
        current = str(payload.get("category", "") or "").strip()
        text = " ".join(str(value) for value in payload.values()).lower()

    if current in VALID_CATEGORIES:
        return current
    if any(
        word in text for word in ["hackathon", "webinar", "conference", "meetup", "accelerator"]
    ):
        return "event"
    if any(word in text for word in ["policy", "regulator", "framework", "initiative"]):
        return "policy"
    if any(word in text for word in ["service", "product", "template", "subscription", "mvp"]):
        return "side_hustle"
    if any(word in text for word in ["learn", "course", "skill", "resource"]):
        return "learning"
    if "company_signal" in text or "expanding" in text or "hiring signal" in text:
        return "company_signal"
    if "role" in text or "analyst" in text or "engineer" in text:
        return "job"
    return "project"


def _copy_item(item: OpportunityItem, **updates: Any) -> OpportunityItem:
    if hasattr(item, "model_copy"):
        return item.model_copy(update=updates)
    return item.copy(update=updates)


def classify_item(item: OpportunityItem) -> OpportunityItem:
    category = infer_category(item)
    if category == item.category:
        return item
    return _copy_item(item, category=category)
