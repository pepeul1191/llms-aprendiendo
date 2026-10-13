from enum import Enum

from models.cv_model import AnalisisCV
from prompts.cv_prompts import crear_sistema_prompts
from langchain_ollama import ChatOllama

models = ["deepseek-r1:7b", "deepseek-r1", "llama3.2",  "qwen3:4b"]

def crear_evaluador_cv():
  llm = ChatOllama(
        model=models[2],
        temperature=0.2,
        num_ctx=2048,
        num_gpu=99,
        verbose=True,
    )
  modelo_estructurado = llm.with_structured_output(AnalisisCV)
  chat_prompt = crear_sistema_prompts()
  cadena_evaluacion = chat_prompt | modelo_estructurado
  return cadena_evaluacion

def evaluar_candidato(texto_cv: str, descripcion_puesto: str) -> AnalisisCV:
  try:
    cadena_evaluacion = crear_evaluador_cv()

    resultado = cadena_evaluacion.invoke({
      "texto_cv": texto_cv,
      "descripcion_puesto": descripcion_puesto
    })

    return resultado

  except Exception as e:
    import traceback
    traceback.print_exc()
    return AnalisisCV(
      nombre_candidato="Error en procesamiento",
      experiencia_años=0,
      habilidades_clave=["Error al procesar CV"],
      education="No se puede determinar",
      experiencia_relevante="Error durante el análisis",
      fortalezas=["Requiere revisión manual del CV"],
      areas_mejora=["Verificar formato y legibilidad del PDF"],
      porcentaje_ajuste=0
    )
