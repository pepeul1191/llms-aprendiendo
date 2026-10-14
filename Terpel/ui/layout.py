# ui/layout.py 
import streamlit as st

from config import CONVERSACIONES
from db import cargar_historial


def render_navbar():
    dark = st.session_state.get("dark_mode", True)
    icono_tema = "☀️" if dark else "🌙"
    tooltip = "Cambiar a modo claro" if dark else "Cambiar a modo oscuro"

    col_logo, col_theme = st.columns([6, 1])

    with col_logo:
        st.markdown(
            """
            <div class="navbar">
                <div class="logo">◆ DataChat AI</div>
                <div class="sub">Análisis inteligente de PDFs y CSVs por conversación</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_theme:
        if st.button(icono_tema, help=tooltip, use_container_width=True,
                     key="btn_tema"):
            st.session_state.dark_mode = not dark
            st.rerun()


def render_sidebar():
    with st.sidebar:
        st.markdown("### 💬 Conversaciones")
        st.caption("Selecciona una máquina para chatear")

        for conv in CONVERSACIONES:
            activo = st.session_state.get("conv_activa") == conv["id"]
            etiqueta = f"{'🟢' if activo else '⚪'} **{conv['nombre']}**"
            st.markdown(etiqueta)
            st.caption(
                f"🧠 Modelo: `{conv['modelo']}`  \n"
                f"🔑 Código: `{conv['codigo']}`"
            )
            if st.button(
                "Abrir conversación" if not activo else "En uso",
                key=f"sel_{conv['id']}",
                use_container_width=True,
                disabled=activo,
            ):
                st.session_state.conv_activa = conv["id"]
                st.rerun()
            st.divider()

        # Botón para limpiar historial de la conversación activa
        conv_id = st.session_state.get("conv_activa")
        if conv_id:
            if st.button("🗑️ Limpiar historial", use_container_width=True,
                         key="btn_limpiar"):
                from db import limpiar_conversacion
                limpiar_conversacion(conv_id)
                st.session_state.pop(f"hist_{conv_id}", None)
                st.success("Historial eliminado")
                st.rerun()