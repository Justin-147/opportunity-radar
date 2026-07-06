from __future__ import annotations

from datetime import datetime, timezone

from opportunity_radar.models import AudienceProfile, OpportunityItem, OpportunityReport
from opportunity_radar.pipeline.rank import filter_category, top_n


def build_executive_summary(profile: AudienceProfile, items: list[OpportunityItem]) -> list[str]:
    top_items = top_n(items, 3)
    top_categories = []
    for item in top_items:
        if item.category not in top_categories:
            top_categories.append(item.category)
    categories_text = ", ".join(top_categories) or "jobs, policy signals, and project ideas"
    best_roles = ", ".join(profile.target_roles[:3])
    return [
        f"Strongest signals this week cluster around {categories_text} for the {profile.name} audience.",
        f"The best role categories to watch are {best_roles}, supported by analytics, governance, and automation skills.",
        "The most portfolio-friendly direction is to convert policy, company, and job signals into small report automation or risk analytics artifacts.",
        "Recommended focus this week: pick one job family, one portfolio artifact, and one networking or event action.",
    ]


def build_actions(items: list[OpportunityItem]) -> list[str]:
    top_jobs = filter_category(items, "job", 2)
    top_side_hustles = filter_category(items, "side_hustle", 1)
    actions = []
    if top_jobs:
        actions.append(f"Tailor a resume and portfolio story for {top_jobs[0].title}.")
    if len(top_jobs) > 1:
        actions.append(f"Compare requirements from {top_jobs[0].company} and {top_jobs[1].company} to find recurring skill evidence.")
    if top_side_hustles:
        actions.append(f"Validate the side-hustle idea '{top_side_hustles[0].title}' with 3 target users.")
    while len(actions) < 3:
        actions.append("Publish one short opportunity analysis note using a synthetic or public-source-style signal.")
    return actions[:3]


def build_source_list(items: list[OpportunityItem]) -> list[dict[str, str]]:
    sources = []
    for item in top_n(items, 30):
        sources.append(
            {
                "title": item.title,
                "source": item.source,
                "date": item.published_at.date().isoformat(),
                "url": item.url,
            }
        )
    return sources


def build_report_context(
    profile: AudienceProfile,
    items: list[OpportunityItem],
    generated_at: datetime | None = None,
) -> dict:
    generated = generated_at or datetime.now(timezone.utc).replace(tzinfo=None)
    sorted_items = top_n(items, len(items))
    context = {
        "profile_name": profile.name,
        "generated_at": generated.isoformat(timespec="seconds"),
        "top_opportunities": top_n(sorted_items, 10),
        "jobs": filter_category(sorted_items, "job", 8),
        "events": filter_category(sorted_items, "event", 5),
        "policy_signals": filter_category(sorted_items, "policy", 5),
        "side_hustles": filter_category(sorted_items, "side_hustle", 5),
        "company_signals": filter_category(sorted_items, "company_signal", 5),
        "learning_priorities": filter_category(sorted_items, "learning", 5),
        "actions": build_actions(sorted_items),
        "source_list": build_source_list(sorted_items),
    }
    context["executive_summary"] = build_executive_summary(profile, sorted_items)
    return context


def build_report(
    profile: AudienceProfile,
    items: list[OpportunityItem],
    generated_at: datetime | None = None,
) -> OpportunityReport:
    generated = generated_at or datetime.now(timezone.utc).replace(tzinfo=None)
    context = build_report_context(profile, items, generated)
    date_label = generated.date().isoformat()
    return OpportunityReport(
        id=f"{date_label}_{profile.id}",
        profile=profile.id,
        generated_at=generated,
        title=f"Singapore AI & FinTech Opportunity Radar | {date_label}",
        executive_summary=context["executive_summary"],
        top_opportunities=context["top_opportunities"],
        jobs=context["jobs"],
        events=context["events"],
        policy_signals=context["policy_signals"],
        side_hustles=context["side_hustles"],
        company_signals=context["company_signals"],
        learning_priorities=context["learning_priorities"],
        actions=context["actions"],
        source_list=context["source_list"],
    )
