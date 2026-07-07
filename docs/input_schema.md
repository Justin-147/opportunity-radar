# Input Schema

Opportunity Radar accepts `.csv`, `.yaml`, and `.yml` files in a manual input directory.
YAML files may be a list, an `items` list, or a mapping containing a list.

## Required Field

- `title`: human-readable opportunity title.

## Recommended Fields

- `company`
- `location`
- `role`
- `category`
- `source`
- `source_type`
- `url`
- `published_at`
- `summary`
- `keywords`
- `required_skills`
- `seniority`
- `remote_option`
- `target_audience`
- `suggested_action`
- `source_notes`

Valid categories are `job`, `event`, `policy`, `project`, `side_hustle`,
`company_signal`, and `learning`.

Valid source types are `company_site`, `policy`, `event`, `job_board`, `news`,
`research`, `community`, and `manual`.

## CSV Example

```csv
title,company,category,source,source_type,url,published_at,summary,keywords,required_skills
AI Governance Analyst,Merlion Trust Bank,job,Manual,manual,https://example.org/job,2026-07-01,Governance role for AI controls,"AI governance,risk","Python,policy analysis"
```

## YAML Example

```yaml
items:
  - title: AI governance checklist product
    category: side_hustle
    source: Manual Idea Backlog
    source_type: manual
    url: https://example.org/ideas/ai-governance-checklist
    published_at: 2026-07-02
    summary: Manual-first checklist for AI application builders.
    keywords:
      - AI governance
      - controls
    required_skills:
      - Python
      - risk analysis
    target_audience:
      - AI application builders
    suggested_action: Validate the offer with five target users.
```

## Validation

Run:

```bash
python -m opportunity_radar.main validate --input-dir examples/sample_inputs
```

Validation fails on missing titles, invalid dates, unsupported categories, invalid URLs,
unknown source types, unreadable files, or unsupported directory structure. It warns on missing
recommended fields and stale `published_at` values.
