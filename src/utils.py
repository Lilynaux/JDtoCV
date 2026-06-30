import re

from config import PROMPTS_DIR


def strip_codeblock(text: str) -> str:
    """Remove markdown code fences that LLMs sometimes wrap around LaTeX output."""
    text = text.strip()
    text = re.sub(r'^```[a-zA-Z]*\n', '', text)
    text = re.sub(r'\n```$', '', text)
    return text.strip()


def load_prompt(name: str) -> str:
    """Read a prompt template from prompts/<name>.md."""
    return (PROMPTS_DIR / f"{name}.md").read_text(encoding="utf-8")
