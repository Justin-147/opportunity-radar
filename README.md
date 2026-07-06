# Opportunity Radar: Singapore AI & FinTech Opportunity Intelligence System

Opportunity Radar is a local-first opportunity intelligence prototype for technical, research, data, and engineering professionals exploring Singapore AI, FinTech, RegTech, risk analytics, and digital transformation opportunities.

It converts manually curated or public-source-style opportunity signals into structured weekly reports with relevance scoring, actionability scoring, opportunity categories, suggested actions, and source lists.

## Target Users

- Chinese research professionals transitioning into AI, data, or FinTech roles
- Engineers exploring Singapore opportunities
- Data analysts looking for FinTech, RegTech, or risk analytics roles
- AI application builders looking for business and portfolio ideas
- Professionals who want a weekly opportunity brief instead of raw job feeds

## What It Does

- Imports synthetic or manually curated CSV/YAML opportunity signals
- Normalizes jobs, events, policy signals, company signals, side-hustle ideas, and learning priorities
- Deduplicates opportunities by URL and title/company
- Scores each item by relevance, actionability, freshness, credibility, and uniqueness
- Generates English and Chinese Markdown reports
- Converts reports to HTML
- Writes processed JSON for dashboarding
- Provides a simple Streamlit dashboard

## What It Does Not Do

- No SaaS, login, payment, or multi-user system
- No automatic job applications or resume submission
- No LinkedIn scraping, paywalled scraping, private data collection, or aggressive web scraping
- No immigration advice, legal advice, investment advice, job guarantees, or automated outreach spam

## Architecture

```text
config/                 Profiles, sources, scoring rules, report template
examples/sample_inputs/ Synthetic CSV/YAML demo inputs
src/opportunity_radar/  Models, pipeline, writers, CLI, dashboard
tests/                  Pytest suite
reports/                Generated Markdown/HTML/JSON outputs
data/processed/         Processed report JSON
```

## Quick Start

```powershell
cd opportunity-radar
python -m pip install -e .
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

Outputs:

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

The dashboard shows the selected profile, generated report selector, total opportunities, category distribution, top opportunities, job opportunities, side-hustle ideas, score distribution, and a Markdown preview.

## Sample Inputs

The sample inputs are synthetic and stored in `examples/sample_inputs/`:

- `singapore_ai_fintech_jobs.csv`
- `sample_policy_signals.yaml`
- `sample_events.yaml`
- `sample_side_hustle_ideas.yaml`
- `sample_company_signals.yaml`

## Sample Reports

Stable sample outputs are stored in:

- `examples/sample_reports/weekly_opportunity_radar_en.md`
- `examples/sample_reports/weekly_opportunity_radar_zh.md`
- `examples/sample_outputs/weekly_opportunity_radar.json`

## Scoring Formula

```text
final_score =
  0.30 * relevance_score
+ 0.25 * actionability_score
+ 0.20 * freshness_score
+ 0.15 * credibility_score
+ 0.10 * uniqueness_score
```

## Tests

```powershell
pytest
```

## Disclaimer

Opportunity Radar is an informational prototype. It does not provide job guarantees, immigration advice, legal advice, investment advice, or automated job application services.
