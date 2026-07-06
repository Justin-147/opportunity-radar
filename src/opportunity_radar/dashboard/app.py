from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[3]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from opportunity_radar.config import load_audience_profiles  # noqa: E402


def load_reports() -> list[Path]:
    processed_dir = PROJECT_ROOT / "data" / "processed"
    return sorted(processed_dir.glob("*.json"), reverse=True)


def load_report(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def item_frame(items: list[dict]) -> pd.DataFrame:
    rows = []
    for item in items:
        rows.append(
            {
                "title": item.get("title"),
                "category": item.get("category"),
                "company": item.get("company") or item.get("source"),
                "score": item.get("final_score"),
                "location": item.get("location"),
                "action": item.get("suggested_action"),
                "url": item.get("url"),
            }
        )
    return pd.DataFrame(rows)


def markdown_path_for(report_path: Path, language: str) -> Path:
    stem = report_path.stem
    return PROJECT_ROOT / "reports" / "markdown" / f"{stem}_{language}.md"


def main() -> None:
    st.set_page_config(page_title="Opportunity Radar", layout="wide")
    st.title("Opportunity Radar")

    profiles = load_audience_profiles(PROJECT_ROOT)
    profile_ids = sorted(profiles)
    selected_profile = st.sidebar.selectbox("Profile", profile_ids)
    st.sidebar.caption(profiles[selected_profile].description)

    reports = load_reports()
    if not reports:
        st.info("No generated reports found. Run `python -m opportunity_radar.main generate --profile singapore_ai_fintech --mock` first.")
        return

    report_path = st.sidebar.selectbox(
        "Generated report", reports, format_func=lambda path: path.name
    )
    report = load_report(report_path)
    items = (
        report.get("top_opportunities", [])
        + report.get("jobs", [])
        + report.get("events", [])
        + report.get("policy_signals", [])
        + report.get("company_signals", [])
        + report.get("side_hustles", [])
        + report.get("learning_priorities", [])
    )
    frame = item_frame(items).drop_duplicates(subset=["title", "category"])

    metric_cols = st.columns(3)
    metric_cols[0].metric("Total opportunities", len(frame))
    metric_cols[1].metric("Top score", f"{frame['score'].max():.2f}" if not frame.empty else "0.00")
    metric_cols[2].metric("Categories", frame["category"].nunique() if not frame.empty else 0)

    chart_cols = st.columns(2)
    with chart_cols[0]:
        st.subheader("Category distribution")
        if not frame.empty:
            st.bar_chart(frame["category"].value_counts())
    with chart_cols[1]:
        st.subheader("Score distribution")
        if not frame.empty:
            st.bar_chart(frame[["score"]])

    st.subheader("Top opportunities")
    st.dataframe(item_frame(report.get("top_opportunities", [])), width="stretch")

    st.subheader("Job opportunities")
    st.dataframe(item_frame(report.get("jobs", [])), width="stretch")

    st.subheader("Side-hustle ideas")
    st.dataframe(item_frame(report.get("side_hustles", [])), width="stretch")

    st.subheader("Markdown report preview")
    language = st.radio("Language", ["en", "zh"], horizontal=True)
    markdown_path = markdown_path_for(report_path, language)
    if markdown_path.exists():
        st.markdown(markdown_path.read_text(encoding="utf-8"))
    else:
        st.warning(f"Markdown report not found: {markdown_path}")


if __name__ == "__main__":
    main()
