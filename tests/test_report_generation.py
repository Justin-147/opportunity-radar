from datetime import datetime

from opportunity_radar.config import load_profile
from opportunity_radar.models import OpportunityItem
from opportunity_radar.pipeline.build_context import build_report
from opportunity_radar.writers.html_writer import write_html_report
from opportunity_radar.writers.markdown_writer import render_markdown, write_markdown_report


def test_markdown_and_html_reports_are_generated(tmp_path):
    profile = load_profile("singapore_ai_fintech")
    item = OpportunityItem(
        id="job-1",
        title="AI Governance Analyst",
        url="https://example.org/job",
        source="Manual",
        source_type="manual",
        published_at=datetime(2026, 7, 1),
        category="job",
        location="Singapore",
        company="Merlion Trust Bank",
        role="AI Governance Analyst",
        summary="Governance role for AI controls.",
        keywords=["AI governance", "risk"],
        final_score=0.88,
        fit_reason="Strong fit for AI governance.",
        suggested_action="Apply with a governance portfolio artifact.",
    )
    report = build_report(profile, [item], datetime(2026, 7, 6))
    md_path = tmp_path / "report.md"
    html_path = tmp_path / "report.html"

    write_markdown_report(report, md_path, "en")
    write_html_report(render_markdown(report, "en"), html_path, report.title)

    assert md_path.exists()
    markdown_text = md_path.read_text(encoding="utf-8")
    assert "# Singapore AI & FinTech Opportunity Radar" in markdown_text
    assert "> Data notice:" in markdown_text
    assert "## What Changed This Week" in markdown_text
    assert "## This Week Focus" in markdown_text
    assert "## Top Companies to Watch" in markdown_text
    assert "## Portfolio Project to Build" in markdown_text
    assert "- Score breakdown:" in markdown_text
    assert "- Best for:" in markdown_text
    assert "## This Week's Action Plan" in markdown_text
    assert "## Disclaimer" in markdown_text
    assert html_path.exists()
    assert "<html" in html_path.read_text(encoding="utf-8")


def test_chinese_report_is_generated_with_data_notice():
    profile = load_profile("singapore_ai_fintech")
    item = OpportunityItem(
        id="policy-1",
        title="AI safeguards signal",
        url="https://example.org/policy",
        source="Manual",
        source_type="manual",
        published_at=datetime(2026, 7, 1),
        category="policy",
        location="Singapore",
        summary="Governance signal for AI controls.",
        keywords=["AI governance"],
        final_score=0.82,
    )
    report = build_report(profile, [item], datetime(2026, 7, 6))
    markdown_text = render_markdown(report, "zh")

    assert "# 新加坡 AI 与 FinTech 机会雷达" in markdown_text
    assert "> 数据说明：" in markdown_text
    assert "## 免责声明" in markdown_text
