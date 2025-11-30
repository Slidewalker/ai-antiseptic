import typer
from rich.console import Console
from antiseptic.core import build_antiseptic_chain

app = typer.Typer()
console = Console()

@app.command()
def ask(question: str, sources_dir: str = "sources"):
    console.print("🧼 Building AI Antiseptic...", style="bold blue")
    chain = build_antiseptic_chain(sources_dir)
    console.print("Antiseptic ready. Asking...\n", style="bold green")
    response = chain.invoke(question)
    console.print(response, style="white on black")

if __name__ == "__main__":
    app()
