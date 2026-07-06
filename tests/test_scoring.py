from datetime import datetime

from opportunity_radar.config import load_profile, load_scoring_rules
from opportunity_radar.models import OpportunityItem
from opportunity_radar.pipeline.score import (
    calculate_freshness_score,
    calculate_relevance_score,
    score_item,
)


def make_item(title: str, summary: str, published_at: datetime) -> OpportunityItem:
    return OpportunityItem(
        id=title.lower().replace(" ", "-"),
        title=title,
        url=f"https://example.org/{title}",
        source="Manual",
        source_type="manual",
        published_at=published_at,
        category="job",
        location="Singapore",
        company="Example",
        role=title,
        summary=summary,
        keywords=["AI", "FinTech", "risk"],
        required_skills=["Python", "SQL"],
    )


def test_relevance_score_higher_for_ai_fintech_risk_roles():
    profile = load_profile("singapore_ai_fintech")
    relevant = make_item(
        "AI Governance Analyst",
        "AI FinTech risk analytics governance role.",
        datetime(2026, 7, 1),
    )
    unrelated = make_item(
        "Retail Store Coordinator",
        "Sales only unrelated retail role.",
        datetime(2026, 7, 1),
    ).model_copy(update={"keywords": ["retail"], "required_skills": ["sales"]})

    assert calculate_relevance_score(relevant, profile) > calculate_relevance_score(unrelated, profile)


def test_freshness_score_higher_for_recent_items():
    rules = load_scoring_rules()
    now = datetime(2026, 7, 6)
    fresh = make_item("Fresh Role", "AI risk role.", datetime(2026, 7, 1))
    old = make_item("Old Role", "AI risk role.", datetime(2025, 12, 1))

    assert calculate_freshness_score(fresh, rules, now) > calculate_freshness_score(old, rules, now)


def test_final_score_between_zero_and_one():
    profile = load_profile("singapore_ai_fintech")
    rules = load_scoring_rules()
    scored = score_item(
        make_item("AI Application Engineer", "AI applications for FinTech risk teams.", datetime(2026, 7, 1)),
        profile,
        rules,
        datetime(2026, 7, 6),
    )

    assert 0 <= scored.final_score <= 1
