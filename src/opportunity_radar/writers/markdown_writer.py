from __future__ import annotations

from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

from opportunity_radar.config import get_project_root
from opportunity_radar.models import OpportunityReport


ZH_TEMPLATE = """# 新加坡 AI 与 FinTech 机会雷达 | {{ generated_at[:10] }}

## 执行摘要
{% for line in executive_summary -%}
- {{ line }}
{% endfor %}

## Top Opportunities
| 机会 | 类别 | 公司 / 来源 | 分数 | 为什么重要 | 建议行动 |
|---|---|---|---:|---|---|
{% for item in top_opportunities -%}
| [{{ item.title }}]({{ item.url }}) | {{ item.category }} | {{ item.company or item.source }} | {{ "%.2f"|format(item.final_score) }} | {{ item.fit_reason }} | {{ item.suggested_action }} |
{% endfor %}

## 职位机会
{% for item in jobs -%}
### {{ item.title }}
- 岗位: {{ item.role or item.title }}
- 公司: {{ item.company or "Unknown" }}
- 匹配原因: {{ item.fit_reason }}
- 关键词: {{ item.keywords | join(", ") }}
- 建议行动: {{ item.suggested_action }}

{% endfor -%}

## 政策 / 生态信号
{% for item in policy_signals -%}
### {{ item.title }}
- 事实: {{ item.summary }}
- 为什么重要: {{ item.fit_reason }}
- 职业 / 项目启发: {{ item.suggested_action }}

{% endfor -%}

## 公司信号
{% for item in company_signals -%}
### {{ item.title }}
- 公司 / 来源: {{ item.company or item.source }}
- 信号: {{ item.summary }}
- 为什么重要: {{ item.fit_reason }}
- 建议行动: {{ item.suggested_action }}

{% endfor -%}

## 副业 / 项目想法
{% for item in side_hustles -%}
### {{ item.title }}
- 想法: {{ item.summary }}
- 目标用户: {{ item.target_audience | join(", ") if item.target_audience else profile_name }}
- 为什么现在值得做: {{ item.fit_reason }}
- MVP: {{ item.source_notes or "先做一个小范围、手动优先的原型，并找 3-5 个目标用户验证。" }}
- 下一步: {{ item.suggested_action }}

{% endfor -%}

## 学习重点
{% for item in learning_priorities -%}
- {{ item.title }}: {{ item.summary }} 建议资源类型: {{ item.suggested_action }}
{% endfor %}

## 本周行动计划
{% for action in actions -%}
- {{ action }}
{% endfor %}

## 来源列表
| 标题 | 来源 | 日期 | URL |
|---|---|---|---|
{% for source in source_list -%}
| {{ source.title }} | {{ source.source }} | {{ source.date }} | {{ source.url }} |
{% endfor %}

## 免责声明
本报告是信息型机会情报原型，不提供就业保证、移民建议、法律建议、投资建议，也不提供自动投递服务。
"""


def _context_from_report(report: OpportunityReport) -> dict:
    generated_at = report.generated_at.isoformat(timespec="seconds")
    return {
        "profile_name": report.profile,
        "generated_at": generated_at,
        "executive_summary": report.executive_summary,
        "top_opportunities": report.top_opportunities,
        "jobs": report.jobs,
        "events": report.events,
        "policy_signals": report.policy_signals,
        "side_hustles": report.side_hustles,
        "company_signals": report.company_signals,
        "learning_priorities": report.learning_priorities,
        "actions": report.actions,
        "source_list": report.source_list,
    }


def render_markdown(report: OpportunityReport, language: str = "en") -> str:
    context = _context_from_report(report)
    if language == "zh":
        env = Environment(autoescape=select_autoescape(disabled_extensions=("md",)))
        template = env.from_string(ZH_TEMPLATE)
        return template.render(**context)

    root = get_project_root()
    env = Environment(
        loader=FileSystemLoader(root / "config"),
        autoescape=select_autoescape(disabled_extensions=("md",)),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    template = env.get_template("report_template.md")
    return template.render(**context)


def write_markdown_report(
    report: OpportunityReport, output_path: str | Path, language: str = "en"
) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_markdown(report, language), encoding="utf-8")
    return path
