"""Feature 4 & 5: CN→EN synchronization."""
from config import OUTPUT_RESUME_CN, OUTPUT_RESUME_EN
from src.llm_factory import get_llm
from src.utils import strip_codeblock

_SYSTEM = """\
你是一名专业的双语简历翻译专家，专注于将中文简历精准翻译为英文。

规则：
- 保持LaTeX结构完全不变，只翻译文本内容
- 使用行业标准英文表达，避免直译
- 动词开头的bullet points（如Led, Designed, Implemented）
- 数字和专有名词保持原样
- 输出完整LaTeX文件"""

_PROMPT = """\
请将以下中文LaTeX简历翻译为英文版本。

要求：
1. 保持完整LaTeX代码结构
2. 只翻译中文内容为英文，不改变任何格式命令
3. 英文动词使用过去式，bullet以动词开头
4. 保留所有公司名、学校名的英文写法

中文简历：
{cn_resume}
"""


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
