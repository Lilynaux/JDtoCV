"""Feature 2: Knowledge Base — load all markdown files from knowledge_base/."""
from pathlib import Path
from config import KNOWLEDGE_BASE_DIR


def load_knowledge_base() -> dict[str, str]:
    """Return {relative_path: content} for every .md file in knowledge_base/."""
    kb: dict[str, str] = {}
    for md_file in sorted(KNOWLEDGE_BASE_DIR.rglob("*.md")):
        key = md_file.relative_to(KNOWLEDGE_BASE_DIR).as_posix()
        kb[key] = md_file.read_text(encoding="utf-8")
    return kb


def format_kb_for_prompt(kb: dict[str, str]) -> str:
    """Flatten KB into a single string for prompt injection."""
    sections = []
    for path, content in kb.items():
        sections.append(f"### [{path}]\n{content.strip()}")
    return "\n\n".join(sections)
