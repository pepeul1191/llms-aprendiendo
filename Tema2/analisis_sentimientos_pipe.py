from langchain_core.runnables import RunnableLambda, RunnableParallel
from langchain_ollama import ChatOllama
import json

# configuración del modelo
models = ['deepseek-r1:1.5b', 'deepseek-r1', 'llama3.2', 'qwen3:4b',]
llm = ChatOllama(model=models[0],temperature=0)

# procesador: limpia espacios y limita 500 caracteres
def preprocess_text(text):
  """Limpia el texto elimniando espacios extras y limitando longitud"""
  return text.strip()[:500]

preprocessor = RunnableLambda(preprocess_text)

# generación de resumen
def generate_summery(text):
  """Genera un resumen conciso del texto"""
  prompt = f"Resume en una sola oración: {text}"
  response = llm.invoke(prompt)
  return response.content.strip()

summary_branch = RunnableLambda(generate_summery)

# análisis de sentimientos con formato JSON
def analyze_sentiment(text):
  prompt = f"""Analiza el sentimiento del siguiente texto.

Responde ÚNICAMENTE en formato JSON válido:
{{"sentimiento": "positivo|negativo|neutro", "razon": "justificación breve, menos de 50 caracteres"}}

Texto: {text}"""

  response = llm.invoke(prompt)

  print("\nRESPUESTA DEL MODELO:")
  print(response.content)

  try:
    contenido = response.content

    contenido = contenido.replace("```json", "")
    contenido = contenido.replace("```", "")
    contenido = contenido.strip()

    resultado = json.loads(contenido)

    #print("JSON PARSEADO:")
    #print(resultado)

    return resultado

  except json.JSONDecodeError:
    return {
      "sentimiento": "neutro",
      "razon": "Error de análisis"
    }

sentiment_branch = RunnableLambda(analyze_sentiment)

# Combinación de resultados
def merge_results(data):
  """Combina los resultados de ambas ramas en un formato unificado"""
  sentimiento_data = data.get("sentimiento_data", {})

  return {
    "resumen": data.get("resumen", ""),
    "sentimiento": sentimiento_data.get("sentimiento", "neutro"),
    "razon": sentimiento_data.get("razon", "Sin información"),
  }

merger = RunnableLambda(merge_results)

parrallel_analysis = RunnableParallel({
  "resumen": summary_branch,
  "sentimiento_data": sentiment_branch, 
})

chain = preprocessor | parrallel_analysis | merger

texto1 = """
    El servicio fue excelente. La atención fue rápida y el personal
    fue muy amable. Sin duda volvería a utilizar este servicio.
"""

texto2 = """
    Estoy muy decepcionado con la compra. El producto llegó tarde,
    estaba dañado y el soporte técnico nunca respondió a mis mensajes.
"""

texto3 = """
    El paquete llegó ayer. El producto funciona correctamente,
    aunque todavía no he tenido suficiente tiempo para evaluar
    si realmente cumple con todas mis expectativas.
"""

texto4 = """
    La aplicación es muy fácil de usar y tiene un diseño excelente,
    pero después de la última actualización empezó a cerrarse
    inesperadamente varias veces.
"""

# procesmando un elemento de manera paralela
#resultado = chain.invoke(texto1)
#print(resultado)

# procesamiento en paralelo de variaas entradas, procesando mùltiples elementos en paralelo
reviews = [texto1, texto2, texto3, texto4]
resultado_batch = chain.batch(reviews)