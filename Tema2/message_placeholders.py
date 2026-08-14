from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

template = ChatPromptTemplate.from_messages([
  ("system", "Eres un asistente útil que manitene el contexto de la conversación."),
  MessagesPlaceholder(variable_name="historial"),
  ("human", "{pregunta_actual}")
])

historial_conversacion = [
  HumanMessage(content="Usuario: ¿Cuál es la capital de Francia?"),
  AIMessage(content="IA: La capital de Francia es Paris."),
  HumanMessage(content="Usuario: ¿Y cuántos habitantes tiene?"),
  AIMessage(content="IA: Paris tiene aproximadamente 2.2 millones de habitantes"),
]

proceed = True

models = ['deepseek-r1:1.5b', 'llama3.2', 'deepseek-r1', 'qwen3:4b',]

llm = ChatOllama(
  model=models[0],
  temperature=0.7
)

while proceed:
  pregunta = input("Haga una pregunta: ")

  mensajes = template.format_messages(
    historial=historial_conversacion,
    pregunta_actual=pregunta
  )

  print("**************  historial **************")
  for m in mensajes:
    print(m.content)

  chain = template | llm # LLMChain(llm=llm, prompt=template)
  response = chain.invoke({
    "historial":historial_conversacion,
    "pregunta_actual": pregunta
  }) # chain.run(name="Juan")

  print("IA:", response.content)

  historial_conversacion.append(HumanMessage(content=pregunta))
  historial_conversacion.append(AIMessage(content=response.content))