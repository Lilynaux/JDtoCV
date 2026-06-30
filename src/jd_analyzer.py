"""Feature 1: JD Analyzer."""
from config import OUTPUT_JD_ANALYSIS
from src.llm_factory import get_llm
from src.utils import load_prompt

_SYSTEM = load_prompt("jd_analysis.system")
_PROMPT = load_prompt("jd_analysis.user")


def analyze_jd(jd_text: str) -> str:
    llm = get_llm()
    result = llm.generate(
        prompt=_PROMPT.format(jd_text=jd_text),
        system=_SYSTEM,
    )
    OUTPUT_JD_ANALYSIS.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_JD_ANALYSIS.write_text(result, encoding="utf-8")
    return result
