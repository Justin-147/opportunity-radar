# Singapore AI & FinTech Opportunity Radar | {{ generated_at[:10] }}

> Data notice: {{ data_notice | md_cell }}

## Executive Summary

{% for line in executive_summary %}
- {{ line }}
{% endfor %}

## What Changed This Week

{% for line in what_changed %}
- {{ line }}
{% endfor %}

## This Week Focus

- Primary role family: {{ this_week_focus.primary_role_family }}
- Best-fit roles this week: {{ this_week_focus.best_fit_roles }}
- Best portfolio artifact to build: {{ this_week_focus.best_portfolio_artifact }}
- Suggested networking action: {{ this_week_focus.suggested_networking_action }}

## Top Opportunities

| Opportunity | Category | Company / Source | Score | Why It Matters | Suggested Action |
|---|---|---|---:|---|---|
{% for item in top_opportunities %}
| [{{ item.title | md_cell }}]({{ item.url | safe_url }}) | {{ item.category | md_cell }} | {{ (item.company or item.source) | md_cell }} | {{ item.final_score | fmt_score }} | {{ item.fit_reason | md_cell }} | {{ item.suggested_action | md_cell }} |
{% endfor %}

## Best-Fit Roles This Week

- Role family: {{ best_fit_roles.role_family }}
- Why it fits: {{ best_fit_roles.why_it_fits }}
- Keywords to add to resume: {{ best_fit_roles.keywords_to_add }}
- Suggested application angle: {{ best_fit_roles.suggested_application_angle }}

## Top Companies to Watch

| Company / Source | Signal | Why It Matters | Suggested Action |
|---|---|---|---|
{% for company in top_companies_to_watch %}
| {{ company.company | md_cell }} | {{ company.signal | md_cell }} | {{ company.why_it_matters | md_cell }} | {{ company.suggested_action | md_cell }} |
{% endfor %}

## Portfolio Project to Build

### {{ portfolio_project.title }}

- Target user: {{ portfolio_project.target_user }}
- Problem solved: {{ portfolio_project.problem_solved }}
- MVP scope: {{ portfolio_project.mvp_scope }}
- Skills demonstrated: {{ portfolio_project.skills_demonstrated }}
- Suggested next step: {{ portfolio_project.suggested_next_step }}

## Job Opportunities

{% for item in jobs %}
### {{ item.role or item.title }} | {{ item.company or "Unknown" }}

- Why it fits: {{ item.fit_reason }}
- Keywords: {{ item.keywords | join(", ") }}
- Score breakdown:
  - Relevance: {{ "%.2f"|format(item.relevance_score) }}
  - Actionability: {{ "%.2f"|format(item.actionability_score) }}
  - Freshness: {{ "%.2f"|format(item.freshness_score) }}
  - Credibility: {{ "%.2f"|format(item.credibility_score) }}
  - Uniqueness: {{ "%.2f"|format(item.uniqueness_score) }}
- Best for: {{ target_user_fit(item) }}
- Suggested action: {{ item.suggested_action }}

{% endfor %}

## Policy / Ecosystem Signals

{% for item in policy_signals %}
### {{ item.title }}

- Fact: {{ item.summary }}
- Why it matters: {{ item.fit_reason }}
- Career / project implication: {{ item.suggested_action }}

{% endfor %}

## Company Signals

{% for item in company_signals %}
### {{ item.company or item.source }} / {{ item.title }}

- Signal: {{ item.summary }}
- Why it matters: {{ item.fit_reason }}
- Suggested action: {{ item.suggested_action }}

{% endfor %}

## Side-Hustle / Project Ideas

{% for item in side_hustles %}
### {{ item.title }}

- Target user: {{ item.target_audience | join(", ") if item.target_audience else target_user_fit(item) }}
- Why now: {{ item.fit_reason }}
- MVP: {{ item.source_notes or "Create a narrow, manual-first prototype and validate demand with 5-10 target users." }}
- Next step: {{ item.suggested_action }}

{% endfor %}

## Learning Priorities

{% for item in learning_priorities %}
- Skill: {{ item.title }}
  Why it matters: {{ item.summary }}
  Suggested resource type: {{ item.suggested_action }}
{% endfor %}

## This Week's Action Plan

{% for action in actions %}
- {{ action }}
{% endfor %}

## Source List

| Title | Source | Date | URL |
|---|---|---|---|
{% for source in source_list %}
| {{ source.title | md_cell }} | {{ source.source | md_cell }} | {{ source.date | md_cell }} | {{ source.url | safe_url | md_cell }} |
{% endfor %}

## Disclaimer

This report is an informational opportunity intelligence prototype. It does not provide job guarantees, immigration advice, legal advice, investment advice, or automated job application services.
