from datetime import datetime

from opportunity_radar.models import OpportunityItem
from opportunity_radar.pipeline.deduplicate import deduplicate_items
from opportunity_radar.pipeline.normalize import normalize_row


def test_items_normalize_correctly():
    item = normalize_row(
        {
            "title": "Risk Data Analyst",
            "url": "https://example.org/risk",
            "source": "Manual",
            "source_type": "manual",
            "published_at": "2026-07-01",
            "category": "job",
            "location": "Singapore",
            "summary": "Analyze FinTech risk data.",
            "keywords": "AI, FinTech, risk",
            "required_skills": "Python, SQL",
        }
    )

    assert item.published_at == datetime(2026, 7, 1)
    assert item.keywords == ["AI", "FinTech", "risk"]
    assert item.required_skills == ["Python", "SQL"]


def test_deduplication_removes_duplicate_url_title_company():
    first = OpportunityItem(
        id="1",
        title="AI Governance Analyst",
        url="https://example.org/item",
        source="Manual",
        source_type="manual",
        published_at=datetime(2026, 7, 1),
        category="job",
        location="Singapore",
        company="Merlion Trust Bank",
        summary="First",
    )
    duplicate = first.model_copy(update={"id": "2"})

    assert len(deduplicate_items([first, duplicate])) == 1
