# Local demo script for Opportunity Radar.
# Run from the repository root in an activated Python environment.

pytest

python -m opportunity_radar.main generate --profile singapore_ai_fintech --mock

# To start the dashboard manually, run:
# streamlit run src/opportunity_radar/dashboard/app.py
