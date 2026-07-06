# Opportunity Radar：新加坡 AI 与 FinTech 机会情报系统

Opportunity Radar 是一个本地优先的机会情报原型，面向有技术、科研、数据或工程背景，并希望探索新加坡 AI、FinTech、RegTech、风险分析、数据分析和数字化转型机会的人群。

它把人工整理或公共来源风格的机会信号转换成结构化周报，包含相关性评分、可行动性评分、机会分类、建议行动和来源列表。

## 目标用户

- 希望从科研转向 AI / 数据 / FinTech 岗位的中文背景专业人士
- 正在探索新加坡岗位的工程师
- 寻找 FinTech、RegTech 或风险分析机会的数据分析师
- 想寻找商业想法和作品集方向的 AI 应用开发者
- 想看每周机会简报，而不是原始岗位流的人

## 它能做什么

- 导入合成样例或人工整理的 CSV/YAML 机会信号
- 标准化职位、活动、政策信号、公司信号、副业想法和学习重点
- 按 URL 和标题/公司去重
- 按相关性、可行动性、新鲜度、可信度和独特性评分
- 生成英文和中文 Markdown 报告
- 转换为 HTML 报告
- 输出用于看板的 JSON
- 提供简单的 Streamlit 看板

## 它不做什么

- 不做 SaaS、登录、支付或多用户系统
- 不自动投递岗位或提交简历
- 不抓取 LinkedIn、不抓取付费内容、不收集私人数据、不做激进爬虫
- 不提供移民建议、法律建议、投资建议、就业保证或自动外联骚扰

## 架构

```text
config/                 用户画像、来源、评分规则、报告模板
examples/sample_inputs/ 合成 CSV/YAML 示例输入
src/opportunity_radar/  模型、流水线、输出器、CLI、看板
tests/                  Pytest 测试
reports/                生成的 Markdown/HTML/JSON 输出
data/processed/         处理后的报告 JSON
```

## 快速开始

```powershell
cd opportunity-radar
python -m pip install -e .
python -m opportunity_radar.main generate --profile singapore_ai_fintech --mock
```

如果不安装包，可以使用：

```powershell
$env:PYTHONPATH="src"
python -m opportunity_radar.main generate --profile singapore_ai_fintech --mock
```

## CLI 命令

使用内置合成样例生成：

```powershell
python -m opportunity_radar.main generate --profile singapore_ai_fintech --mock
```

从人工输入目录生成：

```powershell
python -m opportunity_radar.main generate --profile singapore_ai_fintech --input-dir examples/sample_inputs
```

生成并刷新稳定样例：

```powershell
python -m opportunity_radar.main generate --profile singapore_ai_fintech --mock --copy-samples
```

输出路径：

```text
data/processed/YYYY-MM-DD_singapore_ai_fintech.json
reports/markdown/YYYY-MM-DD_singapore_ai_fintech_en.md
reports/markdown/YYYY-MM-DD_singapore_ai_fintech_zh.md
reports/html/YYYY-MM-DD_singapore_ai_fintech_en.html
reports/html/YYYY-MM-DD_singapore_ai_fintech_zh.html
```

## 看板

```powershell
streamlit run src/opportunity_radar/dashboard/app.py
```

看板包含用户画像选择、已生成报告选择、机会总数、类别分布、Top Opportunities、职位机会、副业想法、分数分布和 Markdown 报告预览。

## 样例输入

所有样例都是合成数据，位于 `examples/sample_inputs/`：

- `singapore_ai_fintech_jobs.csv`
- `sample_policy_signals.yaml`
- `sample_events.yaml`
- `sample_side_hustle_ideas.yaml`
- `sample_company_signals.yaml`

## 样例报告

稳定样例输出位于：

- `examples/sample_reports/weekly_opportunity_radar_en.md`
- `examples/sample_reports/weekly_opportunity_radar_zh.md`
- `examples/sample_outputs/weekly_opportunity_radar.json`

## 评分公式

```text
final_score =
  0.30 * relevance_score
+ 0.25 * actionability_score
+ 0.20 * freshness_score
+ 0.15 * credibility_score
+ 0.10 * uniqueness_score
```

## 测试

```powershell
pytest
```

## 免责声明

Opportunity Radar 是信息型原型，不提供就业保证、移民建议、法律建议、投资建议或自动投递服务。
