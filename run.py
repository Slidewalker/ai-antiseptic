# run.py – Truth Safe entry point
import typer
from include import *

app = typer.Typer()

@app.command()
def ask(query: str):
    log(f"Query: {query}")
    if is_forbidden(query):
        print("REJECTED – forbidden collective language detected")
        return
    print(reflection_speak(f"You asked: {query}"))
    print("Full RAG engine loading soon – stay sovereign.")

if __name__ == "__main__":
    log(GOD_DECLARATION)
    app()
