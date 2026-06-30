import re


def strip_codeblock(text: str) -> str:
    """Remove markdown code fences that LLMs sometimes wrap around LaTeX output."""
    text = text.strip()
    text = re.sub(r'^```[a-zA-Z]*\n', '', text)
    text = re.sub(r'\n```$', '', text)
    return text.strip()
