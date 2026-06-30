"""ResumeTailor — main entry point."""
import sys
import time
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.rule import Rule

import yaml
from config import JD_DIR, OPENAI_API_KEY, GEMINI_API_KEY, OUTPUT_RESUME_CN, MASTER_RESUME_CN
from src.jd_loader import load_jd
from src.jd_analyzer import analyze_jd
from src.knowledge_base import load_knowledge_base, format_kb_for_prompt
from src.resume_optimizer import generate_match_report, optimize_resume_cn
from src.translator import translate_cn_to_en
from src.resume_diff import print_diff
from src.latex_exporter import compile_all

console = Console()


def pick_jd_file() -> Path:
    jd_files = list(JD_DIR.glob("*"))
    jd_files = [f for f in jd_files if f.suffix.lower() in (".txt", ".pdf", ".docx")]

    if not jd_files:
        console.print("[red]No JD files found in data/jd/. Add a .txt, .pdf, or .docx file.[/red]")
        sys.exit(1)

    if len(jd_files) == 1:
        console.print(f"[green]Using JD:[/green] {jd_files[0].name}")
        return jd_files[0]

    console.print("[bold]Available JD files:[/bold]")
    for i, f in enumerate(jd_files, 1):
        console.print(f"  {i}. {f.name}")
    choice = Prompt.ask("Select JD", default="1")
    return jd_files[int(choice) - 1]


def main():
    console.print(Panel.fit("[bold cyan]ResumeTailor[/bold cyan]\nJD → Tailored Resume", border_style="cyan"))

    _cfg = yaml.safe_load(open("config.yaml", encoding="utf-8"))
    _provider = _cfg.get("llm", {}).get("provider", "google")
    if _provider == "google" and not GEMINI_API_KEY:
        console.print("[red]ERROR: Set GEMINI_API_KEY in .env[/red]")
        sys.exit(1)
    if _provider == "openai" and (not OPENAI_API_KEY or OPENAI_API_KEY == "your_openai_api_key_here"):
        console.print("[red]ERROR: Set OPENAI_API_KEY in .env[/red]")
        sys.exit(1)

    start = time.time()

    # Step 1: Load JD
    console.rule("[bold]Step 1/6 — Load JD[/bold]")
    jd_path = pick_jd_file()
    jd_text = load_jd(jd_path)
    console.print(f"[green]✓[/green] Loaded {len(jd_text)} chars from {jd_path.name}")

    # Step 2: Analyze JD
    console.rule("[bold]Step 2/6 — Analyze JD[/bold]")
    jd_analysis = analyze_jd(jd_text)
    console.print("[green]✓[/green] Saved → outputs/jd_analysis.md")
    console.print(jd_analysis[:600] + "…\n")

    # Step 3: Load Knowledge Base
    console.rule("[bold]Step 3/6 — Load Knowledge Base[/bold]")
    kb = load_knowledge_base()
    if not kb:
        console.print("[yellow]Warning: Knowledge base is empty. Add .md files to knowledge_base/[/yellow]")
    else:
        console.print(f"[green]✓[/green] Loaded {len(kb)} knowledge base files")
    kb_text = format_kb_for_prompt(kb)

    # Step 4: Match Report
    console.rule("[bold]Step 4/6 — Generate Match Report[/bold]")
    match_report = generate_match_report(jd_text, jd_analysis, kb_text)
    console.print("[green]✓[/green] Saved → outputs/match_report.md")
    console.print(match_report[:400] + "…\n")

    # Step 5: Optimize CN Resume
    console.rule("[bold]Step 5/6 — Generate CN Resume[/bold]")
    original_cn = MASTER_RESUME_CN.read_text(encoding="utf-8") if MASTER_RESUME_CN.exists() else ""
    optimized_cn = optimize_resume_cn(jd_text, jd_analysis, kb_text)
    console.print("[green]✓[/green] Saved → outputs/resume_cn.tex")

    if original_cn:
        print_diff(original_cn, optimized_cn)

    # Step 6: Translate to EN
    console.rule("[bold]Step 6/6 — Translate to EN[/bold]")
    translate_cn_to_en(optimized_cn)
    console.print("[green]✓[/green] Saved → outputs/resume_en.tex")

    # Optional: compile PDF
    compile = Prompt.ask("\nCompile to PDF with xelatex?", choices=["y", "n"], default="n")
    if compile == "y":
        try:
            cn_pdf, en_pdf = compile_all()
            if cn_pdf:
                console.print(f"[green]✓[/green] {cn_pdf}")
            if en_pdf:
                console.print(f"[green]✓[/green] {en_pdf}")
        except RuntimeError as e:
            console.print(f"[red]PDF compilation failed:[/red] {e}")

    elapsed = time.time() - start
    console.print(Panel.fit(
        f"[bold green]Done in {elapsed:.1f}s[/bold green]\n\n"
        "outputs/jd_analysis.md\n"
        "outputs/match_report.md\n"
        "outputs/resume_cn.tex\n"
        "outputs/resume_en.tex",
        title="Output Files", border_style="green"
    ))


if __name__ == "__main__":
    main()
