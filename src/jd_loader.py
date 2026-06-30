"""Load JD content from txt, pdf, or docx files."""
from pathlib import Path
import pdfplumber
from docx import Document


def load_jd(path: str | Path) -> str:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"JD file not found: {p}")

    suffix = p.suffix.lower()

    if suffix == ".txt":
        return p.read_text(encoding="utf-8")

    if suffix == ".pdf":
        text = []
        with pdfplumber.open(p) as pdf:
            for page in pdf.pages:
                text.append(page.extract_text() or "")
        return "\n".join(text)

    if suffix == ".docx":
        doc = Document(p)
        return "\n".join(para.text for para in doc.paragraphs)

    raise ValueError(f"Unsupported JD format: {suffix}. Use .txt, .pdf, or .docx")
