# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install dependencies (uses uv)
uv sync

# Run the FastAPI server
uv run uvicorn api.Router.main:app --reload

# Run the CLI orchestrator
uv run python -m src.main --query "Necesito ayuda con nómina"

# Lint
uv run ruff check src/ api/

# Format
uv run ruff format src/ api/
```

No test suite exists yet.

## Environment

Copy `.env_example` to `.env` and fill in values:

```
OPENAI_API_KEY=         # Required for all agent calls
OPENAI_MODEL=gpt-4o-mini
TVLY_API_KEY=           # Required for Tavily web search
LANGCHAIN_API_KEY=      # Optional: LangSmith tracing
LANGCHAIN_TRACING_V2=
LANGCHAIN_PROJECT=henry-ai-engineering
```

## Architecture

The project has two independent modules that are not yet connected:

**`src/` — CLI Orchestrator**
- `src/main.py` — CLI entry point (`go()` function, `--query` arg)
- `src/call_api.py` — OpenAI chat completions wrapper (`call_api(system_prompt, user_prompt, json_mode)`)
- `src/logger_configuration.py` — ANSI-colored logger (green=INFO, yellow=WARNING, red=ERROR)
- `src/Orquestador.md` — System prompt for the orchestrator agent

**`api/` — FastAPI application**
- `api/Router/main.py` — FastAPI app instance; currently only has a stub `/books` endpoint

### Agent Routing Pattern

System prompts for each agent role are stored as `.md` files in `src/`. The orchestrator (`Orquestador.md`) receives a user query and returns JSON indicating which department should handle it:

```json
{"departamento": "RRHH", "razon": "..."}
```

Departments: `RRHH`, `Marketing`, `Finanzas`, `Tech`. Their `.md` prompt files exist but are empty — the intended pattern is to read the relevant `.md` file, pass it as `system_prompt` to `call_api()`, then call the department agent.

### Scaffolded (not yet implemented)

- `src/agents/` — individual agent modules
- `src/graph/` — LangGraph workflow definitions
- `src/rag/` — ChromaDB / FAISS vector store setup
- `src/tracing/` — observability

### Known issues in current code

- `call_api.py`: `client` is never defined. An `OpenAI` client must be initialized (e.g., `client = OpenAI()` after `load_dotenv()`).
- `src/main.py`: `system_prompt = Orquestador.md` is a bare name reference, not a file read. Should be `open(Path(__file__).parent / "Orquestador.md").read()`.
