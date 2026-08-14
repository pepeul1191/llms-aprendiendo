from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

models = ['deepseek-r1:1.5b', 'llama3.2', 'deepseek-r1', 'qwen3:4b',]

llm = ChatOllama(
  model=models[0],
  temperature=0.7
)

chat_prompt = ChatPromptTemplate.from_messages([
  ("system",
        "Eres un traductor profesional de español a inglés. "
        "Traduce el texto del usuario al inglés. "
        "Responde únicamente con la traducción, sin explicaciones."),
  ("human", "{texto}")
])

chain = chat_prompt | llm # LLMChain(llm=llm, prompt=template)

template = chat_prompt.format_messages(texto="Hola mundo, ¿cómo estás?")

for m in template:
  print(f"{type(m)}; {m.content}")

response = chain.invoke({"texto":"Hola mundo, ¿cómo estás?"}) # chain.run(name="Juan")

print(response.content)