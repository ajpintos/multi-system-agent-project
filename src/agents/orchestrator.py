"""
Agente Orquestador — clasifica la consulta del usuario en un departamento.

Cadena LangChain:
    ChatPromptTemplate  →  ChatOpenAI  →  JsonOutputParser
                                          (valida con Pydantic)

Salida esperada:
    {"departamento": "RRHH" | "Tech" | "Marketing" | "Finanzas",
     "razon": "<explicación breve>"}
"""
from pathlib import Path

from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field


class RoutingDecision(BaseModel):
    """Esquema de salida del orquestador."""

    departamento: str = Field(
        description="Departamento al que se deriva la consulta: RRHH, Tech, Marketing o Finanzas"
    )
    razon: str = Field(description="Breve justificación del enrutamiento")


def build_orchestrator_chain(llm: ChatOpenAI):
    """
    Construye y retorna la cadena LCEL del orquestador.

    Args:
        llm: instancia de ChatOpenAI ya configurada.

    Returns:
        Runnable que acepta {"query": str} y retorna un dict con
        claves 'departamento' y 'razon'.
    """
    system_prompt = (Path(__file__).parent.parent / "Orquestador.md").read_text(encoding="utf-8").replace("{", "{{").replace("}", "}}")

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "{query}"),
        ]
    )

    parser = JsonOutputParser(pydantic_object=RoutingDecision)

    # Cadena LCEL: prompt | llm | parser
    return prompt | llm | parser
