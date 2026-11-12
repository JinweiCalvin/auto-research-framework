# Auto Research Framework

面向科研课题的本地工作流框架：用 Idea2Paper 产生候选研究故事，用 ARIS 完成按需文献检索、问题收敛、实验设计、结果审计与论文写作。框架把人工决策和证据核查放在研究阶段之间，帮助研究者留下可复现记录。

## 快速部署

需求：macOS 或 Linux、Git、Python 3.10+、Codex CLI。网络需要能访问 GitHub；完整 Idea2Paper pipeline 还需要用户自行配置兼容的对话和 embedding API。

```bash
git clone https://github.com/JinweiCalvin/auto-research-framework.git
cd auto-research-framework
bash setup.sh
```

`setup.sh` 会下载固定版本的 Idea2Paper 与 ARIS、应用本机工作台适配层、生成不含密钥的 `.env` 配置文件，并安装一组精选的文献/选题/实验/写作 ARIS Skills，加上本仓库的 `/anti-defensive-writing`。它不会建立 embedding 索引、运行模型、启动 GPU 作业或创建云资源。

按部署指南在 `idea2paper/.venv` 安装 Python 依赖并设置好 `idea2paper/.env` 后，双击 macOS 的 `start-dashboard.command`，或运行：

```bash
python3 tools/create_research_project.py research-projects/<project-name>
```

然后按 [完整工作流手册](docs/WORKFLOW_CN.md) 开始。首次构建 Idea2Paper 向量索引会调用 embedding API 并产生费用；先阅读 [部署与安全指南](docs/DEPLOYMENT_CN.md)。

## 默认研究路径

研究问题与约束 → 候选故事 → 文献与数据核查 → 人工确认研究主张 → 实验计划与预算关口 → sanity check → 正式实验 → 结果/引用审计 → 论文和 PDF。

当前阶段只启用需要的工具。GPU、自动多轮审稿、研究 Wiki、额外检索源和视觉写作增强都是可选项。

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
