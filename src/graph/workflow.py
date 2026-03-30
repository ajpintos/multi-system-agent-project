"""
Grafo del Sistema Multi-Agente — implementado con LangGraph.

Estructura del grafo:
                    ┌─────────────┐
    entrada ───────▶│ orchestrator│
                    └──────┬──────┘
                           │  add_conditional_edges
                           │  (basado en state["departamento"])
              ┌────────────┼────────────┬────────────┐
              ▼            ▼            ▼            ▼
           [rrhh]      [tech]     [marketing]   [finanzas]
              └────────────┴────────────┴────────────┘
                                 │
                                END

Cada nodo especialista:
    1. Lee el system prompt del .md correspondiente.
    2. Crea la cadena RAG con los documentos de su departamento.
    3. Invoca la cadena y almacena la respuesta en state["respuesta"].
"""
from pathlib import Path
from typing import Optional

from langchain_core.runnables import RunnableConfig
from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph
from typing_extensions import TypedDict

from ..agents.orchestrator import build_orchestrator_chain
from ..agents.specialist import build_specialist_chain
from ..knowledge import (
    FINANZAS_DOCUMENTS,
    MARKETING_DOCUMENTS,
    RRHH_DOCUMENTS,
    TECH_DOCUMENTS,
)
from ..logger_configuration import logger

# ---------------------------------------------------------------------------
# Estado compartido del grafo
# ---------------------------------------------------------------------------

_SRC_DIR = Path(__file__).parent.parent


class GraphState(TypedDict):
    query: str
    departamento: Optional[str]
    razon: Optional[str]
    respuesta: Optional[str]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _read_prompt(filename: str) -> str:
    return (_SRC_DIR / filename).read_text(encoding="utf-8")


def _build_llm() -> ChatOpenAI:
    return ChatOpenAI(model="gpt-4o-mini", temperature=0.3)


# ---------------------------------------------------------------------------
# Nodo 1: Orquestador — clasifica la consulta
# ---------------------------------------------------------------------------


def orchestrator_node(state: GraphState, config: RunnableConfig) -> dict:
    """Llama al LLM para clasificar la consulta en un departamento."""
    chain = build_orchestrator_chain(_build_llm())
    result = chain.invoke({"query": state["query"]}, config=config)
    logger.info(f"[Orquestador] → {result['departamento']} | {result['razon']}")
    return {"departamento": result["departamento"], "razon": result["razon"]}


# ---------------------------------------------------------------------------
# Función de decisión (conditional edge)
# ---------------------------------------------------------------------------


def route_decision(state: GraphState) -> str:
    """
    Determina el siguiente nodo según el departamento elegido por el orquestador.
    Sirve como función de decisión para add_conditional_edges.
    """
    dept = (state.get("departamento") or "").upper()
    routing = {
        "RRHH": "rrhh",
        "TECH": "tech",
        "MARKETING": "marketing",
        "FINANZAS": "finanzas",
    }
    route = routing.get(dept)
    if route is None:
        logger.warning(f"Departamento desconocido '{dept}' — usando RRHH como fallback.")
        return "rrhh"
    return route


# ---------------------------------------------------------------------------
# Fábrica de nodos especialistas
# ---------------------------------------------------------------------------


def _make_specialist_node(dept_label: str, prompt_file: str, documents: list):
    """
    Genera dinámicamente un nodo especialista para evitar repetición de código.
    Cada nodo cierra sobre su propio prompt y documentos.
    """

    def node(state: GraphState, config: RunnableConfig) -> dict:
        system_prompt = _read_prompt(prompt_file)
        chain = build_specialist_chain(_build_llm(), system_prompt, documents)
        response = chain.invoke({"query": state["query"]}, config=config)
        logger.info(f"[{dept_label}] Respuesta generada.")
        return {"respuesta": response}

    node.__name__ = dept_label.lower() + "_node"
    return node


# ---------------------------------------------------------------------------
# Construcción del grafo compilado
# ---------------------------------------------------------------------------


def build_workflow():
    """
    Construye y compila el StateGraph completo del sistema multi-agente.

    Returns:
        CompiledGraph listo para invocar con .invoke(state, config=...).
    """
    graph = StateGraph(GraphState)

    # Nodos
    graph.add_node("orchestrator", orchestrator_node)
    graph.add_node("rrhh", _make_specialist_node("RRHH", "RRHH.md", RRHH_DOCUMENTS))
    graph.add_node("tech", _make_specialist_node("Tech", "Tech.md", TECH_DOCUMENTS))
    graph.add_node("marketing", _make_specialist_node("Marketing", "Marketing.md", MARKETING_DOCUMENTS))
    graph.add_node("finanzas", _make_specialist_node("Finanzas", "Finanzas.md", FINANZAS_DOCUMENTS))

    # Punto de entrada
    graph.set_entry_point("orchestrator")

    # Edge condicional: orquestador → agente especialista
    graph.add_conditional_edges(
        "orchestrator",
        route_decision,
        {
            "rrhh": "rrhh",
            "tech": "tech",
            "marketing": "marketing",
            "finanzas": "finanzas",
        },
    )

    # Todos los agentes especialistas terminan el flujo
    for dept in ("rrhh", "tech", "marketing", "finanzas"):
        graph.add_edge(dept, END)

    return graph.compile()
