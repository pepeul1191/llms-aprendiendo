from pydantic import BaseModel

class Usuario(BaseModel):
  id: int
  nombre: str
  activo: bool = True

data = {"id": "123", "nombre": "Ana"}

usuario = Usuario(**data)

print(usuario)