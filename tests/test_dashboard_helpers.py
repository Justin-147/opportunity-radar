from pathlib import Path

from opportunity_radar.dashboard.app import filter_frame, item_frame, markdown_path_for


def test_item_frame_includes_searchable_fields():
    frame = item_frame(
        [
            {
                "title": "AI Governance Analyst",
                "category": "job",
                "company": "Merlion",
                "final_score": 0.9,
                "summary": "Governance role",
                "keywords": ["AI", "risk"],
                "url": "https://example.org",
            }
        ]
    )

    assert {"summary", "keywords", "url"}.issubset(frame.columns)


def test_filter_frame_handles_category_score_and_keyword():
    frame = item_frame(
        [
            {"title": "AI job", "category": "job", "final_score": 0.9, "summary": "risk"},
            {"title": "Old event", "category": "event", "final_score": 0.4, "summary": "meetup"},
        ]
    )

    filtered = filter_frame(frame, categories=["job"], min_score=0.8, keyword="risk")

    assert list(filtered["title"]) == ["AI job"]


def test_filter_frame_handles_empty_data():
    frame = item_frame([])

    assert filter_frame(frame).empty


def test_markdown_path_for_sample_output():
    path = Path("examples/sample_outputs/weekly_opportunity_radar.json")
    markdown_path = markdown_path_for(path, "zh")

    assert markdown_path.parts[-3:] == (
        "examples",
        "sample_reports",
        "weekly_opportunity_radar_zh.md",
    )
