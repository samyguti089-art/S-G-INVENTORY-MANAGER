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
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown('<div class="pulse">', unsafe_allow_html=True)
    st.image("logo.png", width=200)
    st.markdown('<h2 style="color:white;">S&G INVENTORY MANAGER</h2>', unsafe_allow_html=True)

with col2:
    autenticado = lgn.user_password()

# ✅ Si no está autenticado, detener la app
if not autenticado:
    st.stop()
