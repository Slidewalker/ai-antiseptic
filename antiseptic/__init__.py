"""
AI Antiseptic 🧼🤖
Open-source, private, grounded RAG system – NotebookLM style.
"""

from .core import build_antiseptic_chain
from .cli import app as cli_app
from .audio import generate_audio_overview

__version__ = "0.1.0"
__all__ = [
    "build_antiseptic_chain",
    "cli_app",
    "generate_audio_overview",
]
