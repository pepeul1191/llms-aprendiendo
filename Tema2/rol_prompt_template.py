from langchain_ollama import ChatOllama
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate

plantilla_sistema = SystemMessagePromptTemplate.from_template("" \
  "Eres un {rol} especializado en {especialidad}. Responde de manera {tono}"
)

plantilla_humano = HumanMessagePromptTemplate.from_template(
  "Mi pregunta sobre {tema} es {pregunta}"
)

template = ChatPromptTemplate.from_messages([
  plantilla_sistema,
  plantilla_humano
])

mensajes = template.format_messages(
  rol="nutricionista",
  especialidad="dietas veganas",
  tono="profesional pero accesible",
  tema="proteinas vegetales",
  pregunta="¿Cuáles son las mejores fuentes de protenía para un atleta profesional?"
)

datos = {
  "rol": "nutricionista",
  "especialidad": "dietas veganas",
  "tono": "profesional pero accesible",
  "tema": "proteinas vegetales",
  "pregunta": "¿Cuáles son las mejores fuentes de protenía para un atleta profesional?"
}

print("**************  historial **************")
for m in mensajes:
  print(m.content)

models = ['deepseek-r1:1.5b', 'llama3.2', 'deepseek-r1', 'qwen3:4b',]

llm = ChatOllama(
  model=models[0],
  temperature=0.7
)

chain = template | llm # LLMChain(llm=llm, prompt=template)
response = chain.invoke(datos) # chain.run(name="Juan")

print("IA:", response.content)