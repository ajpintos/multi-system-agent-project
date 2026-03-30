"""
Sistema Multi-Agente — Los chicos de Henry
Punto de entrada principal del orquestador.

Uso:
    uv run python -m src.main --query "¿Cuántos días de vacaciones tengo?"
"""
import argparse

from dotenv import load_dotenv

load_dotenv()

from .graph.workflow import build_workflow  # noqa: E402 (necesita load_dotenv primero)
from .logger_configuration import logger  # noqa: E402
from .tracing.setup import get_langfuse_handler  # noqa: E402


def go():
    parser = argparse.ArgumentParser(description="Sistema Multi-Agente — Los chicos de Henry")
    parser.add_argument("--query", type=str, required=True, help="Consulta del usuario")
    args = parser.parse_args()

    # Trazado opcional con Langfuse
    langfuse_handler = get_langfuse_handler()
    config = {"callbacks": [langfuse_handler]} if langfuse_handler else {}

    # Construcción y ejecución del grafo
    workflow = build_workflow()
    result = workflow.invoke({"query": args.query}, config=config)

    # Salida formateada
    separator = "=" * 60
    print(f"\n{separator}")
    print(f"Departamento : {result['departamento']}")
    print(f"Razón        : {result['razon']}")
    print(f"\nRespuesta:\n{result['respuesta']}")
    print(separator)

    logger.info("Flujo completado exitosamente.")


if __name__ == "__main__":
    go()
