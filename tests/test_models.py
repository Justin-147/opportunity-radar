from datetime import datetime

from opportunity_radar.models import AudienceProfile, OpportunityItem


def test_opportunity_item_model_validates():
    item = OpportunityItem(
        id="item-1",
        title="AI Governance Analyst",
        url="https://example.org/item",
        source="Manual",
        source_type="manual",
        published_at=datetime(2026, 7, 1),
        category="job",
        location="Singapore",
        summary="Governance role for AI controls.",
    )

    assert item.title == "AI Governance Analyst"
    assert item.keywords == []


def test_audience_profile_model_validates():
    profile = AudienceProfile(
        id="profile",
        name="Profile",
        description="Test profile",
        target_locations=["Singapore"],
        target_domains=["AI"],
        target_roles=["Data Analyst"],
        core_skills=["Python"],
        transition_keywords=["risk"],
        avoid_keywords=["sales only"],
    )

    assert profile.target_domains == ["AI"]
