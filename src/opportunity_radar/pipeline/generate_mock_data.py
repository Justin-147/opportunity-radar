from __future__ import annotations

from datetime import datetime

from opportunity_radar.models import AudienceProfile, OpportunityItem


def generate_learning_items(
    profile: AudienceProfile, generated_at: datetime | None = None
) -> list[OpportunityItem]:
    published_at = generated_at or datetime.utcnow()
    learning_specs = [
        (
            "AI governance control testing",
            "Practice mapping AI assistant risks to controls, test evidence, and monitoring metrics.",
            "Complete one regulator-style checklist and attach it to a portfolio case study.",
            ["AI governance", "controls", "model monitoring"],
        ),
        (
            "Payments risk analytics with Python and SQL",
            "Build the core analytics skill set behind fraud, merchant risk, and transaction monitoring roles.",
            "Use a tutorial or synthetic dataset and publish one dashboard screenshot.",
            ["payments risk", "Python", "SQL", "dashboarding"],
        ),
        (
            "Product analytics for tokenisation workflows",
            "Understand user journeys, metrics, and risk questions in tokenised asset product experiments.",
            "Read one product analytics guide and draft a metric tree for a tokenisation MVP.",
            ["tokenisation", "product analytics", "digital assets"],
        ),
        (
            "Streamlit dashboarding for opportunity intelligence",
            "Convert structured signals into a browsable dashboard that demonstrates analyst workflow thinking.",
            "Add filters, score tables, and Markdown previews to a local Streamlit app.",
            ["Streamlit", "dashboarding", "reporting"],
        ),
        (
            "Report automation with Jinja2 and Markdown",
            "Show that fragmented research inputs can become repeatable weekly intelligence reports.",
            "Create one reusable report template and generate English and Chinese outputs.",
            ["Jinja2", "Markdown", "report automation"],
        ),
    ]

    items: list[OpportunityItem] = []
    for index, (title, summary, action, keywords) in enumerate(learning_specs, start=1):
        items.append(
            OpportunityItem(
                id=f"learning-{index}",
                title=title,
                url=f"https://example.org/opportunity-radar/learning/{index}",
                source="Generated Learning Priorities",
                source_type="manual",
                published_at=published_at,
                category="learning",
                location="Remote",
                company=None,
                role=None,
                summary=summary,
                keywords=keywords,
                target_audience=[profile.name],
                required_skills=keywords,
                suggested_action=action,
                source_notes="Generated from the target audience profile and top opportunity themes.",
            )
        )
    return items
