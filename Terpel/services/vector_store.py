import os
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

from config import EMBED_MODEL, NUM_GPU, conv_dir
from services.pdf_processor import extraer_texto_pdf_path
from services.csv_processor import resumen_csv


def _embeddings() -> OllamaEmbeddings:
    """Embeddings con GPU forzada (mismo criterio que el LLM)."""
    return OllamaEmbeddings(
        model=EMBED_MODEL,
        num_gpu=NUM_GPU,   # 99 → usar GPU
    )


def _docs_desde_archivo(path: str) -> list[Document]:
    nombre = os.path.basename(path)
    if path.lower().endswith(".pdf"):
        texto = extraer_texto_pdf_path(path)
        splitter = RecursiveCharacterTextSplitter(chunk_size=900, chunk_overlap=120)
        return [
            Document(page_content=c, metadata={"source": nombre, "tipo": "pdf"})
            for c in splitter.split_text(texto)
        ]
    if path.lower().endswith(".csv"):
        return [
            Document(
                page_content=resumen_csv(path),
                metadata={"source": nombre, "tipo": "csv"},
            )
        ]
    return []


def _index_path(conv_id: str) -> str:
    return str(conv_dir(conv_id) / "faiss_index")


def _docs_de_conversacion(conv_id: str) -> list[Document]:
    d = conv_dir(conv_id)
    docs: list[Document] = []
    for f in sorted(os.listdir(d)):
        if f.lower().endswith((".pdf", ".csv")):
            docs.extend(_docs_desde_archivo(os.path.join(d, f)))
    return docs


def construir_o_cargar(conv_id: str) -> FAISS | None:
    emb = _embeddings()
    ruta = _index_path(conv_id)
    if os.path.exists(ruta):
        return FAISS.load_local(ruta, emb, allow_dangerous_deserialization=True)

    docs = _docs_de_conversacion(conv_id)
    if not docs:
        return None
    vs = FAISS.from_documents(docs, emb)
    vs.save_local(ruta)
    return vs


def agregar_archivos(conv_id: str, rutas: list[str], vs: FAISS | None) -> FAISS | None:
    emb = _embeddings()
    docs: list[Document] = []
    for r in rutas:
        docs.extend(_docs_desde_archivo(r))
    if not docs:
        return vs

    if vs is None:
        vs = FAISS.from_documents(docs, emb)
    else:
        vs.add_documents(docs)
    vs.save_local(_index_path(conv_id))
    return vs