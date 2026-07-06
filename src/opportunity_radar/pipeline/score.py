from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from opportunity_radar.models import AudienceProfile, OpportunityItem


def _copy_item(item: OpportunityItem, **updates: Any) -> OpportunityItem:
    if hasattr(item, "model_copy"):
        return item.model_copy(update=updates)
    return item.copy(update=updates)


def _naive_utc(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value
    return value.astimezone(timezone.utc).replace(tzinfo=None)


def _item_text(item: OpportunityItem) -> str:
    parts = [
        item.title,
        item.summary,
        item.company or "",
        item.role or "",
        item.location,
        " ".join(item.keywords),
        " ".join(item.required_skills),
    ]
    return " ".join(parts).lower()


def _count_hits(text: str, terms: list[str]) -> int:
    return sum(1 for term in terms if term.lower() in text)


def _clamp(value: float) -> float:
    return max(0.0, min(1.0, value))


def calculate_relevance_score(item: OpportunityItem, profile: AudienceProfile) -> float:
    text = _item_text(item)
    domain_hits = _count_hits(text, profile.target_domains)
    role_hits = _count_hits(text, profile.target_roles)
    transition_hits = _count_hits(text, profile.transition_keywords)
    skill_hits = _count_hits(text, profile.core_skills)
    avoid_hits = _count_hits(text, profile.avoid_keywords)
    location_hit = _count_hits(item.location.lower(), profile.target_locations)

    score = 0.18
    score += min(domain_hits, 4) * 0.12
    score += min(role_hits, 2) * 0.15
    score += min(transition_hits, 5) * 0.07
    score += min(skill_hits, 4) * 0.05
    score += min(location_hit, 1) * 0.05
    if avoid_hits:
        score -= 0.45
    return round(_clamp(score), 4)


def calculate_actionability_score(item: OpportunityItem) -> float:
    base_by_category = {
        "job": 0.72,
        "event": 0.76,
        "policy": 0.48,
        "project": 0.66,
        "side_hustle": 0.70,
        "company_signal": 0.55,
        "learning": 0.62,
    }
    text = _item_text(item) + " " + item.suggested_action.lower()
    action_words = ["apply", "register", "build", "learn", "contact", "prepare", "submit", "track"]
    score = base_by_category.get(item.category, 0.50)
    score += min(_count_hits(text, action_words), 3) * 0.08
    if item.url:
        score += 0.04
    if item.suggested_action:
        score += 0.08
    return round(_clamp(score), 4)


def calculate_freshness_score(
    item: OpportunityItem, rules: dict[str, Any], now: datetime | None = None
) -> float:
    thresholds = rules.get("freshness_days", {})
    fresh_days = int(thresholds.get("fresh", 14))
    recent_days = int(thresholds.get("recent", 45))
    stale_days = int(thresholds.get("stale", 120))
    reference = _naive_utc(now or datetime.now(timezone.utc))
    published = _naive_utc(item.published_at)
    age_days = max(0, (reference.date() - published.date()).days)

    if age_days <= fresh_days:
        return 1.0
    if age_days <= recent_days:
        return 0.78
    if age_days <= stale_days:
        return 0.55
    return 0.25


def calculate_credibility_score(item: OpportunityItem, rules: dict[str, Any]) -> float:
    credibility = rules.get("source_credibility", {})
    return float(credibility.get(item.source_type, credibility.get("manual", 0.65)))


def calculate_uniqueness_score(item: OpportunityItem) -> float:
    score = 0.48
    if len(item.summary.split()) >= 14:
        score += 0.16
    if len(item.keywords) >= 3:
        score += 0.12
    if item.company:
        score += 0.08
    if item.source_notes:
        score += 0.08
    if item.category in {"policy", "side_hustle", "company_signal"}:
        score += 0.06
    return round(_clamp(score), 4)


def default_fit_reason(item: OpportunityItem, profile: AudienceProfile) -> str:
    text = _item_text(item)
    matched_domains = [term for term in profile.target_domains if term.lower() in text]
    matched_roles = [term for term in profile.target_roles if term.lower() in text]
    matched_terms = matched_domains[:2] + matched_roles[:1]
    if matched_terms:
        return f"Strong fit for {', '.join(matched_terms)} because it connects market signal, skills, and a clear next action."
    if item.category == "learning":
        return "Useful learning focus because it supports the target Singapore AI and FinTech transition profile."
    return "Relevant signal for tracking Singapore AI, FinTech, RegTech, analytics, or digital transformation opportunities."


def default_suggested_action(item: OpportunityItem) -> str:
    defaults = {
        "job": "Update your resume with AI governance, risk analytics, and workflow automation evidence, then apply through the company careers page.",
        "event": "Register for the event and prepare one question about AI governance, RegTech adoption, or Singapore FinTech hiring signals.",
        "policy": "Write a one-page analysis note that turns this policy signal into a portfolio project or interview talking point.",
        "project": "Build a small reproducible demo, document the decision workflow, and publish the README with synthetic data.",
        "side_hustle": "Build a one-page landing page and validate demand with 10 target users before writing more code.",
        "company_signal": "Track related roles, identify the repeated skill signals, and prepare a tailored portfolio story for this company type.",
        "learning": "Spend one week building a small dashboard or report automation project that demonstrates this skill.",
    }
    return defaults.get(item.category, "Review the signal and decide one concrete next step.")


def score_item(
    item: OpportunityItem,
    profile: AudienceProfile,
    rules: dict[str, Any],
    now: datetime | None = None,
) -> OpportunityItem:
    relevance = calculate_relevance_score(item, profile)
    actionability = calculate_actionability_score(item)
    freshness = calculate_freshness_score(item, rules, now)
    credibility = calculate_credibility_score(item, rules)
    uniqueness = calculate_uniqueness_score(item)
    weights = rules.get("weights", {})
    final_score = (
        float(weights.get("relevance_score", 0.30)) * relevance
        + float(weights.get("actionability_score", 0.25)) * actionability
        + float(weights.get("freshness_score", 0.20)) * freshness
        + float(weights.get("credibility_score", 0.15)) * credibility
        + float(weights.get("uniqueness_score", 0.10)) * uniqueness
    )

    return _copy_item(
        item,
        relevance_score=round(relevance, 4),
        actionability_score=round(actionability, 4),
        freshness_score=round(freshness, 4),
        credibility_score=round(credibility, 4),
        uniqueness_score=round(uniqueness, 4),
        final_score=round(_clamp(final_score), 4),
        fit_reason=item.fit_reason or default_fit_reason(item, profile),
        suggested_action=item.suggested_action or default_suggested_action(item),
    )


def score_items(
    items: list[OpportunityItem],
    profile: AudienceProfile,
    rules: dict[str, Any],
    now: datetime | None = None,
) -> list[OpportunityItem]:
    return [score_item(item, profile, rules, now) for item in items]
