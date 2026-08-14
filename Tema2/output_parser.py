from enum import Enum

from pydantic import BaseModel, Field
from langchain_ollama import ChatOllama


# -----------------------------------
# Modelo de datos
# -----------------------------------

class Sentimiento(str, Enum):
    POSITIVO = "Positivo"
    NEUTRO = "Neutro"
    NEGATIVO = "Negativo"


class AnalisisTexto(BaseModel):

    resumen: str = Field(
        description="Resumen breve del texto"
    )

    sentimiento: Sentimiento = Field(
        description="Sentimiento del texto: Positivo, Neutro o Negativo"
    )


# -----------------------------------
# Modelo Ollama
# -----------------------------------

models = [
    "deepseek-r1:1.5b",
    "deepseek-r1",
    "llama3.2",
    "qwen3:4b"
]

llm = ChatOllama(
    model=models[0],
    temperature=0
)


# -----------------------------------
# Salida estructurada
# -----------------------------------

structured_llm = llm.with_structured_output(AnalisisTexto)


# -----------------------------------
# Texto a analizar
# -----------------------------------

texto_prueba = (
    "Me encantó la nueva película de acción, "
    "tiene muchos efectos especiales y acción."
)


# -----------------------------------
# Ejecutar
# -----------------------------------

resultado = structured_llm.invoke(
    f"""
    Analiza el siguiente texto.

    Genera:
    - Un resumen breve.
    - El sentimiento general: Positivo, Neutro o Negativo.

    Texto:
    {texto_prueba}
    """
)


print(resultado)