from datetime import datetime

from opportunity_radar.config import load_profile
from opportunity_radar.models import OpportunityItem
from opportunity_radar.pipeline.score import default_fit_reason, default_suggested_action


def make_item(category: str, title: str = "AI Governance Analyst") -> OpportunityItem:
    return OpportunityItem(
        id=f"{category}-item",
        title=title,
        url="https://example.org/item",
        source="Manual",
        source_type="manual",
        published_at=datetime(2026, 7, 1),
        category=category,
        location="Singapore",
        company="Merlion Trust Bank",
        role="AI Governance Analyst",
        summary="AI governance risk analytics signal for Singapore FinTech teams.",
        keywords=["AI governance", "risk analytics"],
        required_skills=["Python", "risk analytics", "reporting"],
        target_audience=["career transitioners"],
    )


def test_job_action_mentions_role_or_company():
    action = default_suggested_action(make_item("job"))

    assert "AI Governance Analyst" in action or "Merlion Trust Bank" in action


def test_side_hustle_action_mentions_user_validation():
    action = default_suggested_action(make_item("side_hustle", "AI governance checklist"))

    assert "validate with 5 target users" in action


def test_policy_action_mentions_methodology_or_checklist():
    action = default_suggested_action(make_item("policy", "AI policy signal"))

    assert "methodology" in action or "checklist" in action


def test_default_fit_reasons_are_category_specific():
    profile = load_profile("singapore_ai_fintech")
    reasons = {
        default_fit_reason(make_item("job"), profile),
        default_fit_reason(make_item("policy"), profile),
        default_fit_reason(make_item("side_hustle"), profile),
    }

    assert len(reasons) == 3
