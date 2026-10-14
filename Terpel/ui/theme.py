# ui/theme.py
import streamlit as st

DARK_CSS = """
<style>
:root { color-scheme: dark; }
.stApp { background-color: #0e1117; color: #e6edf3; }
[data-testid="stSidebar"] { background-color: #161b22; }
[data-testid="stSidebar"] * { color: #e6edf3 !important; }
.stChatMessage { background-color: #1c2128; border: 1px solid #30363d; }
.stTextInput input, .stTextArea textarea, .stSelectbox > div > div {
    background-color: #21262d !important; color: #e6edf3 !important;
    border: 1px solid #30363d !important;
}
.stButton > button {
    background-color: #21262d; color: #e6edf3; border: 1px solid #30363d;
}
.stButton > button:hover { background-color: #30363d; }
h1, h2, h3, h4 { color: #e6edf3 !important; }
.navbar {
    background: linear-gradient(90deg,#111827,#1f2937);
    border: 1px solid #30363d; border-radius: 12px;
    padding: 12px 20px; margin-bottom: 12px;
    display: flex; align-items: center; gap: 14px;
}
.navbar .logo {
    font-size: 28px; font-weight: 800;
    background: linear-gradient(90deg,#60a5fa,#a78bfa,#f472b6);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.navbar .sub { color:#9ca3af; font-size: 12px; }
</style>
"""

LIGHT_CSS = """
<style>
:root { color-scheme: light; }
.stApp { background-color: #ffffff; color: #1f2328; }
[data-testid="stSidebar"] { background-color: #f6f8fa; }
.stChatMessage { background-color: #f6f8fa; border: 1px solid #e5e7eb; }
.navbar {
    background: linear-gradient(90deg,#eef2ff,#f5f3ff);
    border: 1px solid #e5e7eb; border-radius: 12px;
    padding: 12px 20px; margin-bottom: 12px;
    display: flex; align-items: center; gap: 14px;
}
.navbar .logo {
    font-size: 28px; font-weight: 800;
    background: linear-gradient(90deg,#2563eb,#7c3aed,#db2777);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.navbar .sub { color:#6b7280; font-size: 12px; }
</style>
"""


def aplicar_tema():
    if st.session_state.get("dark_mode", True):
        st.markdown(DARK_CSS, unsafe_allow_html=True)
    else:
        st.markdown(LIGHT_CSS, unsafe_allow_html=True)