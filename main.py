import streamlit as st
import pandas as pd
import login as lgn
from utils import logo_title, animaciones, menu

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
autenticado = lgn.user_password()

# ✅ Si NO está autenticado, detenemos la ejecución aquí
if not autenticado:
    st.stop()

# ✅ Si está autenticado, mostrar menú dinámico
opcion = menu(st.session_state["usuario"], st.session_state["rol"])

# ✅ Cargar páginas según la opción seleccionada
if opcion == "Inicio":
    st.header("🏠 Página Principal")

elif opcion == "Inventario":
    st.header("📦 Inventario")
    st.write("Aquí va tu módulo de inventario...")

elif opcion == "Administración de usuarios":
    from admin_usuarios import admin_usuarios
    admin_usuarios()
