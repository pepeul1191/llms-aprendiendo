# db.py
import json
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker

from config import DB_PATH

engine = create_engine(
    f"sqlite:///{DB_PATH}",
    connect_args={"check_same_thread": False},
    future=True,
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()


class Mensaje(Base):
    __tablename__ = "mensajes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    conversation_id = Column(String(64), index=True, nullable=False)
    role = Column(String(20), nullable=False)
    content = Column(Text, nullable=False)
    archivos = Column(Text, nullable=True)   # JSON
    grafico = Column(Text, nullable=True)    # JSON
    created_at = Column(DateTime, default=datetime.utcnow)


def init_db():
    """Crea la tabla si no existe (alternativa rápida al script SQL)."""
    Base.metadata.create_all(engine)


# ---------- CRUD helpers ----------

def guardar_mensaje(conversation_id: str, role: str, content: str,
                    archivos: list | None = None,
                    grafico: dict | None = None) -> Mensaje:
    with SessionLocal() as s:
        m = Mensaje(
            conversation_id=conversation_id,
            role=role,
            content=content,
            archivos=json.dumps(archivos, ensure_ascii=False) if archivos else None,
            grafico=json.dumps(grafico, ensure_ascii=False) if grafico else None,
        )
        s.add(m)
        s.commit()
        s.refresh(m)
        return m


def cargar_historial(conversation_id: str) -> list[dict]:
    with SessionLocal() as s:
        filas = (
            s.query(Mensaje)
            .filter(Mensaje.conversation_id == conversation_id)
            .order_by(Mensaje.created_at.asc(), Mensaje.id.asc())
            .all()
        )
        return [
            {
                "id": f.id,
                "role": f.role,
                "content": f.content,
                "archivos": json.loads(f.archivos) if f.archivos else None,
                "grafico": json.loads(f.grafico) if f.grafico else None,
                "created_at": f.created_at,
            }
            for f in filas
        ]


def limpiar_conversacion(conversation_id: str):
    with SessionLocal() as s:
        s.query(Mensaje).filter(Mensaje.conversation_id == conversation_id).delete()
        s.commit()