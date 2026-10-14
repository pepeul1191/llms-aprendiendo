from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_ollama import ChatOllama

from config import (
    get_conversacion, conv_dir,
    MODELO_ACTIVO, NUM_GPU, NUM_CTX,
)
from schemas import RespuestaLLM
from services.csv_processor import catalogo_csv

SYSTEM_PROMPT = """Eres un asistente experto en análisis de documentos y datos.
Respondes SIEMPRE en español, de forma clara y profesional.

Tienes acceso a fragmentos de los documentos (PDF/CSV) del usuario.
Usa SOLO la información del contexto proporcionado. Si no alcanza, dilo.

CATÁLOGO DE CSVs DISPONIBLES:
{catalogo}

REGLAS PARA GRÁFICOS:
- Si el usuario pide un gráfico, visualización, chart o similar, configura
  `requiere_grafico=True` y completa `grafico` con:
    * tipo: "bar" | "line" | "pie" | "scatter" | "area"
    * titulo: string
    * archivo: nombre EXACTO del CSV del catálogo
    * x: nombre EXACTO de una columna
    * y: lista con nombres EXACTOS de columnas
- Si el usuario NO pide gráfico, deja `requiere_grafico=False` y `grafico=null`.
- Nunca inventes columnas ni archivos que no existan en el catálogo.
"""


def _crear_llm() -> ChatOllama:
    """Instancia ChatOllama con la MISMA configuración del ejemplo:
       model=models[2], num_gpu=99, num_ctx=2048, verbose=True."""
    return ChatOllama(
        model=MODELO_ACTIVO,   # "llama3.2"  (igual que models[2])
        temperature=0.2,
        num_ctx=NUM_CTX,       # 2048
        num_gpu=NUM_GPU,       # 99  →  fuerza uso de GPU
        verbose=True,
    )


def responder(conv_id: str, pregunta: str, historial: list[dict],
              vector_store) -> RespuestaLLM:
    conv = get_conversacion(conv_id)
    if not conv:
        raise ValueError(f"Conversación desconocida: {conv_id}")

    # 1) Contexto RAG
    contexto = ""
    if vector_store is not None:
        try:
            docs = vector_store.similarity_search(pregunta, k=4)
            contexto = "\n\n---\n\n".join(d.page_content for d in docs)
        except Exception as e:
            contexto = f"(Error recuperando contexto: {e})"

    # 2) Prompt
    catalogo = catalogo_csv(str(conv_dir(conv_id)))
    mensajes = [SystemMessage(content=SYSTEM_PROMPT.format(catalogo=catalogo))]

    for m in historial[-12:]:
        if m["role"] == "user":
            mensajes.append(HumanMessage(content=m["content"]))
        elif m["role"] == "assistant":
            mensajes.append(AIMessage(content=m["content"]))

    if contexto:
        user_content = (
            f"CONTEXTO RECUPERADO DE LOS DOCUMENTOS:\n{contexto}\n\n"
            f"PREGUNTA DEL USUARIO:\n{pregunta}"
        )
    else:
        user_content = pregunta
    mensajes.append(HumanMessage(content=user_content))

    # 3) Invocación con GPU
    llm = _crear_llm()
    structured = llm.with_structured_output(RespuestaLLM)
    return structured.invoke(mensajes)