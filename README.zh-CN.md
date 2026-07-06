# Opportunity Radar：新加坡 AI 与 FinTech 机会情报系统

![tests](https://github.com/Justin-147/opportunity-radar/actions/workflows/tests.yml/badge.svg)

Opportunity Radar 是一个 local-first 的机会情报系统，面向具有技术、科研、数据或工程背景，并希望探索新加坡 AI、FinTech、RegTech、风险分析、数据分析和数字化转型机会的人群。

它将人工整理或公开来源风格的岗位、政策、公司、活动、学习方向和副业机会信号转化为结构化周报，并提供相关性评分、行动价值评分、建议动作和来源列表。

该项目既是一个可展示的作品集原型，也可以作为未来 newsletter、咨询服务或机会情报产品的基础。

Opportunity Radar 不提供求职保证、移民建议、法律建议、投资建议、自动投递服务或自动外联服务。

## 目标用户

Opportunity Radar 面向：

- 希望转向 AI / 数据 / FinTech 岗位的科研人员；
- 正在探索新加坡机会的工程师；
- 寻找 FinTech 或 RegTech 岗位的数据分析师；
- 正在寻找商业想法的 AI 应用开发者；
- 希望阅读每周机会简报，而不是原始岗位流的专业人士。

## 它能做什么

- 导入人工整理的岗位、政策、活动、公司、学习和副业机会信号；
- 将信号标准化为统一的 `OpportunityItem` 数据结构；
- 对相似机会进行去重；
- 按类别进行分类；
- 计算相关性、行动价值、新鲜度、可信度和独特性评分；
- 对机会进行排序；
- 生成英文和中文每周报告；
- 提供简单的 Streamlit 看板。

## 它不做什么

- 不抓取 LinkedIn；
- 不绕过登录页面；
- 不自动投递岗位；
- 不提供移民或法律建议；
- 不提供投资建议；
- 不保证求职结果；
- 不收集私人个人数据。

## 架构

Opportunity Radar 使用确定性的本地流水线：

```text
人工 CSV/YAML 输入
  -> 导入和标准化
  -> 去重和分类
  -> 评分和排序
  -> 构建报告上下文
  -> 输出 Markdown、HTML 和 JSON
  -> 在 Streamlit 中查看
```

## 快速开始

```powershell
cd opportunity-radar
python -m pip install -e .[dev]
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

预期输出：

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

看板包含报告选择器、机会总数、类别分布、分数分布、Top Opportunities、职位机会、副业想法和 Markdown 报告预览。

## 截图

后续可以补充截图，用于展示：

- Opportunity Dashboard；
- 生成的每周机会简报；
- 分类和评分分布。

## 样例输入

样例输入是合成数据，聚焦新加坡 AI / FinTech / RegTech 场景，并且适合公开发布：

- `examples/sample_inputs/singapore_ai_fintech_jobs.csv`
- `examples/sample_inputs/sample_policy_signals.yaml`
- `examples/sample_inputs/sample_events.yaml`
- `examples/sample_inputs/sample_side_hustle_ideas.yaml`
- `examples/sample_inputs/sample_company_signals.yaml`

## 样例报告

- [英文每周样例报告](examples/sample_reports/weekly_opportunity_radar_en.md)
- [中文每周样例报告](examples/sample_reports/weekly_opportunity_radar_zh.md)
- [样例 JSON 输出](examples/sample_outputs/weekly_opportunity_radar.json)

## 评分公式

```text
final_score =
  0.30 * relevance_score
+ 0.25 * actionability_score
+ 0.20 * freshness_score
+ 0.15 * credibility_score
+ 0.10 * uniqueness_score
```

- `relevance_score`：机会与所选用户画像的匹配程度。
- `actionability_score`：该机会是否指向清晰的下一步，例如申请、报名、构建、学习或联系。
- `freshness_score`：机会信号的新近程度。
- `credibility_score`：来源类型的可信度。
- `uniqueness_score`：该机会是否提供了区别于重复信号的独特价值。

## 仓库结构

```text
config/                 用户画像、来源、评分规则和报告模板
docs/screenshots/       后续截图占位目录
examples/sample_inputs/ 合成 CSV/YAML 示例输入
examples/sample_reports 精选稳定 Markdown 样例报告
examples/sample_outputs 精选稳定 JSON 样例输出
src/opportunity_radar/  模型、流水线、输出器、CLI 和看板
tests/                  Pytest 测试
reports/                生成的 Markdown/HTML/JSON 输出，Git 忽略
data/processed/         生成的处理后 JSON，Git 忽略
```

## 仓库卫生

生成报告和处理后数据会被 Git 忽略：

- `reports/`
- `data/processed/`
- `data/cache/`

精选样例保存在：

- `examples/sample_inputs/`
- `examples/sample_reports/`
- `examples/sample_outputs/`

## 测试

```powershell
pytest
```

## 本地验证

提交前请运行：

```powershell
pytest
python -m opportunity_radar.main generate --profile singapore_ai_fintech --mock
```

## 免责声明

Opportunity Radar 是信息型机会情报原型，不提供求职保证、移民建议、法律建议、投资建议、自动投递服务或自动外联服务。
