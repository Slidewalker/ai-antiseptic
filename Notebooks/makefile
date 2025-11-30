# ╔══════════════════════════════════════════════════════════════╗
# ║                  AI Antiseptic – Makefile                    ║
# ╚══════════════════════════════════════════════════════════════╝

.PHONY: all install dev run ask audio demo serve web rebuild index clean distclean \
        banner test lint format docs release help

# ── Default ───────────────────────────────────────────────────
all: banner install

# ── Setup ─────────────────────────────────────────────────────
install:                        ## Install production dependencies
	pip install -r requirements.txt

dev: install                    ## Install dev + optional tools
	pip install -r requirements.txt jupyterlab ruff black mypy pre-commit
	pre-commit install

# ── Running ───────────────────────────────────────────────────
run:                            ## Run quick summary of all sources
	python run.py "Summarize everything in the sources"

ask:                            ## Interactive Q&A (best target ever)
	@read -p "Ask AI Antiseptic: " q; \
	echo "🧼 Thinking...\n"; \
	python run.py "$$q"

audio:                          ## Generate podcast-style audio overview
	python run.py "Create an engaging 2-minute audio overview of all sources" --audio

demo:                           ## Launch Jupyter demo
	jupyter lab notebooks/demo.ipynb

serve: dev                      ## Launch beautiful Gradio web UI (auto-creates if missing)
	python -c "from antiseptic.web import app; app.launch()" || \
		echo "Web UI not installed yet → run: pip install gradio"

web: serve

# ── Index Management ──────────────────────────────────────────
rebuild index:                  ## Delete & rebuild vector database from scratch
	rm -rf .chroma
	python run.py "What is AI Antiseptic?" --rebuild

update:                         ## Re-index only new/changed files (fast)
	python run.py "Update the knowledge base with new sources"

# ── Development ───────────────────────────────────────────────
test:                           ## Run basic sanity tests
	python -c "from antiseptic import build_antiseptic_chain; print('Chain builds OK')"

lint:                           ## Lint with ruff
	ruff check antiseptic tests *.py

format:                         ## Auto-format with black + ruff
	black .
	ruff check --fix
	isort .

docs:                           ## Generate README screenshots & docs (future)
	@echo "Docs generation coming soon..."

# ── Utilities ─────────────────────────────────────────────────
banner:                         ## Show beautiful banner
	python -c "from antiseptic.utils import print_banner; print_banner()"

clean:                          ## Remove temp files & audio
	rm -rf __pycache__ */__pycache__ *.pyc .mypy_cache .ruff_cache
	rm -f *.mp3 *.wav *.m4a overview.mp3

distclean: clean                ## Nuclear cleanup (keeps sources & config)
	rm -rf .chroma build dist *.egg-info

# ── Release ───────────────────────────────────────────────────
release: lint test              ## Prepare for release
	@echo "Ready for release! Don't forget to bump version in __init__.py"

# ── Help ──────────────────────────────────────────────────────
help:                           ## Show this help (you're looking at it!)
	@echo "\nAI Antiseptic Makefile – Available targets:\n"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  make \033[36m%-15s\033[0m %s\n", $$1, $$2}'
	@echo ""

# Default goal
.DEFAULT_GOAL := help
