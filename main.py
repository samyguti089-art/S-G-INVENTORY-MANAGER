import streamlit as st
import pandas as pd
import login as lgn
from utils import logo_title, animaciones

# Configuración de la página (debe ir primero)
st.set_page_config(
    page_title="S&G INVENTORY MANAGER",
    page_icon="🖥",
    layout="wide"
)

# ✅ Cargar animaciones primero
animaciones()

# ✅ Mostrar logo y título ANTES del login
logo_title()

# ✅ Llamada al login
# Esta función debe manejar internamente si el usuario está autenticado o no
autenticado = lgn.user_password()

# ✅ Si NO está autenticado, detenemos la ejecución aquí
if not autenticado:
    st.stop()

# ✅ Si está autenticado, ahora sí mostramos la página principal
st.header('Página :blue[Principal]')
