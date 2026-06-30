"""Feature 6: Resume Diff — show changes between master and optimized resume."""
import difflib
from pathlib import Path
from rich.console import Console
from rich.text import Text


def diff_resumes(original: str, optimized: str, label: str = "Resume Diff") -> str:
    """Return a unified diff string between original and optimized."""
    orig_lines = original.splitlines(keepends=True)
    opt_lines = optimized.splitlines(keepends=True)
    diff = list(difflib.unified_diff(
        orig_lines, opt_lines,
        fromfile="master_resume",
        tofile="optimized_resume",
        lineterm="",
    ))
    return "".join(diff)


def print_diff(original: str, optimized: str) -> None:
    """Print colored diff to terminal using rich."""
    console = Console()
    orig_lines = original.splitlines()
    opt_lines = optimized.splitlines()
    diff = difflib.unified_diff(orig_lines, opt_lines, fromfile="master", tofile="optimized", lineterm="")

    console.rule("[bold cyan]Resume Diff[/bold cyan]")
    for line in diff:
        if line.startswith("+++") or line.startswith("---"):
            console.print(Text(line, style="bold white"))
        elif line.startswith("+"):
            console.print(Text(line, style="green"))
        elif line.startswith("-"):
            console.print(Text(line, style="red"))
        elif line.startswith("@@"):
            console.print(Text(line, style="cyan"))
        else:
            console.print(line)
