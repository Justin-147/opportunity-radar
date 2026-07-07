from datetime import datetime

from opportunity_radar.config import load_profile
from opportunity_radar.models import OpportunityItem
from opportunity_radar.pipeline.build_context import build_report
from opportunity_radar.writers.html_writer import render_html
from opportunity_radar.writers.markdown_writer import render_markdown


def test_html_title_is_escaped():
    html = render_html("# Report", 'Bad <script>alert(1)</script>', "en")

    assert "<script>" not in html
    assert "&lt;script&gt;" in html


def test_html_language_is_limited():
    html = render_html("# Report", "Title", '"><script>')

    assert '<html lang="en">' in html


def test_html_body_does_not_render_raw_script_from_item_fields():
    profile = load_profile("singapore_ai_fintech")
    item = OpportunityItem(
        id="unsafe-html",
        title="Bad <script>alert(1)</script>",
        url="https://example.org",
        source="Manual",
        source_type="manual",
        published_at=datetime(2026, 7, 1),
        category="job",
        location="Singapore",
        company="Bank <script>",
        role="AI Risk <script>",
        summary="Summary <script>alert(1)</script>",
        keywords=["AI", "risk"],
        final_score=0.9,
        fit_reason="Fit <script>alert(1)</script>",
        suggested_action="Apply <script>alert(1)</script>",
    )
    report = build_report(profile, [item], datetime(2026, 7, 6))
    markdown = render_markdown(report, "en")
    html = render_html(markdown, report.title, "en")

    assert "<script>" not in html
    assert "&lt;script&gt;" in html
