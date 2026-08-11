from langchain_ollama import ChatOllama
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

models = ['deepseek-r1:1.5b', 'llama3.2', 'deepseek-r1', 'qwen3:4b',]

llm = ChatOllama(
  model=models[0],
  temperature=0.7
)

# hola mundo
'''
response = llm.invoke("como se suma dos número en el lenguaje de programación ruby")
print(response.content)
'''

template = PromptTemplate(
  input_variables=["name"],
  template="Saludo al usuario nombre.\n Nombre del usuario: {name}Asistente:"
)

chain = template | llm # LLMChain(llm=llm, prompt=template)
response = chain.invoke({"name":"Juan"}) # chain.run(name="Juan")

print(response.content)


