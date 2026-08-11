from langchain_ollama import ChatOllama
from langchain.schema import AIMessage, HumanMessage, SystemMessage
import streamlit as st
from langchain.prompts import PromptTemplate

# configurar la página de la aplicación
st.set_page_config(page_title="Chatbot con LangChain y Ollama", page_icon="🤖")
st.title("🤖 Chatbot con LangChain y Ollama")
st.markdown("Este es un chatbot simple construido con LangChain y Ollama.")

models = ['deepseek-r1:1.5b', 'deepseek-r1', 'llama3.2', 'qwen3:4b',]

with st.sidebar:
  st.header('Configuración: ')
  temperature = st.slider("Temperatura", 0.0, 1.0, 0.5, 0.1)
  model_name = st.selectbox("Modelo", models)

  llm = ChatOllama(model=model_name,temperature=temperature)

# crear prompt template
prompt_template = PromptTemplate(
  input_variables=["prompt", "historial"],
  template="""Eres un asistente ùtil y amigable llamado ChatBrot
Historial de conversación:
{historial}
  
Responde de manera clara y concisa a la siguiente pregunta: {prompt}
  """
)

# inicializar historial de chat
if "messages" not in st.session_state:
  st.session_state.messages = []

# mostrar mensajes del historial de chat
for message in st.session_state.messages:
  if isinstance(message, SystemMessage):
    continue

  # determinar el rol del mensaje
  role = "assistant" if isinstance(message, AIMessage) else "user"

  with st.chat_message(role):
    st.markdown(message.content)

if st.button(" Nueva conversación: "):
  st.session_state.messages = []
  st.rerun()

# cuadro de entrada de texto
prompt = st.chat_input("Escribe tu mensaje: ")

if prompt:
  # agregar mensaje del usuario al historial
  st.session_state.messages.append(HumanMessage(content=prompt))

  # mostrar mensaje del usuario en la interfaz
  with st.chat_message("user"):
    st.markdown(prompt)

   

  # generar respuesta del asistente
  response = llm.invoke(
    st.session_state.messages
  )

  # agregar respuesta del asistente al historial
  st.session_state.messages.append(
    AIMessage(content=response.content)
  )

  # mostrar respuesta del asistente en la interfaz
  with st.chat_message("assistant"):
    st.markdown(response.content)
