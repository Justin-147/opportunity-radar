# Singapore AI & FinTech Opportunity Radar | {{ generated_at[:10] }}

> Data notice: {{ data_notice | md_text }}

## Executive Summary

{% for line in executive_summary %}
- {{ line | md_text }}
{% endfor %}

## What Changed This Week

{% for line in what_changed %}
- {{ line | md_text }}
{% endfor %}

## This Week Focus

- Primary role family: {{ this_week_focus.primary_role_family | md_text }}
- Best-fit roles this week: {{ this_week_focus.best_fit_roles | md_text }}
- Best portfolio artifact to build: {{ this_week_focus.best_portfolio_artifact | md_text }}
- Suggested networking action: {{ this_week_focus.suggested_networking_action | md_text }}

## Top Opportunities

| Opportunity | Category | Company / Source | Score | Why It Matters | Suggested Action |
|---|---|---|---:|---|---|
{% for item in top_opportunities %}
| [{{ item.title | md_cell }}]({{ item.url | safe_url }}) | {{ item.category | md_cell }} | {{ (item.company or item.source) | md_cell }} | {{ item.final_score | fmt_score }} | {{ item.fit_reason | md_cell }} | {{ item.suggested_action | md_cell }} |
{% endfor %}

## Best-Fit Roles This Week

- Role family: {{ best_fit_roles.role_family | md_text }}
- Why it fits: {{ best_fit_roles.why_it_fits | md_text }}
- Keywords to add to resume: {{ best_fit_roles.keywords_to_add | md_text }}
- Suggested application angle: {{ best_fit_roles.suggested_application_angle | md_text }}

## Top Companies to Watch

| Company / Source | Signal | Why It Matters | Suggested Action |
|---|---|---|---|
{% for company in top_companies_to_watch %}
| {{ company.company | md_cell }} | {{ company.signal | md_cell }} | {{ company.why_it_matters | md_cell }} | {{ company.suggested_action | md_cell }} |
{% endfor %}

## Portfolio Project to Build

### {{ portfolio_project.title | md_text }}

- Target user: {{ portfolio_project.target_user | md_text }}
- Problem solved: {{ portfolio_project.problem_solved | md_text }}
- MVP scope: {{ portfolio_project.mvp_scope | md_text }}
- Skills demonstrated: {{ portfolio_project.skills_demonstrated | md_text }}
- Suggested next step: {{ portfolio_project.suggested_next_step | md_text }}

## Job Opportunities

{% for item in jobs %}
### {{ (item.role or item.title) | md_text }} | {{ (item.company or "Unknown") | md_text }}

- Why it fits: {{ item.fit_reason | md_text }}
- Keywords: {{ item.keywords | join(", ") | md_text }}
- Score breakdown:
  - Relevance: {{ "%.2f"|format(item.relevance_score) }}
  - Actionability: {{ "%.2f"|format(item.actionability_score) }}
  - Freshness: {{ "%.2f"|format(item.freshness_score) }}
  - Credibility: {{ "%.2f"|format(item.credibility_score) }}
  - Uniqueness: {{ "%.2f"|format(item.uniqueness_score) }}
- Best for: {{ target_user_fit(item) | md_text }}
- Suggested action: {{ item.suggested_action | md_text }}

{% endfor %}

## Policy / Ecosystem Signals

{% for item in policy_signals %}
### {{ item.title | md_text }}

- Fact: {{ item.summary | md_text }}
- Why it matters: {{ item.fit_reason | md_text }}
- Career / project implication: {{ item.suggested_action | md_text }}

{% endfor %}

## Company Signals

{% for item in company_signals %}
### {{ (item.company or item.source) | md_text }} / {{ item.title | md_text }}

- Signal: {{ item.summary | md_text }}
- Why it matters: {{ item.fit_reason | md_text }}
- Suggested action: {{ item.suggested_action | md_text }}

{% endfor %}

## Side-Hustle / Project Ideas

{% for item in side_hustles %}
### {{ item.title | md_text }}

- Target user: {{ (item.target_audience | join(", ") if item.target_audience else target_user_fit(item)) | md_text }}
- Why now: {{ item.fit_reason | md_text }}
- MVP: {{ (item.source_notes or "Create a narrow, manual-first prototype and validate demand with 5-10 target users.") | md_text }}
- Next step: {{ item.suggested_action | md_text }}

{% endfor %}

## Learning Priorities

{% for item in learning_priorities %}
- Skill: {{ item.title | md_text }}
  Why it matters: {{ item.summary | md_text }}
  Suggested resource type: {{ item.suggested_action | md_text }}
{% endfor %}

## This Week's Action Plan

{% for action in actions %}
- {{ action | md_text }}
{% endfor %}

## Source List

| Title | Source | Date | URL |
|---|---|---|---|
{% for source in source_list %}
| {{ source.title | md_cell }} | {{ source.source | md_cell }} | {{ source.date | md_cell }} | {{ source.url | safe_url | md_cell }} |
{% endfor %}

## Disclaimer

This report is an informational opportunity intelligence prototype. It does not provide job guarantees, immigration advice, legal advice, investment advice, or automated job application services.
