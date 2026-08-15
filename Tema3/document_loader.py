from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader, GoogleDriveLoader

def read_pdf():
  loader = PyPDFLoader("rcl.pdf")
  #loader = PyPDFLoader("cv_de_prueba_1.pdf")

  pages = loader.load()

  for i, page in enumerate(pages):
    print(f"=== Página {i+1} ===")
    print(f"Contenido: {page.page_content}")
    print(f"Metadatos: {page.metadata}")

def read_www():
  loader = WebBaseLoader("https://actualidad.rt.com/")

  docs = loader.load()

  print(docs)

read_www()