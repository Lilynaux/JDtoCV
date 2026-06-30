"""LaTeX compilation — compile .tex to PDF using xelatex."""
import subprocess
import shutil
from pathlib import Path
from config import OUTPUTS_DIR, PDF_DIR


def compile_latex(tex_path: Path, output_name: str | None = None) -> Path:
    """Compile a .tex file with xelatex. Returns path to generated PDF."""
    if not shutil.which("xelatex"):
        raise RuntimeError(
            "xelatex not found. Install MacTeX: brew install --cask mactex-no-gui"
        )

    PDF_DIR.mkdir(parents=True, exist_ok=True)
    output_name = output_name or tex_path.stem

    result = subprocess.run(
        ["xelatex", "-interaction=nonstopmode", "-output-directory", str(PDF_DIR), str(tex_path)],
        capture_output=True,
        text=True,
        cwd=str(tex_path.parent),
    )

    pdf_path = PDF_DIR / f"{output_name}.pdf"
    if not pdf_path.exists():
        raise RuntimeError(
            f"xelatex compilation failed.\n\nSTDOUT:\n{result.stdout[-2000:]}\n\nSTDERR:\n{result.stderr[-1000:]}"
        )
    return pdf_path


def compile_all() -> tuple[Path | None, Path | None]:
    """Compile both CN and EN resumes. Returns (cn_pdf, en_pdf)."""
    from config import OUTPUT_RESUME_CN, OUTPUT_RESUME_EN

    cn_pdf = en_pdf = None
    if OUTPUT_RESUME_CN.exists():
        cn_pdf = compile_latex(OUTPUT_RESUME_CN, "resume_cn")
    if OUTPUT_RESUME_EN.exists():
        en_pdf = compile_latex(OUTPUT_RESUME_EN, "resume_en")
    return cn_pdf, en_pdf
