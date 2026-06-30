"""Feature 4 & 5: CN→EN synchronization."""
from config import OUTPUT_RESUME_CN, OUTPUT_RESUME_EN
from src.llm_factory import get_llm
from src.utils import load_prompt, strip_codeblock

_SYSTEM = load_prompt("translate.system")
_PROMPT = load_prompt("translate.user")


def translate_cn_to_en(cn_tex: str | None = None) -> str:
    if cn_tex is None:
        if not OUTPUT_RESUME_CN.exists():
            raise FileNotFoundError("No CN resume found. Run optimize first.")
        cn_tex = OUTPUT_RESUME_CN.read_text(encoding="utf-8")

    llm = get_llm()
    result = strip_codeblock(llm.generate(
        prompt=_PROMPT.format(cn_resume=cn_tex),
        system=_SYSTEM,
    ))
    OUTPUT_RESUME_EN.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_RESUME_EN.write_text(result, encoding="utf-8")
    return result
