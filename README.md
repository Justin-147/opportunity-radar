# Opportunity Radar: Singapore AI & FinTech Opportunity Intelligence System

![tests](https://github.com/Justin-147/opportunity-radar/actions/workflows/tests.yml/badge.svg)

Opportunity Radar is a local-first opportunity intelligence system for technical, research, data, and engineering professionals exploring Singapore AI, FinTech, RegTech, risk analytics, data analytics, and digital transformation opportunities.

It converts curated job, policy, company, event, learning, and side-hustle signals into structured weekly opportunity briefs with relevance scoring, actionability scoring, suggested next actions, and source lists.

The project is designed as a portfolio-ready prototype and a foundation for a future newsletter, consulting service, or opportunity intelligence product.

Opportunity Radar does not provide job guarantees, immigration advice, legal advice, investment advice, automated job applications, or automated outreach services.

## Target Users

Opportunity Radar is designed for:

- research professionals transitioning into AI / data / FinTech roles;
- engineers exploring Singapore opportunities;
- data analysts looking for FinTech or RegTech roles;
- AI application builders looking for business ideas;
- professionals who want a weekly opportunity brief rather than raw job feeds.

## What It Does

- imports curated job, policy, event, company, learning, and side-hustle signals;
- normalizes them into a common `OpportunityItem` schema;
- deduplicates similar items;
- classifies items by category;
- scores relevance, actionability, freshness, credibility, and uniqueness;
- ranks opportunities;
- generates English and Chinese weekly reports;
- provides a simple Streamlit dashboard.

## What It Does Not Do

- does not scrape LinkedIn;
- does not bypass login pages;
- does not auto-apply to jobs;
- does not provide immigration or legal advice;
- does not provide investment advice;
- does not guarantee job outcomes;
- does not collect private personal data.

## Architecture

Opportunity Radar uses a deterministic local pipeline:

```text
manual CSV/YAML inputs
  -> import and normalize
  -> deduplicate and classify
  -> score and rank
  -> build report context
  -> write Markdown, HTML, and JSON
  -> inspect in Streamlit
```

## Quick Start

```powershell
cd opportunity-radar
python -m pip install -e .[dev]
python -m opportunity_radar.main generate --profile singapore_ai_fintech --mock
```

Without installing the package, run:

```powershell
$env:PYTHONPATH="src"
python -m opportunity_radar.main generate --profile singapore_ai_fintech --mock
```

## CLI Commands

Generate from bundled synthetic sample inputs:

```powershell
python -m opportunity_radar.main generate --profile singapore_ai_fintech --mock
```

Generate from a manual input directory:

```powershell
python -m opportunity_radar.main generate --profile singapore_ai_fintech --input-dir examples/sample_inputs
```

Generate and refresh stable examples:

```powershell
python -m opportunity_radar.main generate --profile singapore_ai_fintech --mock --copy-samples
```

Expected outputs:

```text
data/processed/YYYY-MM-DD_singapore_ai_fintech.json
reports/markdown/YYYY-MM-DD_singapore_ai_fintech_en.md
reports/markdown/YYYY-MM-DD_singapore_ai_fintech_zh.md
reports/html/YYYY-MM-DD_singapore_ai_fintech_en.html
reports/html/YYYY-MM-DD_singapore_ai_fintech_zh.html
```

## Dashboard

```powershell
streamlit run src/opportunity_radar/dashboard/app.py
```

The dashboard shows a report selector, total opportunities, category distribution, score distribution, top opportunities, job opportunities, side-hustle ideas, and a Markdown report preview.

## Screenshots

Screenshots can be added later to demonstrate:

- the Opportunity Dashboard;
- the generated weekly opportunity report;
- category and score distributions.

## Sample Inputs

The sample inputs are synthetic, Singapore-focused, and safe to publish:

- `examples/sample_inputs/singapore_ai_fintech_jobs.csv`
- `examples/sample_inputs/sample_policy_signals.yaml`
- `examples/sample_inputs/sample_events.yaml`
- `examples/sample_inputs/sample_side_hustle_ideas.yaml`
- `examples/sample_inputs/sample_company_signals.yaml`

## Sample Reports

- [English weekly sample report](examples/sample_reports/weekly_opportunity_radar_en.md)
- [Chinese weekly sample report](examples/sample_reports/weekly_opportunity_radar_zh.md)
- [Sample JSON output](examples/sample_outputs/weekly_opportunity_radar.json)

## Scoring Formula

```text
final_score =
  0.30 * relevance_score
+ 0.25 * actionability_score
+ 0.20 * freshness_score
+ 0.15 * credibility_score
+ 0.10 * uniqueness_score
```

- `relevance_score`: how closely the opportunity matches the selected audience profile.
- `actionability_score`: whether the item suggests a clear next step such as apply, register, build, learn, or contact.
- `freshness_score`: how recent the opportunity signal is.
- `credibility_score`: reliability of the source type.
- `uniqueness_score`: whether the item adds distinct value rather than duplicating other signals.

## Repository Structure

```text
config/                 Profiles, sources, scoring rules, report template
docs/screenshots/       Placeholder for future dashboard and report screenshots
examples/sample_inputs/ Synthetic CSV/YAML demo inputs
examples/sample_reports Curated stable sample Markdown reports
examples/sample_outputs Curated stable sample JSON output
src/opportunity_radar/  Models, pipeline, writers, CLI, dashboard
tests/                  Pytest suite
reports/                Generated Markdown/HTML/JSON outputs, ignored by Git
data/processed/         Generated processed JSON, ignored by Git
```

## Repository Hygiene

Generated reports and processed data are intentionally ignored by Git:

- `reports/`
- `data/processed/`
- `data/cache/`

Curated examples are stored under:

- `examples/sample_inputs/`
- `examples/sample_reports/`
- `examples/sample_outputs/`

## Tests

```powershell
pytest
```

## Local Verification

Before committing changes, run:

```powershell
pytest
python -m opportunity_radar.main generate --profile singapore_ai_fintech --mock
```

## Disclaimer

Opportunity Radar is an informational opportunity intelligence prototype. It does not provide job guarantees, immigration advice, legal advice, investment advice, automated job application services, or automated outreach services.
