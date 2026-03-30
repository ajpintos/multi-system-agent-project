"""
Agente Especialista — responde con información recuperada (RAG).

Cadena LangChain (LCEL):
    RunnablePassthrough.assign(context=<retriever>)
        →  ChatPromptTemplate  →  ChatOpenAI  →  StrOutputParser

El flujo de recuperación:
    1. Se construye un InMemoryVectorStore con los documentos del departamento.
    2. El retriever busca los k documentos más similares a la query del usuario.
    3. Los documentos recuperados se formatean e inyectan en el system prompt.
    4. El LLM genera una respuesta fundamentada en ese contexto.
"""
from operator import itemgetter

from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import ChatOpenAI, OpenAIEmbeddings


def _format_docs(docs: list[Document]) -> str:
    """Convierte una lista de Documents en un bloque de texto para el prompt."""
    return "\n\n---\n\n".join(doc.page_content for doc in docs)


def build_specialist_chain(llm: ChatOpenAI, system_prompt: str, documents: list[Document]):
    """
    Construye y retorna la cadena RAG del agente especialista.

    Args:
        llm:           instancia de ChatOpenAI ya configurada.
        system_prompt: contenido del archivo .md del departamento.
        documents:     lista de Documents de la base de conocimiento.

    Returns:
        Runnable que acepta {"query": str} y retorna la respuesta como str.
    """
    # --- Construcción del vector store en memoria ---
    embeddings = OpenAIEmbeddings()
    vectorstore = InMemoryVectorStore(embedding=embeddings)
    vectorstore.add_documents(documents)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

    # --- Prompt con contexto recuperado ---
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                system_prompt + "\n\n## Información de contexto relevante:\n{context}",
            ),
            ("human", "{query}"),
        ]
    )

    # --- Cadena LCEL ---
    # itemgetter("query") extrae la query para pasarla al retriever;
    # RunnablePassthrough() propaga el dict completo para el prompt.
    chain = (
        RunnablePassthrough.assign(
            context=itemgetter("query") | retriever | _format_docs
        )
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain
