# Auto Research Framework

面向科研课题的本地工作流框架：用 Idea2Paper 产生候选研究故事，用 ARIS 完成按需文献检索、问题收敛、实验设计、结果审计与论文写作。框架把人工决策和证据核查放在研究阶段之间，帮助研究者留下可复现记录。

## 快速部署

需求：macOS 或 Linux、Git、Python 3.10+、Codex CLI。网络需要能访问 GitHub；完整 Idea2Paper pipeline 还需要用户自行配置兼容的对话和 embedding API。

```bash
git clone https://github.com/JinweiCalvin/auto-research-framework.git
cd auto-research-framework
bash setup.sh
```

`setup.sh` 会下载固定版本的 Idea2Paper 与 ARIS、应用本机工作台适配层、生成不含密钥的 `.env` 配置文件，并把项目维护者已启用的 60 个 ARIS Skills 安装到项目级 Skills 目录。仓库还自带 `/anti-defensive-writing` 和 5 个 Nature 工作流 Skills，Codex 从项目目录打开后即可识别。安装不会建立 embedding 索引、运行模型、启动 GPU 作业或创建云资源。

按部署指南在 `idea2paper/.venv` 安装 Python 依赖并设置好 `idea2paper/.env` 后，双击 macOS 的 `start-dashboard.command`，或运行：

```bash
python3 tools/create_research_project.py research-projects/<project-name>
```

然后按 [完整工作流手册](docs/WORKFLOW_CN.md) 开始。首次构建 Idea2Paper 向量索引会调用 embedding API 并产生费用；先阅读 [部署与安全指南](docs/DEPLOYMENT_CN.md)。

## 默认研究路径

研究问题与约束 → 候选故事 → 文献与数据核查 → 人工确认研究主张 → 实验计划与预算关口 → sanity check → 正式实验 → 结果/引用审计 → 论文和 PDF。

当前阶段只启用需要的工具。GPU、自动多轮审稿、研究 Wiki、额外检索源和视觉写作增强都是可选项。

## Codex 使用教程

### 怎样开始一个课题

先创建项目目录，再把真实目标、现有材料和限制告诉 Codex。尽量提供文件路径，不要只说“帮我做研究”。

```text
请先阅读这个项目的 RESEARCH_BRIEF.md 和我提供的材料。
研究目标是：[一句话说明目标]。
现有数据/资源是：[数据、问卷、代码、GPU 或 API]。
限制是：[截止日期、预算、目标期刊或不能做的事项]。
先盘点证据和缺口，更新项目状态与下一步清单；不要编造数据、文献或结果，也不要在我确认研究方案前启动长时间实验。
```

### 怎样进行多轮对话

把一个研究阶段作为一轮工作，每轮结束时要求 Codex 更新 `STAGE_STATUS.md`、保存产物路径、列出待确认事项和下一步。接续时直接说“继续”，或指出具体阶段/文件；Codex 应从项目记录续做，不必重复背景。

建议顺序：问题与可行性 → 文献和数据核验 → 研究主张与方案确认 → 实验计划 → 小规模 sanity check → 正式实验 → 结果和引用审计 → 写作与独立审稿。每轮可以这样要求：

```text
继续这个课题。先查看 STAGE_STATUS.md 和最近的实验/决策记录，告诉我当前阶段与未解决事项，然后完成一个可以闭环的下一步。把结果写入对应文件，更新状态，并说明哪些结论有证据、哪些仍待确认。
```

### 怎样调度 Skills

可在消息中直接写 Skill 名称，要求 Codex 读取并按其流程执行。完整 ARIS 已启用清单见 [`config/aris-skills.txt`](config/aris-skills.txt)；按工作目标选择，不必每轮把所有 Skill 都跑一遍：

| 目标 | 推荐调用 |
|---|---|
| 研究问题与文献 | `/idea-discovery`、`/research-lit`、`/novelty-check` |
| 方案与实验 | `/experiment-plan`、`/qinyan-nature-statistics` |
| 图表 | `/qinyan-nature-figures`，要求图可追溯到结果数据和生成代码 |
| 论文结构与起草 | `/paper-plan`、`/qinyan-nature-writing`、`/paper-writing` |
| 语言精修 | `/qinyan-nature-polishing`，再用 `/anti-defensive-writing` 检查防御性表达 |
| 独立审查 | `/qinyan-nature-review`、`/citation-audit`、`/paper-claim-audit` |
| PDF 与交付 | `/paper-compile`，并要求逐页检查图表、引用和交叉引用 |

### 提示词示例

**先审方案，不急着写稿：**

```text
请用 /research-review 和 /qinyan-nature-statistics 审查当前研究方案。先列出会影响结论的设计问题、需要的证据和可执行修改；区分“必须解决”和“可选增强”。不要替我假设数据已经支持研究假设。
```

**结果出来后再写：**

```text
只根据 experiments/ 中已完成且可复现的结果，用 /result-to-claim 建立主张-证据表，再用 /qinyan-nature-writing 重构 Results 和 Discussion。每个数字回链到结果文件；没有证据的内容标记为待确认，不得补造。
```

**多轮修改论文：**

```text
第 1 轮：用 /qinyan-nature-review 给 paper/main.tex 做独立审查，按严重度排序问题，不要直接重写全文。
第 2 轮：我确认修改范围后，逐条处理重大问题，保留修改记录，并用 /anti-defensive-writing 检查行文。
第 3 轮：用 /qinyan-nature-polishing 优化表达，用 /citation-audit 和 /paper-claim-audit 核对文献及数字，再编译 PDF 检查版面。
```

“Nature” Skills 提供结构、统计、表达、图表与审稿标准，不代表稿件达到特定期刊录用门槛。结论强度始终由研究设计和数据证据决定。

## 版本与边界

- Idea2Paper upstream: `AgentAlphaAGI/Idea2Paper`, pinned at `64170d4d9ca9068b26bd561648ce5c576bf1a2fb`.
- ARIS upstream: `wanshuiyin/Auto-claude-code-research-in-sleep`, pinned at `ed593c72011936adaef2d6e6cc57f98ce80f8b4e`.
- 本仓库提供工作流、模板、脚手架和集成说明；两项上游工具保留各自仓库与许可证。
- Idea2Paper 的评分是筛选信号。研究新颖性、方法贡献和论文结论必须由来源文献与真实实验核实。
- 工作流不会替代研究者的伦理、数据许可和学术判断。

## 文档

- [完整工作流手册](docs/WORKFLOW_CN.md)
- [部署与安全指南](docs/DEPLOYMENT_CN.md)
- [慢病管理案例如何映射到通用流程](docs/CASE_STUDY_CHRONIC_DISEASE_CN.md)
- [新课题模板说明](docs/PROJECT_TEMPLATE_CN.md)

## License

本仓库自有文档、模板和脚手架采用 MIT License。Idea2Paper 与 ARIS 是独立上游项目，分别遵循其仓库许可证。
