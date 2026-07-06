FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml README.md ./
COPY config ./config
COPY examples ./examples
COPY src ./src

RUN pip install --no-cache-dir -e .

CMD ["python", "-m", "opportunity_radar.main", "generate", "--profile", "singapore_ai_fintech", "--mock"]
