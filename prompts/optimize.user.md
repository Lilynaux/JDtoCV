请根据以下信息，生成一份针对目标岗位优化的中文简历（LaTeX格式）。

## 目标岗位JD
{jd_text}

## JD分析结果
{jd_analysis}

## 候选人知识库
{knowledge_base}

## 主简历（LaTeX模板）
{master_resume}

---
请按以下步骤思考（思考过程不要写进输出，只输出最终LaTeX）：

### Step 1 — 定义 Positioning（人设先行）

结合JD与候选人知识库，确定 HR 读完这份简历后应记住的 3 个核心标签（例如 "Financial Business + AI Product + Technical Understanding"）。后续所有内容取舍都必须服务于这 3 个标签；不能强化任何标签的经历应降级、压缩或删除。

### Step 2 — 构建 Career Narrative（职业故事）

确保所有经历能串联成一条统一的职业故事（例如：业务理解 → 产品设计 → 技术落地），而不是互相独立、各自证明不同能力的项目堆砌。

### Step 3 — 按统一结构组织每段经历

Business Background（一句话业务场景，不展开背景介绍）→ Responsibility（一句话Ownership，不要写"参与"）→ Core Contribution（2~3条Bullet，每条Bullet只证明一个能力）→ Result（一句话业务价值，优先量化，没有数据则描述业务成果）。

### Step 4 — Bullet 写作规则

每条Bullet遵循 One Bullet → One Purpose → One Capability，禁止一条Bullet同时证明多种能力（如产品+算法+Demo+测试+用户研究+数据分析+项目管理）；一句话能拆成两条就拆开。Bullet目标是理解成本最小化，而不是信息最大化。

### Step 5 — Main Story vs Supporting Evidence

判断哪些经历是 Main Story（直接支撑目标岗位，应重点展开），哪些是 Supporting Evidence（证明学习能力或技术背景，如数学建模、科研、竞赛，应简洁保留），Supporting Evidence 不应占据 Main Story 的篇幅。

### Step 6 — Skills 部分

仅用于证明基础能力（如Python、SQL、机器学习），集中展示，不要与项目经历中的Bullet重复出现。

### Step 7 — 自查后再输出

确认以下问题均为"是"后再生成最终LaTeX：HR能否在30秒内记住3个核心标签？所有经历是否共同服务于同一个Career Narrative？是否存在一条Bullet堆砌多个能力？是否有无关经历占据了核心篇幅？所有项目是否采用统一结构（Background→Responsibility→Contribution→Result）？每条经历能否在2~3分钟内作为面试问答自然讲述？

---
输出要求：
1. 完整的LaTeX文件内容（可直接用xelatex编译）
2. 使用 \documentclass[UTF8]{{ctexart}} 支持中文
3. 保留Jake's Resume风格的结构（Education, Experience, Projects, Skills）
4. 只输出最终LaTeX代码，不要输出思考过程或额外解释
