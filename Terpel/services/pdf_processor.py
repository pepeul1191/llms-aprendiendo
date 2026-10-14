# services/pdf_proccesor.py
from io import BytesIO
from pypdf import PdfReader


def extraer_texto_pdf_bytes(data: bytes) -> str:
    try:
        reader = PdfReader(BytesIO(data))
        partes = []
        for i, pagina in enumerate(reader.pages, 1):
            t = pagina.extract_text() or ""
            if t.strip():
                partes.append(f"\n--- PÁGINA {i} ---\n{t}\n")
        texto = "".join(partes).strip()
        return texto or "Error: PDF vacío o solo imágenes."
    except Exception as e:
        return f"Error al procesar PDF: {e}"


def extraer_texto_pdf_path(path: str) -> str:
    with open(path, "rb") as f:
        return extraer_texto_pdf_bytes(f.read())