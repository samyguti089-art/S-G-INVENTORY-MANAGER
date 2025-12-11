import streamlit as st
import pandas as pd
import login as lgn
from utils import logo_title, animaciones, menu

# Configuración de la página
st.set_page_config(
    page_title="S&G INVENTORY MANAGER",
    page_icon="🖥",
    layout="wide"
)

# Animaciones y logo
animaciones()
logo_title()

# Login
autenticado = lgn.user_password()

# Si no está autenticado, detener ejecución
if not autenticado:
    st.stop()

# ✅ AQUÍ VA EL MENÚ (ESTE ES EL LUGAR CORRECTO)
opcion = menu(st.session_state["usuario"], st.session_state["rol"])

# ✅ Cargar páginas según la opción seleccionada
if opcion == "Inicio":
    st.header("🏠 Página Principal")

elif opcion == "Inventario":
    st.header("📦 Inventario")
    # Aquí va tu módulo de inventario

elif opcion == "Reportes":
    st.header("📊 Reportes")
    # Aquí va tu módulo de reportes

elif opcion == "Compras":
    st.header("🛒 Compras")
    # Aquí va tu módulo de compras

elif opcion == "Ventas":
    st.header("💰 Ventas")
    # Aquí va tu módulo de ventas

elif opcion == "Administración de usuarios":
    from admin_usuarios import admin_usuarios
    admin_usuarios()
