"""
Configuración de Langfuse para el trazado del sistema multi-agente.

Langfuse captura automáticamente cada llamada al LLM y cada paso del grafo
a través del CallbackHandler de LangChain.

Para activar el trazado, agregar al .env:
    LANGFUSE_SECRET_KEY=sk-lf-...
    LANGFUSE_PUBLIC_KEY=pk-lf-...
    LANGFUSE_HOST=https://cloud.langfuse.com  (opcional, es el valor por defecto)
"""
import os

from ..logger_configuration import logger


def get_langfuse_handler():
    """
    Retorna un CallbackHandler de Langfuse si las credenciales están configuradas.
    Si no lo están, retorna None y el sistema corre sin trazado.
    """
    secret_key = os.getenv("LANGFUSE_SECRET_KEY")
    public_key = os.getenv("LANGFUSE_PUBLIC_KEY")

    if not secret_key or not public_key:
        logger.warning("Langfuse no configurado. Ejecutando sin trazado.")
        return None

    try:
        from langfuse.callback import CallbackHandler

        handler = CallbackHandler(
            secret_key=secret_key,
            public_key=public_key,
            host=os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com"),
        )
        logger.info("Langfuse activado — los traces se enviarán a Langfuse Cloud.")
        return handler
    except ImportError:
        logger.warning("Paquete 'langfuse' no instalado. Ejecutando sin trazado.")
        return None
