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

prompt_template = "Eres un experto en marketing. Sugiere un eslogan creativo para un producto {producto}."

template = PromptTemplate(
  input_variables=["producto"],
  template=prompt_template
)

chain = template | llm # LLMChain(llm=llm, prompt=template)
response = chain.invoke({"producto":"bicicleta"}) # chain.run(name="Juan")

print(response.content)


