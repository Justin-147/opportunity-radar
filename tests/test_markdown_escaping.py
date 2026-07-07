from datetime import datetime

from opportunity_radar.config import load_profile
from opportunity_radar.models import OpportunityItem
from opportunity_radar.pipeline.build_context import build_report
from opportunity_radar.writers.markdown_writer import md_cell, render_markdown, safe_url


def test_md_cell_escapes_pipes_and_collapses_newlines():
    assert md_cell("AI | risk\nanalytics") == r"AI \| risk analytics"


def test_safe_url_rejects_non_http_urls():
    assert safe_url("javascript:alert(1)") == "#"


def test_markdown_tables_escape_unsafe_values_in_both_languages():
    profile = load_profile("singapore_ai_fintech")
    item = OpportunityItem(
        id="unsafe",
        title="AI | Risk Analyst",
        url="javascript:alert(1)",
        source="Manual | Source",
        source_type="manual",
        published_at=datetime(2026, 7, 1),
        category="job",
        location="Singapore",
        company="Bank | Lab",
        role="AI Risk Analyst",
        summary="Line one\nline two",
        keywords=["AI", "risk"],
        final_score=0.9,
        fit_reason="Fits | because\nit is relevant.",
        suggested_action="Apply | with a memo.",
    )
    report = build_report(profile, [item], datetime(2026, 7, 6))

    english = render_markdown(report, "en")
    chinese = render_markdown(report, "zh")

    assert r"AI \| Risk Analyst" in english
    assert "](#)" in english
    assert "Fits \\| because it is relevant." in english
    assert r"AI \| Risk Analyst" in chinese
    assert "](#)" in chinese
