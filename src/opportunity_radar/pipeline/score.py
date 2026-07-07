from __future__ import annotations

import re
from datetime import UTC, datetime
from typing import Any

from opportunity_radar.models import AudienceProfile, OpportunityItem


def _copy_item(item: OpportunityItem, **updates: Any) -> OpportunityItem:
    if hasattr(item, "model_copy"):
        return item.model_copy(update=updates)
    return item.copy(update=updates)


def _naive_utc(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value
    return value.astimezone(UTC).replace(tzinfo=None)


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


def term_in_text(term: str, text: str) -> bool:
    normalized_term = term.strip().lower()
    if not normalized_term:
        return False

    normalized_text = text.lower()
    if " " in normalized_term:
        pattern = rf"(?<!\w){re.escape(normalized_term)}(?!\w)"
        return re.search(pattern, normalized_text, flags=re.IGNORECASE) is not None
    if len(normalized_term) <= 3 and normalized_term.isascii():
        pattern = rf"(?<![a-zA-Z0-9]){re.escape(normalized_term)}(?![a-zA-Z0-9])"
        return re.search(pattern, text, flags=re.IGNORECASE) is not None
    return normalized_term in normalized_text


def _count_hits(text: str, terms: list[str]) -> int:
    seen_terms = {term.strip().lower() for term in terms if term.strip()}
    return sum(1 for term in seen_terms if term_in_text(term, text))


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
    reference = _naive_utc(now or datetime.now(UTC))
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
    matched_domains = [term for term in profile.target_domains if term_in_text(term, text)]
    matched_roles = [term for term in profile.target_roles if term_in_text(term, text)]
    matched_skills = [term for term in profile.core_skills if term_in_text(term, text)]
    skills = matched_skills[:3] or item.required_skills[:3] or item.keywords[:3]
    skills_text = ", ".join(skills) if skills else "the profile's core skills"
    role = matched_roles[0] if matched_roles else item.role or "the target role"
    domain = matched_domains[0] if matched_domains else "the Singapore opportunity market"

    if item.category == "job":
        company_text = f" at {item.company}" if item.company else ""
        return (
            f"Good job-fit signal for {role}{company_text}: it combines {skills_text} "
            f"with Singapore or remote relevance."
        )
    if item.category == "policy":
        return (
            f"Useful policy signal for {domain}: it can be turned into a methodology note, "
            "checklist, or portfolio-ready analysis artifact."
        )
    if item.category == "event":
        return (
            f"Useful networking signal for {domain}: it can reveal hiring language, "
            f"ecosystem priorities, and practical {skills_text} examples."
        )
    if item.category == "side_hustle":
        audience = ", ".join(item.target_audience[:2]) or profile.name
        return (
            f"Promising manual-first MVP angle for {audience}, especially where {skills_text} "
            "can produce a concrete weekly deliverable."
        )
    if item.category == "company_signal":
        company = item.company or item.source
        return (
            f"Company watchlist signal from {company}: it points to role preparation around "
            f"{role}, {domain}, and {skills_text}."
        )
    if item.category == "learning":
        return (
            f"Useful learning focus for {role}: it strengthens {skills_text} evidence "
            "that can be shown in a portfolio artifact."
        )
    if matched_roles or matched_domains or matched_skills:
        matched_terms = matched_domains[:1] + matched_roles[:1] + matched_skills[:2]
        return (
            f"Relevant signal because it matches {', '.join(matched_terms)} and can support "
            "a focused next action or portfolio story."
        )
    return (
        "Relevant but exploratory signal for tracking Singapore AI, FinTech, RegTech, "
        "analytics, or digital transformation opportunities."
    )


def default_suggested_action(item: OpportunityItem) -> str:
    skills = item.required_skills[:3] or item.keywords[:3]
    skills_text = ", ".join(skills) if skills else "the strongest matching skills"
    role_or_company = item.role or item.company or item.title
    defaults = {
        "job": (
            f"Tailor one resume bullet for {role_or_company}, emphasizing {skills_text}, "
            "then apply through the source link."
        ),
        "event": (
            "Register, prepare one question, and convert the event notes into a short "
            "portfolio memo."
        ),
        "policy": "Turn this signal into a one-page methodology note or checklist.",
        "project": (
            "Build a small reproducible demo, document the decision workflow, "
            "and publish the README with synthetic data."
        ),
        "side_hustle": (
            "Create a one-page offer, validate with 5 target users, and keep the first "
            "version manual-first."
        ),
        "company_signal": (
            "Track related roles, identify the repeated skill signals, and prepare "
            "a tailored portfolio story for this company type."
        ),
        "learning": (
            "Spend one week building a small dashboard or report automation project "
            "that demonstrates this skill."
        ),
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
