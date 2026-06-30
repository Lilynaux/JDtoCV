"""Feature 1: JD Analyzer."""
from config import OUTPUT_JD_ANALYSIS
from src.llm_factory import get_llm

_SYSTEM = """\
你是一名专业的简历顾问和职业规划师，擅长分析招聘JD并提炼关键信息。
请用结构化Markdown输出，保持简洁专业。"""

_PROMPT = """\
请分析以下职位描述（JD），并输出以下内容：

## Position Summary
一段话概括岗位核心职责和定位。

## Required Skills
必要技能列表（bullet points）。

## Preferred Skills
加分项技能列表（bullet points）。

## ATS Keywords
适合放入简历的ATS关键词（逗号分隔，15-25个词）。

## Missing Skills Analysis
[此项需结合知识库对比，暂输出占位符：待匹配知识库后填充]

## Match Score
[待知识库匹配后计算，0-100分]

---
JD内容：
{jd_text}
"""


def analyze_jd(jd_text: str) -> str:
    llm = get_llm()
    result = llm.generate(
        prompt=_PROMPT.format(jd_text=jd_text),
        system=_SYSTEM,
    )
    OUTPUT_JD_ANALYSIS.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_JD_ANALYSIS.write_text(result, encoding="utf-8")
    return result
