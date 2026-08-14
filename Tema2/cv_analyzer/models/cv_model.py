from pydantic import BaseModel, Field

class AnalisisCV(BaseModel):
    """Modelo de datos para el análisis completo de un Cv."""

    nombre_candidato: str = Field(description="Nombre completo del candidato extraído del CV.")
    experiencia_años: int = Field(description="Años totales de experiencia laboral relevante.")
    habilidades_clave: list[str] = Field(description="Lista de las 5-7 habilidades del candidato más relevantes para el puesto.")
    education: str = Field(description="Nivel educativo más alto y especialización principal.")
    experiencia_relevante: str = Field(description="Resumen conciso de la experiencia más relevante para el puesto específico.")
    fortalezas: list[str] = Field(description="3-5 principales fortalezas del candidato basadas en su perfil.")
    areas_mejora: list[str] = Field(description="2-4 áreas donde el candidato podría desarrollarse o mejorar.")
    porcentaje_ajuste: int = Field(description="Porcetaje de ajuste al puesto (0-100) basado en experiencia, habilidades y formación.", ge=0, le=100)