"""Feature 3: Resume Optimizer."""
from config import MASTER_RESUME_CN, OUTPUT_RESUME_CN, OUTPUT_MATCH_REPORT
from src.llm_factory import get_llm
from src.utils import strip_codeblock

_SYSTEM_OPTIMIZER = """\
你是一名专业的简历优化师。你的任务是根据目标职位JD，从候选人的知识库和主简历中，
精选并重组最相关的经历，生成针对性强的中文LaTeX简历。

规则：
- 绝对不编造经历、技能或数据
- 只能重新排列、精选和优化表达方式
- 保持LaTeX格式完整，可直接编译
- 突出与JD最匹配的技能和经历"""

_PROMPT_OPTIMIZER = """\
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
输出要求：
1. 完整的LaTeX文件内容（可直接用xelatex编译）
2. 使用 \\documentclass[UTF8]{{ctexart}} 支持中文
3. 保留Jake's Resume风格的结构（Education, Experience, Projects, Skills）
4. 只输出LaTeX代码，不要额外解释
"""

_PROMPT_MATCH = """\
根据以下JD和候选人知识库，生成一份匹配度分析报告：

## 目标JD
{jd_text}

## 候选人知识库
{knowledge_base}

输出：
## Match Score
X/100 — 一句话理由

## 强匹配项
与JD高度匹配的经历/技能（bullet points）

## 待补强项
JD要求但候选人暂时缺少的能力（bullet points）

## 建议优化方向
如何在不编造的前提下最大化匹配度（2-3条具体建议）
"""

_SYSTEM_MATCH = "你是一名专业的职业规划师，擅长客观评估人才与岗位的匹配度。"


def generate_match_report(jd_text: str, jd_analysis: str, kb_text: str) -> str:
    llm = get_llm()
    result = llm.generate(
        prompt=_PROMPT_MATCH.format(jd_text=jd_text, knowledge_base=kb_text),
        system=_SYSTEM_MATCH,
    )
    OUTPUT_MATCH_REPORT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_MATCH_REPORT.write_text(result, encoding="utf-8")
    return result


def optimize_resume_cn(jd_text: str, jd_analysis: str, kb_text: str) -> str:
    master = MASTER_RESUME_CN.read_text(encoding="utf-8") if MASTER_RESUME_CN.exists() else ""
    llm = get_llm()
    result = strip_codeblock(llm.generate(
        prompt=_PROMPT_OPTIMIZER.format(
            jd_text=jd_text,
            jd_analysis=jd_analysis,
            knowledge_base=kb_text,
            master_resume=master,
        ),
        system=_SYSTEM_OPTIMIZER,
    ))
    OUTPUT_RESUME_CN.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_RESUME_CN.write_text(result, encoding="utf-8")
    return result
