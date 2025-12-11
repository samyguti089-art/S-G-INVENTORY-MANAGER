import streamlit as st
import login as lgn
from utils import animaciones

st.set_page_config(
    page_title="S&G INVENTORY MANAGER",
    page_icon="🖥",
    layout="wide"
)

# ✅ Fondo animado y estilo
animaciones()

# ✅ Estructura visual: logo a la izquierda, login a la derecha
col1, col2 = st.columns([1, 2], gap="large")

with col1:
    st.markdown("""
        <div class="pulse" style="text-align:center;">
            <img src="https://raw.githubusercontent.com/your-repo/logo.png" width="180">
            <h2 style="color:white; margin-top:10px;">S&G INVENTORY MANAGER</h2>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="fade-in" style="padding-top:40px;">
            <h3 style="color:white;">🔒 Inicio de sesión</h3>
        </div>
    """, unsafe_allow_html=True)
    autenticado = lgn.user_password()

# ✅ Si no está autenticado, detener la app
if not autenticado:
    st.stop()
