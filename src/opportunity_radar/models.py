from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class OpportunityItem(BaseModel):
    id: str
    title: str
    url: str
    source: str
    source_type: str
    published_at: datetime
    category: str
    location: str
    company: str | None = None
    role: str | None = None
    summary: str
    keywords: list[str] = Field(default_factory=list)
    target_audience: list[str] = Field(default_factory=list)
    required_skills: list[str] = Field(default_factory=list)
    nice_to_have_skills: list[str] = Field(default_factory=list)
    seniority: str | None = None
    remote_option: str | None = None
    actionability_score: float = 0.0
    relevance_score: float = 0.0
    freshness_score: float = 0.0
    credibility_score: float = 0.0
    uniqueness_score: float = 0.0
    final_score: float = 0.0
    fit_reason: str = ""
    suggested_action: str = ""
    source_notes: str = ""


class AudienceProfile(BaseModel):
    id: str
    name: str
    description: str
    target_locations: list[str] = Field(default_factory=list)
    target_domains: list[str] = Field(default_factory=list)
    target_roles: list[str] = Field(default_factory=list)
    core_skills: list[str] = Field(default_factory=list)
    transition_keywords: list[str] = Field(default_factory=list)
    avoid_keywords: list[str] = Field(default_factory=list)


class OpportunityReport(BaseModel):
    id: str
    profile: str
    generated_at: datetime
    title: str
    executive_summary: list[str] = Field(default_factory=list)
    this_week_focus: dict[str, str] = Field(default_factory=dict)
    top_opportunities: list[OpportunityItem] = Field(default_factory=list)
    jobs: list[OpportunityItem] = Field(default_factory=list)
    events: list[OpportunityItem] = Field(default_factory=list)
    policy_signals: list[OpportunityItem] = Field(default_factory=list)
    side_hustles: list[OpportunityItem] = Field(default_factory=list)
    company_signals: list[OpportunityItem] = Field(default_factory=list)
    learning_priorities: list[OpportunityItem] = Field(default_factory=list)
    actions: list[str] = Field(default_factory=list)
    source_list: list[dict[str, Any]] = Field(default_factory=list)
