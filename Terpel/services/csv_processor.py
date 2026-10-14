# services/csv_processor.py
import os
import pandas as pd


def resumen_csv(path: str, max_filas_muestra: int = 20) -> str:
    """Devuelve un resumen textual del CSV para el LLM."""
    try:
        df = pd.read_csv(path)
    except Exception as e:
        return f"Error leyendo CSV {os.path.basename(path)}: {e}"

    partes = [
        f"ARCHIVO: {os.path.basename(path)}",
        f"Filas: {len(df)} | Columnas: {list(df.columns)}",
        f"Tipos: {df.dtypes.astype(str).to_dict()}",
    ]
    try:
        partes.append("Estadísticas:\n" + df.describe(include="all").to_string())
    except Exception:
        pass
    partes.append(
        "Muestra de filas:\n" + df.head(max_filas_muestra).to_csv(index=False)
    )
    return "\n\n".join(partes)


def catalogo_csv(conv_dir: str) -> str:
    """Lista todos los CSVs con sus columnas (para incluir en el prompt)."""
    lineas = []
    for f in sorted(os.listdir(conv_dir)):
        if f.lower().endswith(".csv"):
            try:
                df = pd.read_csv(os.path.join(conv_dir, f), nrows=5)
                lineas.append(f"- {f} | columnas: {list(df.columns)}")
            except Exception as e:
                lineas.append(f"- {f} | (error: {e})")
    return "\n".join(lineas) if lineas else "(no hay CSVs cargados)"