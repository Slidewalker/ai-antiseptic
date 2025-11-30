# antiseptic/utils.py
import os
import textwrap
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.syntax import Syntax

console = Console()

def print_banner():
    """Print a beautiful startup banner"""
    banner = """
    🧼 AI Antiseptic 🧼
    Grounded • Private • Verifiable
    NotebookLM-style RAG, but 100% yours.
    """
    console.print(Panel(banner, style="bold cyan", expand=False))

def format_sources(sources):
    """Pretty-print retrieved sources with numbering"""
    if not sources:
        return "No sources retrieved."
    
    output = []
    for i, doc in enumerate(sources, 1):
        page = doc.metadata.get("page", "N/A")
        source = doc.metadata.get("source", "Unknown")
        filename = Path(source).name
        snippet = doc.page_content.strip().replace("\n", " ")
        short = textwrap.shorten(snippet, width=200, placeholder="...")
        output.append(f"[bold yellow]{i}.[/] [dim]{filename}[/] (page {page})\n   {short}")
    
    return "\n".join(output)

def pretty_print_response(response: str):
    """Print final answer in a clean, readable panel"""
    console.print("\n[bold green]Answer[/bold green]")
    console.print(Panel(Markdown(response), border_style="bright_blue"))

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def save_response(text: str, filename: str = "antiseptic_response.txt"):
    """Quick save to file"""
    Path(filename).write_text(text, encoding="utf-8")
    console.print(f"Saved response → {filename}")

def syntax_print(code: str, language: str = "python"):
    """Print code blocks nicely"""
    syntax = Syntax(code, language, theme="monokai", line_numbers=True)
    console.print(syntax)
