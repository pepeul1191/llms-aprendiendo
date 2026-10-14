# ui/main.py
import streamlit as st

from db import init_db
from ui.theme import aplicar_tema
from ui.layout import render_navbar, render_sidebar
from ui.chat import render_chat


def _init_state():
    st.session_state.setdefault("dark_mode", True)
    st.session_state.setdefault("conv_activa", None)


def run():
    st.set_page_config(
        page_title="DataChat AI",
        page_icon="◆",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    init_db()
    _init_state()
    aplicar_tema()

    render_navbar()
    render_sidebar()
    render_chat()