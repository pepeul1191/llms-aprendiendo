# schemas.py
from typing import Literal, Optional
from pydantic import BaseModel, Field


class GraficoSpec(BaseModel):
    tipo: Literal["bar", "line", "pie", "scatter", "area"] = Field(
        description="Tipo de gráfico a generar"
    )
    titulo: str = Field(description="Título del gráfico")
    archivo: str = Field(
        description="Nombre del archivo CSV a usar (solo el nombre, ej: 'ventas.csv')"
    )
    x: str = Field(description="Nombre exacto de la columna del eje X")
    y: list[str] = Field(
        description="Nombres exactos de una o más columnas del eje Y"
    )


class RespuestaLLM(BaseModel):
    texto: str = Field(description="Respuesta en lenguaje natural al usuario")
    requiere_grafico: bool = Field(
        default=False,
        description="True solo si el usuario pidió explícitamente un gráfico o visualización",
    )
    grafico: Optional[GraficoSpec] = Field(
        default=None,
        description="Especificación del gráfico cuando requiere_grafico=True",
    )