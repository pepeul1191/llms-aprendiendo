# ui/chat.py
import os
import json
import streamlit as st

from config import conv_dir, get_conversacion, MODELO_ACTIVO, NUM_GPU
from db import guardar_mensaje, cargar_historial
from schemas import GraficoSpec
from services.llm_service import responder
from services.vector_store import construir_o_cargar, agregar_archivos
from services.chart_service import construir_grafico


# ---------- Helpers ----------

def _hist_key(conv_id):    return f"hist_{conv_id}"
def _vs_key(conv_id):      return f"vs_{conv_id}"
def _upkey_key(conv_id):   return f"upkey_{conv_id}"


def _cargar_o_init_historial(conv_id: str):
    if _hist_key(conv_id) not in st.session_state:
        st.session_state[_hist_key(conv_id)] = cargar_historial(conv_id)


def _get_vectorstore(conv_id: str):
    if _vs_key(conv_id) not in st.session_state:
        with st.spinner("Preparando índice de documentos..."):
            st.session_state[_vs_key(conv_id)] = construir_o_cargar(conv_id)
    return st.session_state[_vs_key(conv_id)]


# ---------- Renderizado ----------

def _render_mensaje(m: dict):
    with st.chat_message(m["role"]):
        st.markdown(m["content"])
        if m.get("archivos"):
            st.caption("📎 Adjuntos: " + ", ".join(m["archivos"]))
        if m.get("grafico"):
            try:
                spec = GraficoSpec(**m["grafico"])
                fig = construir_grafico(spec, str(conv_dir(st.session_state.conv_activa)))
                st.plotly_chart(fig, use_container_width=True,
                                key=f"fig_{m.get('id', 'x')}")
            except Exception as e:
                st.warning(f"No se pudo reconstruir el gráfico: {e}")


def _guardar_archivos(conv_id: str, files) -> list[str]:
    nombres = []
    for f in files:
        destino = conv_dir(conv_id) / f.name
        with open(destino, "wb") as out:
            out.write(f.getbuffer())
        nombres.append(f.name)
    return nombres


# ---------- Main ----------

def render_chat():
    conv_id = st.session_state.get("conv_activa")
    if not conv_id:
        st.info("👈 Selecciona una conversación en el sidebar para comenzar.")
        return

    conv = get_conversacion(conv_id)
    st.markdown(
        f"### {conv['nombre']}  \n"
        f"`modelo: {MODELO_ACTIVO}` · `código: {conv['codigo']}` · `GPU: {NUM_GPU}`"
    )
    st.divider()

    _cargar_o_init_historial(conv_id)
    historial = st.session_state[_hist_key(conv_id)]

    # --- Adjuntar archivos ---
    if _upkey_key(conv_id) not in st.session_state:
        st.session_state[_upkey_key(conv_id)] = 0

    with st.expander("📎 Adjuntar PDFs o CSVs a esta conversación", expanded=False):
        files = st.file_uploader(
            "Selecciona archivos (PDF/CSV). Puedes agregar más en cualquier momento.",
            type=["pdf", "csv"],
            accept_multiple_files=True,
            key=f"up_{conv_id}_{st.session_state[_upkey_key(conv_id)]}",
        )
        if files and st.button("📥 Procesar archivos", key=f"btn_up_{conv_id}"):
            nombres = _guardar_archivos(conv_id, files)
            rutas = [str(conv_dir(conv_id) / n) for n in nombres]

            with st.spinner("Indexando archivos..."):
                vs = st.session_state.get(_vs_key(conv_id))
                vs = agregar_archivos(conv_id, rutas, vs)
                st.session_state[_vs_key(conv_id)] = vs

            # Registrar en el chat + DB
            texto = "📎 Archivos agregados: " + ", ".join(nombres)
            guardar_mensaje(conv_id, "system", texto, archivos=nombres)
            historial.append({"role": "system", "content": texto,
                              "archivos": nombres, "grafico": None})

            st.session_state[_upkey_key(conv_id)] += 1
            st.rerun()

    # --- Historial visible ---
    for m in historial:
        _render_mensaje(m)

    # --- Entrada de chat ---
    pregunta = st.chat_input("Escribe tu pregunta sobre los documentos de esta conversación...")
    if not pregunta:
        return

    # Mensaje del usuario
    with st.chat_message("user"):
        st.markdown(pregunta)
    guardar_mensaje(conv_id, "user", pregunta)
    historial.append({"role": "user", "content": pregunta, "grafico": None})

    # Respuesta del LLM
    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            vs = _get_vectorstore(conv_id)
            try:
                resultado = responder(conv_id, pregunta, historial[:-1], vs)
            except Exception as e:
                st.error(f"Error al consultar el modelo: {e}")
                return

            st.markdown(resultado.texto)

            grafico_dict = None
            if resultado.requiere_grafico and resultado.grafico:
                try:
                    fig = construir_grafico(resultado.grafico, str(conv_dir(conv_id)))
                    st.plotly_chart(fig, use_container_width=True)
                    grafico_dict = resultado.grafico.model_dump()
                except Exception as e:
                    st.warning(f"No se pudo generar el gráfico: {e}")

            guardar_mensaje(
                conv_id,
                "assistant",
                resultado.texto,
                grafico=grafico_dict,
            )
            historial.append({
                "role": "assistant",
                "content": resultado.texto,
                "grafico": grafico_dict,
            })