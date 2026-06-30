# ResumeTailor

根据职位描述（JD）自动生成定制化中英文 LaTeX 简历的本地工具。输入一份 JD 和一份个人经历知识库，输出针对该岗位优化过的简历草稿，最终在 LaTeX 中精修排版、导出 PDF。

> **关于本仓库的数据**：`templates/`、`jobs/`、`knowledge_base/working experience/`、`knowledge_base/academic experience and projects/` 存放的是真实简历数据，已在 `.gitignore` 中排除，不会出现在这个公开仓库里。`examples/` 目录提供了一套结构相同、内容虚构的示范数据，展示各文件应该怎么写。克隆本仓库后，按相同格式在对应路径放入你自己的信息即可，详见下方「快速开始」。

---

## 功能

- **JD 解析**：调用 LLM 提取职位的核心职责、硬性要求、加分项，结构化输出。
- **匹配度分析**：对比 JD 与个人知识库，给出匹配分数、强匹配项、待补强项和优化建议。
- **简历定制生成**：基于 JD 分析结果和知识库，从全部经历中精选、重组出针对该岗位的中文 LaTeX 简历（不编造经历，只做筛选和措辞优化）。
- **中英文同步翻译**：将定制后的中文简历翻译为英文，保持 LaTeX 结构不变。
- **PDF 编译**：调用 xelatex 一键编译中英文简历。
- **多 LLM 支持**：通过 `config.yaml` 切换 Gemini / OpenAI，两者接口统一抽象，便于扩展其他模型。
- **按岗位归档**：每个目标岗位有独立目录（JD + 定制简历），可随时回顾、对比、复用。

---

## 项目架构

项目由两套互补的工作流组成：一套自动化 LLM 流水线负责"从知识库快速生成草稿"，一套手工 LaTeX 工作流负责"精修排版、按岗位归档"。

### 1. 自动化生成流水线（`main.py`）

```
data/jd/your_job.txt
        │
        ▼
┌───────────────────┐
│ 1. jd_loader       │  读取 JD（txt / pdf / docx）
├───────────────────┤
│ 2. jd_analyzer     │  LLM 分析 JD → outputs/jd_analysis.md
├───────────────────┤
│ 3. knowledge_base   │  加载 knowledge_base/ 下全部 .md 文件
├───────────────────┤
│ 4. resume_optimizer │  生成匹配度报告 → outputs/match_report.md
│    (match report)   │
├───────────────────┤
│ 5. resume_optimizer │  生成定制中文简历 → outputs/resume_cn.tex
│    (optimize)       │
├───────────────────┤
│ 6. translator       │  翻译为英文 → outputs/resume_en.tex
├───────────────────┤
│ (可选) latex_exporter│  xelatex 编译 → outputs/pdf/
└───────────────────┘
```

核心模块（`src/`）：

| 模块 | 职责 |
| --- | --- |
| `jd_loader.py` | 解析 `.txt` / `.pdf` / `.docx` 格式的 JD 文件 |
| `jd_analyzer.py` | 调用 LLM 提炼 JD 的职责、要求、加分项 |
| `knowledge_base.py` | 递归加载 `knowledge_base/` 下所有 `.md` 文件并拼接进 prompt |
| `resume_optimizer.py` | 生成匹配度报告；基于 JD + 知识库生成定制简历 |
| `translator.py` | 中文简历 → 英文简历，保持 LaTeX 结构 |
| `resume_diff.py` | 对比生成结果与主简历模板的差异，终端高亮展示 |
| `latex_exporter.py` | 调用 `xelatex` 把 `.tex` 编译为 PDF |
| `llm_factory.py` + `providers/` | 按 `config.yaml` 配置返回对应的 LLM Provider（Gemini / OpenAI），统一 `BaseLLM` 接口 |

`config.py` 集中管理所有路径常量和 API Key 读取（从 `.env` 加载）。

所有调用 LLM 用到的 prompt 都外置在 `prompts/` 目录下（按 `<场景>.system.md` / `<场景>.user.md` 命名），通过 `src/utils.py` 的 `load_prompt()` 读取，不写死在代码里，方便非工程同学直接改 prompt、做版本管理。其中简历生成的 prompt（`prompts/optimize.*.md`）遵循 `docs/PRD_003.md` 定义的简历编写规范（先定位 Positioning，再组织 Career Narrative，每段经历按 Background → Responsibility → Contribution → Result 展开，每条 Bullet 只证明一个能力）。

### 2. 按岗位归档的手工 LaTeX 工作流（`templates/` + `jobs/` + `Makefile`）

自动生成的草稿通常还需要手工精修排版，因此项目额外提供了一套基于 `Makefile` 的归档工作流：

