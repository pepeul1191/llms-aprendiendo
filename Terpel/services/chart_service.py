# services/chart_service.py
import os
import pandas as pd
import plotly.express as px

from schemas import GraficoSpec


def construir_grafico(spec: GraficoSpec, conv_dir_path: str):
    """Genera la figura Plotly a partir de la especificación del LLM."""
    archivo = os.path.basename(spec.archivo)
    ruta = os.path.join(conv_dir_path, archivo)
    if not os.path.exists(ruta):
        raise FileNotFoundError(f"No existe el archivo CSV: {archivo}")

    df = pd.read_csv(ruta)

    # Validar columnas
    faltantes = [c for c in [spec.x] + list(spec.y) if c not in df.columns]
    if faltantes:
        raise ValueError(
            f"Columnas no encontradas en {archivo}: {faltantes}. "
            f"Disponibles: {list(df.columns)}"
        )

    y = spec.y if len(spec.y) > 1 else spec.y[0]
    titulo = spec.titulo or f"{spec.tipo.title()} de {y}"

    if spec.tipo == "bar":
        fig = px.bar(df, x=spec.x, y=y, title=titulo)
    elif spec.tipo == "line":
        fig = px.line(df, x=spec.x, y=y, title=titulo, markers=True)
    elif spec.tipo == "area":
        fig = px.area(df, x=spec.x, y=y, title=titulo)
    elif spec.tipo == "pie":
        fig = px.pie(df, names=spec.x, values=spec.y[0], title=titulo)
    elif spec.tipo == "scatter":
        fig = px.scatter(df, x=spec.x, y=y, title=titulo)
    else:
        raise ValueError(f"Tipo de gráfico no soportado: {spec.tipo}")

    fig.update_layout(template="plotly_white", height=480)
    return fig