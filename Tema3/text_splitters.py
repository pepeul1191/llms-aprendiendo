from langchain_community.document_loaders import PyPDFLoader
from langchain_ollama import ChatOllama
from langchain_text_splitters import RecursiveCharacterTextSplitter

models = ['deepseek-r1:1.5b', 'llama3.2', 'deepseek-r1', 'qwen3:4b',]

llm = ChatOllama(
  model=models[0],
  temperature=0.7
)

loader = PyPDFLoader("rsl.pdf")
pages = loader.load()

# dividir el texto en chunks màs pequeños
text_spllitter = RecursiveCharacterTextSplitter(
  chunk_size=3000,
  chunk_overlap=200
)

chunks = text_spllitter.split_documents(pages)

summaries = []

for chunk in chunks:
  response = llm.invoke(f"Haz un resumen de los puntos más importantes del siguiente documento: {chunk}")
  summaries.append(response.content)
  print('+++++++++++++++++++++++++++')
  print(response.content)

final_summary = llm.invoke(f"Combia y sintetiza estos resúmenes en un resumen coherente y completo: {" ".join(summaries)}")
print(final_summary)