```
templates/resume_cn.tex / resume_en.tex   ← 包含全部经历的基础模板
        │  make new JOB=<name>
        ▼
jobs/<name>/
  ├── jd.txt           ← 该岗位的 JD
  ├── resume_cn.tex    ← 从模板复制，手工/借助上面的流水线精简定制
  └── resume_en.tex
        │  make compile JOB=<name> LANG=cn|en
        ▼
jobs/<name>/resume_*.pdf
```

`templates/photo.jpg` 作为统一证件照资源被所有岗位目录共享（`\graphicspath` 已在模板中配置好）。`outputs/` 目录保留给流水线（1）使用，两套工作流互不干扰。

---

## 环境准备

```bash
conda create -n JDCV python=3.11
conda activate JDCV
pip install -r requirements.txt
```

编译 PDF 需要 LaTeX 环境（macOS）：

```bash
brew install --cask mactex-no-gui
```

---

## 快速开始

### 1. 配置 API Key

复制 `.env` 模板并填入你的 key：

```
GEMINI_API_KEY=你的key        # 默认使用，免费额度大，https://aistudio.google.com/apikey 获取
OPENAI_API_KEY=你的key        # 可选，切换到 GPT 时填写
```

### 2.（可选）选择模型

编辑 `config.yaml`，默认使用 Gemini：

```yaml
llm:
  provider: google          # google | openai
  model: gemini-2.5-flash   # gemini-2.5-pro | gpt-5 | gpt-5-mini
  temperature: 0.3
  max_tokens: 4000
```

### 3. 填写你的知识库

知识库是简历的原材料，越详细生成效果越好。每段经历/每个项目对应一个 `.md` 文件，放入 `knowledge_base/`（无固定子目录要求，递归扫描全部 `.md`）：

```
knowledge_base/
├── working experience/                    # 每段实习/工作经历一个文件
├── academic experience and projects/      # 每个项目一个文件
└── terminology/                           # 行业术语库（可选，提升 LLM 理解准确度）
```

格式参考 `examples/knowledge_base/` 下的示例文件。

### 4. 填写主简历模板

把你的真实信息（姓名、学校、联系方式、全部经历）填入 `templates/resume_cn.tex` 和 `templates/resume_en.tex`，证件照放在 `templates/photo.jpg`。格式参考 `examples/templates/`。

### 5. 跑通一个岗位

```bash
# 把目标岗位 JD 放进 data/jd/（支持 .txt / .pdf / .docx）
cp your_job_description.txt data/jd/

# 运行自动化流水线：分析 JD → 匹配度报告 → 生成中英文简历草稿
python main.py
```

生成的草稿在 `outputs/resume_cn.tex` / `outputs/resume_en.tex`，结合 `outputs/match_report.md` 的建议手工精修后，建档为一个岗位：

```bash
make new JOB=target_job          # 在 jobs/target_job/ 下新建归档目录
# 把 outputs/resume_*.tex 的内容整理进 jobs/target_job/resume_*.tex
make all JOB=target_job          # 编译中英文 PDF
```

也可以跳过自动化流水线，直接从模板手工定制：

```bash
make new JOB=target_job
# 手动编辑 jobs/target_job/resume_cn.tex / resume_en.tex
make compile JOB=target_job LANG=cn
```

---

## Makefile 命令

| 操作 | 命令 |
| --- | --- |
| 新建岗位归档 | `make new JOB=risk_control` |
| 编译指定语言 | `make compile JOB=ai_pm LANG=cn` |
| 编译中英文 | `make all JOB=ai_pm` |
| 清理编译产物 | `make clean JOB=ai_pm` |
| 查看所有岗位 | `make list` |

---

## 项目结构

```text
.
├── main.py                    # 自动化流水线入口
├── config.py / config.yaml    # 路径常量、API Key、LLM 配置
├── src/                       # 流水线核心模块（见上方架构图）
│   └── providers/             # LLM Provider 抽象（Gemini / OpenAI）
├── prompts/                   # 外置的 LLM prompt 模板（<场景>.system.md / .user.md）
├── data/jd/                   # 待处理的 JD 原始文件
├── knowledge_base/            # 个人经历知识库（.md），递归加载
├── templates/                 # 简历基础模板 + 共享证件照
├── jobs/<name>/                # 按岗位归档：jd.txt + 定制简历 + 编译产物
├── outputs/                    # 自动化流水线产物（JD 分析 / 匹配报告 / 简历草稿 / PDF）
├── examples/                   # 虚构示范数据，结构与上面完全一致，供参考
├── docs/                       # PRD / 简历编写规范文档
├── Makefile                    # 岗位归档 + 编译命令
└── requirements.txt
```
