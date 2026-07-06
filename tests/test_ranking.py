from datetime import datetime

from opportunity_radar.models import OpportunityItem
from opportunity_radar.pipeline.rank import top_n


def item(title: str, score: float) -> OpportunityItem:
    return OpportunityItem(
        id=title,
        title=title,
        url=f"https://example.org/{title}",
        source="Manual",
        source_type="manual",
        published_at=datetime(2026, 7, 1),
        category="job",
        location="Singapore",
        summary=title,
        final_score=score,
    )


def test_top_opportunities_are_sorted_by_final_score():
    ranked = top_n([item("low", 0.2), item("high", 0.9), item("mid", 0.5)], 3)

    assert [entry.title for entry in ranked] == ["high", "mid", "low"]
