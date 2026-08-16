from langchain_ollama import OllamaEmbeddings
import numpy as np

embeddings = OllamaEmbeddings(model="embeddinggemma")

texto1 = "La capital de Francia es Paris"
texto2 = "Paris es la ciudad capital de Francia"
texto3 = "Paris es un nombre común para mascotas"

vec1 = embeddings.embed_query(texto1)
vec2 = embeddings.embed_query(texto2)
vec3 = embeddings.embed_query(texto3)

print(f"Dimensión de los vectores: {len(vec1)}")

cos_sim = np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

print(f"Similitud coseno entre vec1 y vec2: {cos_sim:.3f}")

cos_sim = np.dot(vec1, vec3) / (np.linalg.norm(vec1) * np.linalg.norm(vec3))

print(f"Similitud coseno entre vec1 y vec2: {cos_sim:.3f}")