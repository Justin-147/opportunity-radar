# Methodology

Opportunity Radar is a local-first opportunity intelligence prototype. Demo reports use
synthetic, Singapore-focused sample signals so the repository can be reviewed without
scraping private, logged-in, paid, or platform-restricted data.

## Data Boundaries

- Sample inputs are synthetic and safe to publish.
- Real usage should replace sample inputs with manually curated public sources.
- The project does not scrape LinkedIn, bypass login pages, access paid content, or collect
  private personal data.
- Outputs are informational and do not provide employment, legal, immigration, investment,
  automated application, or automated outreach advice.

## Classification

Inputs are normalized into a common `OpportunityItem` schema and classified into:

- `job`
- `event`
- `policy`
- `project`
- `side_hustle`
- `company_signal`
- `learning`

Manual categories are preserved when valid. Missing categories are inferred from record text.

## Scoring

The final score combines five dimensions:

```text
final_score =
  0.30 * relevance_score
+ 0.25 * actionability_score
+ 0.20 * freshness_score
+ 0.15 * credibility_score
+ 0.10 * uniqueness_score
```

- `relevance_score`: match against the selected audience profile, target domains, roles,
  locations, transition keywords, skills, and avoid keywords.
- `actionability_score`: whether the signal has a clear next action such as apply, register,
  build, learn, contact, prepare, submit, or track.
- `freshness_score`: how recent the signal is relative to the report date.
- `credibility_score`: source-type reliability configured in `config/scoring_rules.yaml`.
- `uniqueness_score`: whether the item adds detail, keywords, company context, or source notes.

## Deduplication

Items are deduplicated by normalized title, company/source, and URL. The pipeline keeps the first
best representative so repeated signals do not dominate the weekly report.

## Limitations

- Scores are heuristics, not predictions.
- Sample reports are not live market data.
- Any real data integration should be manually reviewed before decisions are made.
- The dashboard is a local inspection surface, not a production analytics service.
