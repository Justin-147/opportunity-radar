# Singapore AI & FinTech Opportunity Radar | {{ generated_at[:10] }}

## Executive Summary

{% for line in executive_summary %}
- {{ line }}
{% endfor %}

## This Week Focus

- Primary role family: {{ this_week_focus.primary_role_family }}
- Best portfolio artifact to build: {{ this_week_focus.best_portfolio_artifact }}
- Suggested networking action: {{ this_week_focus.suggested_networking_action }}

## Top Opportunities

| Opportunity | Category | Company / Source | Score | Why It Matters | Suggested Action |
|---|---|---|---:|---|---|
{% for item in top_opportunities %}
| [{{ item.title }}]({{ item.url }}) | {{ item.category }} | {{ item.company or item.source }} | {{ "%.2f"|format(item.final_score) }} | {{ item.fit_reason }} | {{ item.suggested_action }} |
{% endfor %}

## Top Opportunity Details

{% for item in top_opportunity_details %}
### {{ item.title }} | {{ item.company or item.source }}

- Best for: {{ target_user_fit(item) }}
- Why it matters: {{ item.fit_reason }}
- Suggested action: {{ item.suggested_action }}
- Score breakdown:
  - Relevance: {{ "%.2f"|format(item.relevance_score) }}
  - Actionability: {{ "%.2f"|format(item.actionability_score) }}
  - Freshness: {{ "%.2f"|format(item.freshness_score) }}
  - Credibility: {{ "%.2f"|format(item.credibility_score) }}
  - Uniqueness: {{ "%.2f"|format(item.uniqueness_score) }}

{% endfor %}

## Job Opportunities

{% for item in jobs %}
### {{ item.role or item.title }} | {{ item.company or "Unknown" }}

- Best for: {{ target_user_fit(item) }}
- Why it fits: {{ item.fit_reason }}
- Keywords: {{ item.keywords | join(", ") }}
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
| {{ source.title }} | {{ source.source }} | {{ source.date }} | {{ source.url }} |
{% endfor %}

## Disclaimer

This report is an informational opportunity intelligence prototype. It does not provide job guarantees, immigration advice, legal advice, investment advice, or automated job application services.
