from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import pandas as pd
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[3]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from opportunity_radar.config import load_audience_profiles  # noqa: E402


def load_reports() -> list[Path]:
    search_dirs = [
        PROJECT_ROOT / "data" / "processed",
        PROJECT_ROOT / "reports" / "json",
        PROJECT_ROOT / "examples" / "sample_outputs",
    ]
    reports: list[Path] = []
    seen: set[Path] = set()
    for directory in search_dirs:
        for path in sorted(directory.glob("*.json"), reverse=True):
            if path not in seen:
                reports.append(path)
                seen.add(path)
    return reports


def load_report(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def item_frame(items: list[dict[str, Any]]) -> pd.DataFrame:
    rows = []
    for item in items:
        keywords = item.get("keywords") or []
        if isinstance(keywords, list):
            keyword_text = ", ".join(str(keyword) for keyword in keywords)
        else:
            keyword_text = str(keywords)
        rows.append(
            {
                "title": item.get("title"),
                "category": item.get("category"),
                "company": item.get("company") or item.get("source"),
                "score": item.get("final_score"),
                "location": item.get("location"),
                "summary": item.get("summary"),
                "keywords": keyword_text,
                "action": item.get("suggested_action"),
                "url": item.get("url"),
            }
        )
    return pd.DataFrame(rows)


def markdown_path_for(report_path: Path, language: str) -> Path:
    stem = report_path.stem
    if "examples" in report_path.parts and "sample_outputs" in report_path.parts:
        return PROJECT_ROOT / "examples" / "sample_reports" / f"{stem}_{language}.md"
    return PROJECT_ROOT / "reports" / "markdown" / f"{stem}_{language}.md"


def filter_frame(
    frame: pd.DataFrame,
    categories: list[str] | None = None,
    min_score: float = 0.0,
    keyword: str = "",
) -> pd.DataFrame:
    if frame.empty:
        return frame

    filtered = frame.copy()
    if categories:
        filtered = filtered[filtered["category"].isin(categories)]
    filtered = filtered[pd.to_numeric(filtered["score"], errors="coerce").fillna(0.0) >= min_score]

    query = keyword.strip().lower()
    if query:
        search_columns = ["title", "category", "company", "summary", "keywords"]
        mask = (
            filtered[search_columns]
            .fillna("")
            .astype(str)
            .apply(
                lambda row: query in " ".join(row).lower(),
                axis=1,
            )
        )
        filtered = filtered[mask]
    return filtered


def link_column_config() -> dict[str, Any] | None:
    try:
        return {"url": st.column_config.LinkColumn("url")}
    except Exception:
        return None


def show_frame(frame: pd.DataFrame) -> None:
    column_config = link_column_config()
    if column_config:
        st.dataframe(frame, use_container_width=True, column_config=column_config)
    else:
        st.dataframe(frame, use_container_width=True)


def main() -> None:
    st.set_page_config(page_title="Opportunity Radar", layout="wide")
    st.title("Opportunity Radar")

    profiles = load_audience_profiles(PROJECT_ROOT)
    profile_ids = sorted(profiles)
    selected_profile = st.sidebar.selectbox("Profile", profile_ids)
    st.sidebar.caption(profiles[selected_profile].description)

    reports = load_reports()
    if not reports:
        st.info(
            "No generated or sample reports found. Run "
            "`python -m opportunity_radar.main generate "
            "--profile singapore_ai_fintech --mock` first."
        )
        return

    report_path = st.sidebar.selectbox(
        "Generated report", reports, format_func=lambda path: path.name
    )
    report = load_report(report_path)
    language = st.sidebar.radio("Language", ["en", "zh"], horizontal=True)
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
    categories = sorted(
        value for value in frame.get("category", pd.Series(dtype=str)).dropna().unique()
    )
    selected_categories = st.sidebar.multiselect("Category", categories, default=categories)
    min_score = st.sidebar.slider("Minimum score", 0.0, 1.0, 0.0, 0.05)
    keyword = st.sidebar.text_input("Search")
    filtered_frame = filter_frame(frame, selected_categories, min_score, keyword)

    metric_cols = st.columns(3)
    metric_cols[0].metric("Total opportunities", len(filtered_frame))
    metric_cols[1].metric(
        "Top score",
        f"{filtered_frame['score'].max():.2f}" if not filtered_frame.empty else "0.00",
    )
    metric_cols[2].metric(
        "Categories",
        filtered_frame["category"].nunique() if not filtered_frame.empty else 0,
    )

    focus = report.get("this_week_focus", {})
    if focus:
        st.subheader("This Week Focus")
        focus_cols = st.columns(4)
        focus_cols[0].metric("Role family", focus.get("primary_role_family", "n/a"))
        focus_cols[1].metric("Best-fit roles", focus.get("best_fit_roles", "n/a"))
        focus_cols[2].metric("Portfolio artifact", focus.get("best_portfolio_artifact", "n/a"))
        focus_cols[3].metric("Networking action", focus.get("suggested_networking_action", "n/a"))

    chart_cols = st.columns(2)
    with chart_cols[0]:
        st.subheader("Category distribution")
        if not filtered_frame.empty:
            st.bar_chart(filtered_frame["category"].value_counts())
    with chart_cols[1]:
        st.subheader("Score distribution")
        if not filtered_frame.empty:
            st.bar_chart(filtered_frame[["score"]])

    if filtered_frame.empty:
        st.warning("No opportunities match the selected filters.")
        return

    st.subheader("Top opportunities")
    show_frame(
        filter_frame(
            item_frame(report.get("top_opportunities", [])), selected_categories, min_score, keyword
        )
    )

    st.subheader("Job opportunities")
    show_frame(
        filter_frame(item_frame(report.get("jobs", [])), selected_categories, min_score, keyword)
    )

    st.subheader("Side-hustle ideas")
    show_frame(
        filter_frame(
            item_frame(report.get("side_hustles", [])), selected_categories, min_score, keyword
        )
    )

    st.subheader("Markdown report preview")
    markdown_path = markdown_path_for(report_path, language)
    if markdown_path.exists():
        st.markdown(markdown_path.read_text(encoding="utf-8"))
    else:
        st.warning(f"Markdown report not found: {markdown_path}")


if __name__ == "__main__":
    main()
