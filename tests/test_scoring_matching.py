from datetime import datetime

from opportunity_radar.config import load_profile
from opportunity_radar.models import OpportunityItem
from opportunity_radar.pipeline.score import calculate_relevance_score, term_in_text


def make_item(title: str, summary: str) -> OpportunityItem:
    return OpportunityItem(
        id=title.lower().replace(" ", "-"),
        title=title,
        url="https://example.org/item",
        source="Manual",
        source_type="manual",
        published_at=datetime(2026, 7, 1),
        category="job",
        location="Singapore",
        company="Example",
        role=title,
        summary=summary,
        keywords=["AI", "FinTech", "risk"],
        required_skills=["Python", "SQL"],
    )


def test_short_ai_term_uses_word_boundary():
    assert term_in_text("AI", "AI governance")
    assert not term_in_text("AI", "paid search specialist")


def test_phrase_matching_is_case_insensitive():
    assert term_in_text("Risk Analytics", "risk analytics dashboard")


def test_avoid_keyword_reduces_relevance_score():
    profile = load_profile("singapore_ai_fintech")
    relevant = make_item("AI Governance Analyst", "AI FinTech risk analytics governance role.")
    avoided = make_item(
        "AI Governance Analyst",
        "AI FinTech risk analytics governance role with sales only cold calling.",
    )

    assert calculate_relevance_score(avoided, profile) < calculate_relevance_score(
        relevant, profile
    )
