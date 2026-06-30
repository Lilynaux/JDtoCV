# ResumeTailor

根据 JD 自动生成定制化中英文 LaTeX 简历。

> **关于本仓库**：`templates/`、`jobs/`、`knowledge_base/working experience/`、`knowledge_base/academic experience and projects/` 以及 `templates/photo.jpg` 存放的是使用者本人的真实简历数据，已在 `.gitignore` 中排除，不会被提交到 GitHub。
> `examples/` 目录提供了一套结构相同、内容完全虚构的示范数据（虚构人物"张三"），用来说明各文件应该怎么填写；克隆本仓库后，把你自己的真实信息按相同格式放入对应的真实路径即可。

---

## 环境准备

```bash
conda activate JDCV
```

> 环境已创建好，Python 3.11，所有依赖已安装。

---

## 配置

### 1. 填写 API Key

编辑 `.env`：

```
GEMINI_API_KEY=你的key        # 默认使用，免费额度大
OPENAI_API_KEY=你的key        # 可选，切换到 GPT 时填写
```

### 2. 选择模型（可选）

编辑 `config.yaml`（默认已是 Gemini，无需改动）：

```yaml
llm:
  provider: google          # google | openai
  model: gemini-2.5-flash   # gemini-2.5-pro | gpt-5 | gpt-5-mini
  temperature: 0.3
  max_tokens: 4000
```

---

## 使用流程

### Step 1：放入 JD 文件

将 JD 复制到 `data/jd/`，支持：

```
data/jd/target_job.txt
data/jd/target_job.pdf
data/jd/target_job.docx
```

### Step 2：运行

```bash
python main.py
```

程序会自动完成：

1. 分析 JD → `outputs/jd_analysis.md`
2. 匹配知识库 → `outputs/match_report.md`
3. 生成中文简历 → `outputs/resume_cn.tex`
4. 翻译英文简历 → `outputs/resume_en.tex`
5. （可选）编译 PDF → `outputs/pdf/`

### Step 3：编辑并导出 PDF

在 VS Code 中打开 `outputs/resume_cn.tex` 或 `resume_en.tex` 手动调整，然后编译：

```bash
xelatex outputs/resume_cn.tex
xelatex outputs/resume_en.tex
```

> 需要安装 MacTeX：`brew install --cask mactex-no-gui`

---

## 填充知识库

知识库是简历的原材料，越详细效果越好：

```
knowledge_base/
├── experience/     # 每段实习一个 .md 文件（EY.md, Citic.md ...）
├── projects/       # 每个项目一个 .md 文件
├── skills/         # 每类技能一个 .md 文件
└── terminology/    # 行业术语库（可选）
```

参考已有的示例文件格式填写。

---

## 更新主简历模板

`data/master_resume_cn.tex` 是基础模板，填入你的真实信息（姓名、学校、联系方式）。英文版对应 `data/master_resume_en.tex`。

---

## 项目结构

202606JD_CV/
├── templates/                 # 基础模板 + 共享资源（真实数据，.gitignore 已排除）
│   ├── resume_cn.tex          # 中文基础模板（全部经历）
│   ├── resume_en.tex          # 英文基础模板（全部经历）
│   └── photo.jpg              # 证件照（所有岗位共享）
├── jobs/                      # 按岗位定制（真实数据，.gitignore 已排除）
│   └── ai_pm/                 # 例如：AI 产品经理
│       ├── jd.txt             # 岗位 JD
│       ├── resume_cn.tex      # 定制中文简历
│       └── resume_en.tex      # 定制英文简历
├── examples/                  # 虚构示范数据（会被提交到 GitHub），结构与上面完全一致
│   ├── templates/
│   ├── jobs/demo_fintech_pm/
│   └── knowledge_base/
├── Makefile                   # 编译 + 新建岗位
├── src/                       # Python 工具链（未动）
├── knowledge_base/            # 素材库；working experience/、academic experience and projects/ 为真实数据已排除，terminology/ 为通用术语保留
├── outputs/                   # Python pipeline 产物（保留兼容，.gitignore 已排除）
└── ...
工作流：

操作 命令
新建岗位 make new JOB=risk_control
编译简历 make compile JOB=ai_pm LANG=cn
编译中英文 make all JOB=ai_pm
清理产物 make clean JOB=ai_pm
查看所有岗位 make list

\graphicspath 已配置好，photo.jpg 统一放在 templates/，所有岗位目录编译时自动找到。outputs/ 保留不动，避免破坏 Python 工具链。
