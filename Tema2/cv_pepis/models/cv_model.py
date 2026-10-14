# models/cv_model.py
from pydantic import BaseModel, Field

class AnalisisCV(BaseModel):
  nombre_candidato: str = Field(description="Nombre completo extraìdo del cv.")
  experiencia_años: int = Field(description="Años totales de experiencia laboral relevante.")
  habilidades_clave: list[str] = Field(description="Lista de las 5 a 7 hablidades del candidato para el puesto")
  education: str = Field(description="Nivel educativo más alto y especializado el postulante")
  experiencia_relevante: str = Field(description="Resumen conciso de la expericencia más relevante para el puesto específico")
  fortalezas: list[str] = Field(description="3-5 principales fortalezas del candidato basadas en su perfil")
  areas_mejora: list[str] = Field(description="2-4 áreas donde el cantidado podría mejorar")
  porcentaje_ajuste: int = Field(description="Porcentaje de ajusto al puesto (0-100) basado en experiencia, habilidades y fomración.", ge=0, le=100)