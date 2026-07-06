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
        actions.append(
            f"Update one resume section with evidence for {top_jobs[0].title}, then map the role to one portfolio artifact."
        )
    if len(top_jobs) > 1:
        actions.append(
            f"Compare requirements from {top_jobs[0].company} and {top_jobs[1].company} to identify recurring AI, analytics, and risk skills."
        )
    if top_side_hustles:
        actions.append(
            f"Validate the side-hustle idea '{top_side_hustles[0].title}' with 5-10 target users before building more code."
        )
    while len(actions) < 3:
        actions.append("Publish one short opportunity analysis note using a synthetic or public-source-style signal.")
    return actions[:3]


def build_this_week_focus(profile: AudienceProfile) -> dict[str, str]:
    if profile.id == "singapore_ai_fintech":
        return {
            "primary_role_family": "AI Governance / Risk Analytics",
            "best_fit_roles": "AI Governance Analyst, Risk Data Analyst, RegTech Product Analyst, AI Application Engineer",
            "best_portfolio_artifact": "AI agent control checklist or risk intelligence dashboard",
            "suggested_networking_action": "register for one FinTech, RegTech, or AI governance event this week",
        }

    primary_roles = " / ".join(profile.target_roles[:2]) or "AI / analytics roles"
    return {
        "primary_role_family": primary_roles,
        "best_fit_roles": ", ".join(profile.target_roles[:4]) or primary_roles,
        "best_portfolio_artifact": "one small report automation or analytics dashboard",
        "suggested_networking_action": "join one relevant event or community discussion this week",
    }


def build_what_changed(items: list[OpportunityItem]) -> list[str]:
    top_jobs = filter_category(items, "job", 3)
    top_companies = filter_category(items, "company_signal", 2)
    top_policy = filter_category(items, "policy", 1)

    changes = []
    if top_jobs:
        roles = ", ".join(item.role or item.title for item in top_jobs[:3])
        changes.append(f"Hiring signals are strongest around {roles}.")
    if top_companies:
        companies = ", ".join(item.company or item.source for item in top_companies)
        changes.append(f"Company watchlist activity points to {companies} as useful signals to track.")
    if top_policy:
        changes.append(f"Policy and ecosystem signals continue to favor AI governance, risk controls, and digital finance talent.")
    changes.append("Portfolio-friendly opportunities cluster around AI controls, payments risk analytics, and report automation.")
    return changes[:4]


def build_best_fit_roles(profile: AudienceProfile) -> dict[str, str]:
    if profile.id == "singapore_ai_fintech":
        return {
            "role_family": "AI Governance / Risk Analytics",
            "why_it_fits": "This role family connects research, data analysis, Python, risk controls, and financial services transformation.",
            "keywords_to_add": "AI governance, risk analytics, workflow automation, Python, dashboarding, compliance analytics",
            "suggested_application_angle": "Position your background around translating complex signals into controls, dashboards, and decision-ready reports.",
        }

    return {
        "role_family": " / ".join(profile.target_roles[:2]) or "AI / analytics roles",
        "why_it_fits": "This role family matches the selected audience profile and recurring opportunity signals.",
        "keywords_to_add": ", ".join(profile.transition_keywords[:6]),
        "suggested_application_angle": "Use one concrete portfolio artifact to connect your prior experience with the target role family.",
    }


def build_top_companies_to_watch(items: list[OpportunityItem]) -> list[dict[str, str]]:
    companies = []
    for item in filter_category(items, "company_signal", 3):
        companies.append(
            {
                "company": item.company or item.source,
                "signal": item.summary,
                "why_it_matters": item.fit_reason,
                "suggested_action": item.suggested_action,
            }
        )
    return companies


def build_portfolio_project(profile: AudienceProfile, items: list[OpportunityItem]) -> dict[str, str]:
    top_side_hustles = filter_category(items, "side_hustle", 1)
    if profile.id == "singapore_ai_fintech":
        return {
            "title": "AI Agent Control Checklist or Risk Intelligence Dashboard",
            "target_user": "AI governance analysts, risk analysts, and FinTech career transitioners",
            "problem_solved": "Turns scattered AI governance and risk signals into a practical control or dashboard artifact.",
            "mvp_scope": "A one-page control checklist plus a small Streamlit dashboard using synthetic risk and policy signals.",
            "skills_demonstrated": "Python, data modeling, risk analytics, AI governance, reporting, and dashboarding",
            "suggested_next_step": "Build the checklist first, then add one synthetic dashboard view and a short methodology note.",
        }
    if top_side_hustles:
        idea = top_side_hustles[0]
        return {
            "title": idea.title,
            "target_user": ", ".join(idea.target_audience) or profile.name,
            "problem_solved": idea.summary,
            "mvp_scope": idea.source_notes or "A narrow manual-first prototype with synthetic sample data.",
            "skills_demonstrated": ", ".join(idea.required_skills or idea.keywords),
            "suggested_next_step": idea.suggested_action,
        }
    return {
        "title": "Weekly opportunity intelligence brief",
        "target_user": profile.name,
        "problem_solved": "Helps users turn fragmented signals into a weekly action plan.",
        "mvp_scope": "Curated inputs, scoring rules, Markdown report, and dashboard preview.",
        "skills_demonstrated": "Python, data modeling, scoring, reporting, and dashboarding",
        "suggested_next_step": "Ship one sample report and collect feedback from target readers.",
    }


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
        "this_week_focus": build_this_week_focus(profile),
        "best_fit_roles": build_best_fit_roles(profile),
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
    context["what_changed"] = build_what_changed(sorted_items)
    context["top_companies_to_watch"] = build_top_companies_to_watch(sorted_items)
    context["portfolio_project"] = build_portfolio_project(profile, sorted_items)
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
        what_changed=context["what_changed"],
        this_week_focus=context["this_week_focus"],
        best_fit_roles=context["best_fit_roles"],
        top_companies_to_watch=context["top_companies_to_watch"],
        portfolio_project=context["portfolio_project"],
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
