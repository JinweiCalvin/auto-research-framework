# 部署与安全指南

## 运行要求

- macOS 13+ 或常见 Linux 发行版；Python 3.10+、Git、Codex CLI。
- 可访问 GitHub。Idea2Paper 对话和 embedding API 由使用者自行申请并配置。
- CPU 可完成讨论、文献工作和小规模分析。只有实验需求明确后才配置 GPU；任何云端算力均由使用者自行选择并设置账单上限。

## 部署步骤

```bash
git clone https://github.com/JinweiCalvin/auto-research-framework.git
cd auto-research-framework
bash setup.sh
```

安装脚本固定拉取 README 中列出的两个上游 commit，避免默认追踪变化中的主分支。Idea2Paper 上游包含公开论文/知识图谱资产，首次检出约需数百 MB；向量索引仍由用户在需要时本机生成。脚本创建 `idea2paper/.env` 的本机副本，并为 Codex 安装精选的常用 ARIS Skills。安装失败时，先检查 Git、网络与 Codex CLI，再按 ARIS 官方文档单独安装。

## 配置 Idea2Paper

1. 打开 `idea2paper/.env`，填入所选兼容服务的 LLM 和 Embedding API 地址、模型名、密钥。
2. 确认该服务支持代码所需协议和 JSON 输出；先做小样本请求。
3. 首次建立文献向量索引时会消耗 embedding 用量并在本地产生索引文件。索引与模型、维度相匹配；更换 embedding 模型时重建索引。
4. 本地工作台仅绑定 `127.0.0.1`。不要用 `0.0.0.0` 将其直接暴露到校园网或公网。

Idea2Paper 的 pipeline 依赖位于 `idea2paper/Paper-KG-Pipeline/requirements.txt`。它包括 PyTorch 周边和聚类组件，安装可能下载较大的依赖。建议先创建独立虚拟环境，再安装：

```bash
cd idea2paper
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r Paper-KG-Pipeline/requirements.txt
```

Windows 用户请在 PowerShell 激活 `.venv\Scripts\Activate.ps1`。前端有已构建静态文件，普通运行不需要 Node.js。开发前端时才需要 Node.js 与 `npm ci`。

## 新建课题

```bash
python3 tools/create_research_project.py research-projects/<project-name>
```

新目录已存在时，脚本会拒绝覆盖。先完成 `RESEARCH_BRIEF.md`，再保存候选故事、计划、实验结果和稿件。

## GPU / SSH / 云服务

GPU 不是启动工作流的前提。需要时填写 `AGENTS.md` 中的服务器规格、SSH alias、环境、远程项目目录、存储、时限和费用上限；先只读探测 `nvidia-smi`、CUDA/PyTorch、磁盘和权限，再传代码/数据。可识别健康数据、受限调查数据和未发表的敏感材料不应传到未经批准的服务。

租卡、启动云任务或上传私有数据前，明确确认实例类型、小时价格/最高预算、区域、最长运行时间、关机条件和数据删除策略。任务结束后验证结果回传再释放实例。

## 安全与版本管理

- 密钥只放在被 `.gitignore` 忽略的 `.env` 或系统密钥管理器中。只提交 `.env.example`。
- 曾经发到聊天、Issue 或提交记录的 API Key 都应视为泄露并轮换；删除消息或后来删除文件不能使旧密钥恢复安全。
- 原始数据、个人身份信息、问卷许可文件、受限代码本、运行日志、API 请求/响应、缓存和本机索引都先按敏感材料处理。
- 公共仓库只放框架、可公开模板和许可允许的示例。研究项目独立存放；公开复现材料须再次核对数据许可和隐私。
- 分享 Idea2Paper run 前检查 prompt、模型响应、路径、日志和配置是否包含 key 或数据片段。
- 上游依赖各自保留许可证；升级 pin 后做 smoke test，记录 commit 与升级日期。

## 常见问题

**Skills 没显示？** 重启 Codex 项目窗口，确认 `.agents/skills` 链接和 `.aris/installed-skills-codex.txt` 清单；按 ARIS 官方指南重新安装。

**dashboard 启动但 API 不通？** 保持终端窗口运行；检查 `idea2paper/.env`、Python 环境、端口和日志。服务只应对本机开放。

**第一次运行耗时或费用高？** 先检查是否需要建立 embedding 索引。用少量公开论文样本测试后再跑完整索引。

**没有 API Key 或 GPU？** 仍可完成研究问题讨论、文献计划、手工证据审计、实验设计和轻量 CPU 分析；跳过依赖相应资源的阶段并标注状态。
