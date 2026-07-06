from __future__ import annotations

from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

from opportunity_radar.config import get_project_root
from opportunity_radar.models import OpportunityItem, OpportunityReport


ZH_TEMPLATE = """# 新加坡 AI 与 FinTech 机会雷达 | {{ generated_at[:10] }}

## 执行摘要

{% for line in executive_summary %}
- {{ line }}
{% endfor %}

## 本周变化

{% for line in what_changed %}
- {{ line }}
{% endfor %}

## 本周重点

- 主要岗位方向：{{ this_week_focus.primary_role_family }}
- 本周最匹配岗位：{{ this_week_focus.best_fit_roles }}
- 最值得构建的作品集产物：{{ this_week_focus.best_portfolio_artifact }}
- 建议 networking 动作：{{ this_week_focus.suggested_networking_action }}

## 重点机会

| 机会 | 类别 | 公司 / 来源 | 分数 | 为什么重要 | 建议行动 |
|---|---|---|---:|---|---|
{% for item in top_opportunities %}
| [{{ item.title }}]({{ item.url }}) | {{ item.category }} | {{ item.company or item.source }} | {{ "%.2f"|format(item.final_score) }} | {{ item.fit_reason }} | {{ item.suggested_action }} |
{% endfor %}

## 本周最匹配岗位方向

- 岗位方向：{{ best_fit_roles.role_family }}
- 为什么匹配：{{ best_fit_roles.why_it_fits }}
- 简历关键词：{{ best_fit_roles.keywords_to_add }}
- 申请切入角度：{{ best_fit_roles.suggested_application_angle }}

## 本周值得关注公司

| 公司 / 来源 | 信号 | 为什么重要 | 建议行动 |
|---|---|---|---|
{% for company in top_companies_to_watch %}
| {{ company.company }} | {{ company.signal }} | {{ company.why_it_matters }} | {{ company.suggested_action }} |
{% endfor %}

## 建议打造的作品集项目

### {{ portfolio_project.title }}

- 目标用户：{{ portfolio_project.target_user }}
- 解决的问题：{{ portfolio_project.problem_solved }}
- MVP 范围：{{ portfolio_project.mvp_scope }}
- 展示技能：{{ portfolio_project.skills_demonstrated }}
- 建议下一步：{{ portfolio_project.suggested_next_step }}

## 岗位机会

{% for item in jobs %}
### {{ item.role or item.title }} | {{ item.company or "Unknown" }}

- 匹配原因：{{ item.fit_reason }}
- 关键词：{{ item.keywords | join(", ") }}
- 评分拆解：
  - 相关性：{{ "%.2f"|format(item.relevance_score) }}
  - 行动价值：{{ "%.2f"|format(item.actionability_score) }}
  - 新鲜度：{{ "%.2f"|format(item.freshness_score) }}
  - 可信度：{{ "%.2f"|format(item.credibility_score) }}
  - 独特性：{{ "%.2f"|format(item.uniqueness_score) }}
- 适合人群：{{ target_user_fit_zh(item) }}
- 建议行动：{{ item.suggested_action }}

{% endfor %}

## 政策 / 生态信号

{% for item in policy_signals %}
### {{ item.title }}

- 事实：{{ item.summary }}
- 为什么重要：{{ item.fit_reason }}
- 职业 / 项目启发：{{ item.suggested_action }}

{% endfor %}

## 公司信号

{% for item in company_signals %}
### {{ item.company or item.source }} / {{ item.title }}

- 信号：{{ item.summary }}
- 为什么重要：{{ item.fit_reason }}
- 建议行动：{{ item.suggested_action }}

{% endfor %}

## 副业 / 项目想法

{% for item in side_hustles %}
### {{ item.title }}

- 目标用户：{{ item.target_audience | join(", ") if item.target_audience else target_user_fit_zh(item) }}
- 为什么现在值得做：{{ item.fit_reason }}
- MVP：{{ item.source_notes or "先做一个小范围、手动优先的原型，并找 5-10 个目标用户验证。" }}
- 下一步：{{ item.suggested_action }}

{% endfor %}

## 学习优先级

{% for item in learning_priorities %}
- 技能：{{ item.title }}
  为什么重要：{{ item.summary }}
  建议资源类型：{{ item.suggested_action }}
{% endfor %}

## 本周行动计划

{% for action in actions %}
- {{ action }}
{% endfor %}

## 来源列表

| 标题 | 来源 | 日期 | URL |
|---|---|---|---|
{% for source in source_list %}
| {{ source.title }} | {{ source.source }} | {{ source.date }} | {{ source.url }} |
{% endfor %}

## 免责声明

本报告是信息型机会情报原型，不提供就业保证、移民建议、法律建议、投资建议，也不提供自动投递服务。
"""


def target_user_fit(item: OpportunityItem) -> str:
    if item.target_audience:
        return ", ".join(item.target_audience)
    if item.required_skills:
        skills = ", ".join(item.required_skills[:4])
        return f"candidates with {skills} experience"
    if item.role:
        return f"{item.role} candidates tracking Singapore AI and FinTech opportunities"
    if item.category == "side_hustle":
        return "AI builders and analysts validating small opportunity-intelligence services"
    if item.category == "learning":
        return "career transitioners building visible AI, analytics, or reporting evidence"
    return "research-to-AI transitioners, data analysts, and FinTech risk candidates"


def target_user_fit_zh(item: OpportunityItem) -> str:
    if item.target_audience:
        return "、".join(item.target_audience)
    if item.required_skills:
        skills = "、".join(item.required_skills[:4])
        return f"具备 {skills} 经验的候选人"
    if item.role:
        return f"正在关注新加坡 AI 与 FinTech 机会的 {item.role} 候选人"
    if item.category == "side_hustle":
        return "正在验证小型机会情报服务的 AI builder 和分析师"
    if item.category == "learning":
        return "希望积累 AI、分析或报告自动化作品集证据的转型者"
    return "科研转 AI 人群、数据分析师和 FinTech 风险方向候选人"


def _context_from_report(report: OpportunityReport) -> dict:
    generated_at = report.generated_at.isoformat(timespec="seconds")
    return {
        "profile_name": report.profile,
        "generated_at": generated_at,
        "executive_summary": report.executive_summary,
        "what_changed": report.what_changed,
        "this_week_focus": report.this_week_focus,
        "best_fit_roles": report.best_fit_roles,
        "top_companies_to_watch": report.top_companies_to_watch,
        "portfolio_project": report.portfolio_project,
        "top_opportunities": report.top_opportunities,
        "jobs": report.jobs,
        "events": report.events,
        "policy_signals": report.policy_signals,
        "side_hustles": report.side_hustles,
        "company_signals": report.company_signals,
        "learning_priorities": report.learning_priorities,
        "actions": report.actions,
        "source_list": report.source_list,
        "target_user_fit": target_user_fit,
        "target_user_fit_zh": target_user_fit_zh,
    }


def render_markdown(report: OpportunityReport, language: str = "en") -> str:
    context = _context_from_report(report)
    if language == "zh":
        env = Environment(autoescape=False, trim_blocks=True, lstrip_blocks=True)
        template = env.from_string(ZH_TEMPLATE)
        return template.render(**context).strip() + "\n"

    root = get_project_root()
    env = Environment(
        loader=FileSystemLoader(root / "config"),
        autoescape=select_autoescape(disabled_extensions=("md",)),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    template = env.get_template("report_template.md")
    return template.render(**context).strip() + "\n"


def write_markdown_report(
    report: OpportunityReport, output_path: str | Path, language: str = "en"
) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_markdown(report, language), encoding="utf-8")
    return path
