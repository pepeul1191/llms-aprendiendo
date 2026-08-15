from langchain_community.document_loaders import GoogleDriveLoader

credentials_path = "./credentials.json"
token_path = "./token.json"

loader = GoogleDriveLoader(
  folder_id="1J5jRt8ft6HqsA1VLzewyQwaOA5G69uAL",
  credentials_path=credentials_path,
  token_path=token_path,
  recursive=True
)

documents = loader.load()

print(documents)