from langchain_core.runnables import RunnableLambda
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

# análisis de sentimientos con formato JSON
def analyze_sentiment(text):
  prompt = f"""Analiza el sentimiento del siguiente texto
  Responde ÚNICAMENTE en formato JSON válido:
  {{"sentimiento": "positivo|negativo|neutro", "razon": "justificación breve, menos de 50 caracteres"}}

  Texto: {text}"""

  response = llm.invoke(prompt)

  #print("RESPUESTA DEL MODELO:")
  #print(response.content)

  try:
    contenido = response.content

    contenido = contenido.replace("```json", "")
    contenido = contenido.replace("```", "")
    contenido = contenido.strip()

    return json.loads(contenido)
  except json.JSONDecodeError:
    return {
      "sentimiento": "neutro",
      "razon": "Error de análisis"
    }

# Combinación de resultados
def merge_results(resumen, sentimiento_data):
  """Combina los resultados de ambas ramas en un formato unificado"""
  return {
    "resumen": resumen,
    "sentimiento": sentimiento_data["sentimiento"],
    "razon": sentimiento_data["razon"],
  }

def process_one(t):
  resumen = generate_summery(t)
  sentimimento_data = analyze_sentiment(t)
  return merge_results(resumen, sentimimento_data)

process = RunnableLambda(process_one) #1:16

chain = preprocessor | process

texto = """
    Me encantó este producto. La calidad es excelente,
    funciona perfectamente y llegó mucho antes de lo esperado.
"""

resultado = chain.invoke(texto)

print(resultado)