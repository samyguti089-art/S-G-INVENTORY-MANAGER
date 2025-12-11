import streamlit as st
import login as lgn
from utils import animaciones

st.set_page_config(
    page_title="S&G INVENTORY MANAGER",
    page_icon="🖥",
    layout="wide"
)

# ✅ Fondo animado
animaciones()

# ✅ Estructura visual: logo izquierda, login derecha
col1, col2 = st.columns([1, 2], gap="large")

with col1:
    st.markdown('<div class="pulse" style="text-align:center;">', unsafe_allow_html=True)
    st.image("logo.png", width=200)  # ✅ AHORA SÍ SE VE EL LOGO
    st.markdown('<h2 style="color:white; margin-top:10px;">S&G INVENTORY MANAGER</h2>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<h3 style="color:white;">🔒 Inicio de sesión</h3>', unsafe_allow_html=True)
    autenticado = lgn.user_password()

# ✅ Si no está autenticado, detener la app
if not autenticado:
    st.stop()

