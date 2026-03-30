# Sistema Multi-Agente

Sistema de agentes IA que enruta consultas al departamento correcto usando LangGraph + FastAPI.

## Setup

```bash
uv sync
cp .env_example .env   # completar con las API keys
```

Variables requeridas en `.env`:
- `OPENAI_API_KEY` — clave de OpenAI
- `OPENAI_MODEL` — modelo a usar (default: `gpt-4o-mini`)

## Correr por CLI

```bash
uv run python -m src.main --query "Necesito ayuda con nómina"
```

## Correr por API

```bash
uv run uvicorn api.Router.main:app --reload
```

Luego enviar una consulta:

```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"query": "Necesito ayuda con nómina"}'
```

Respuesta:

```json
{
  "departamento": "RRHH",
  "razon": "La consulta es sobre nómina y pagos a empleados",
  "respuesta": "..."
}
```

## Cómo funciona

1. **Orquestador** — recibe la consulta y la clasifica en un departamento via LLM
2. **Router** — dirige al agente especialista correspondiente
3. **Especialista** — responde usando su prompt y base de conocimiento

Departamentos disponibles: `RRHH`, `Tech`, `Finanzas`, `Marketing`
