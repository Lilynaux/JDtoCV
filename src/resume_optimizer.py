"""Feature 3: Resume Optimizer."""
from config import MASTER_RESUME_CN, OUTPUT_RESUME_CN, OUTPUT_MATCH_REPORT
from src.llm_factory import get_llm
from src.utils import load_prompt, strip_codeblock

_SYSTEM_OPTIMIZER = load_prompt("optimize.system")
_PROMPT_OPTIMIZER = load_prompt("optimize.user")

_PROMPT_MATCH = load_prompt("match.user")
_SYSTEM_MATCH = load_prompt("match.system")


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
