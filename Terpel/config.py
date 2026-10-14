from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

DB_PATH = DATA_DIR / "app.db"
CONV_DIR = DATA_DIR / "conversations"
CONV_DIR.mkdir(parents=True, exist_ok=True)

# ── Mismos modelos del código de ejemplo ─────────────────────────────
MODELS = ["deepseek-r1:7b", "deepseek-r1", "llama3.2", "qwen3:4b"]

# Índice del modelo activo (igual que en el ejemplo: models[2] = "llama3.2")
MODELO_ACTIVO = MODELS[2]

# Configuración GPU (misma que el ejemplo)
NUM_GPU = 99
NUM_CTX = 2048

# Modelo de embeddings (también se ejecutará en GPU)
EMBED_MODEL = "nomic-embed-text"

# Las 3 conversaciones: TODAS usan el mismo modelo activo (llama3.2)
CONVERSACIONES = [
    {"id": "conv_1", "nombre": "Máquina Alpha", "modelo": MODELO_ACTIVO, "codigo": "AL-001"},
    {"id": "conv_2", "nombre": "Máquina Beta",  "modelo": MODELO_ACTIVO, "codigo": "BE-002"},
    {"id": "conv_3", "nombre": "Máquina Gamma", "modelo": MODELO_ACTIVO, "codigo": "GA-003"},
]


def get_conversacion(conv_id: str) -> dict:
    return next((c for c in CONVERSACIONES if c["id"] == conv_id), None)


def conv_dir(conv_id: str) -> Path:
    p = CONV_DIR / conv_id
    p.mkdir(parents=True, exist_ok=True)
    return p