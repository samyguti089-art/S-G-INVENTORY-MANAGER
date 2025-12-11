import streamlit as st
import pandas as pd
import json
import os
import io
import plotly.express as px


# ============================================================
# ✅ ANIMACIONES Y ESTILO CORPORATIVO S&G
# ============================================================
def animaciones():
    st.markdown("""
    <style>

    /* ✅ Fondo animado sci‑fi */
    html, body, .stApp {
        background: linear-gradient(-45deg, #0a0f1f, #0d1b2a, #1b263b, #415a77);
        background-size: 400% 400%;
        animation: gradientBG 12s ease infinite !important;
        color: #e0e6ed;
        font-family: 'Segoe UI', sans-serif;
    }

    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* ✅ Fade-in general */
    .fade-in {
        opacity: 0;
        animation: fadeIn 1.2s ease-in forwards;
    }

    @keyframes fadeIn {
        to { opacity: 1; }
    }

    /* ✅ Pulso del logo */
    .pulse {
        animation: pulse 1.5s ease-in-out infinite;
    }

    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }

    /* ✅ Inputs */
    input:focus, textarea:focus {
        border-color: #00bcd4 !important;
        box-shadow: 0 0 5px rgba(0, 188, 212, 0.5) !important;
        transition: all 0.3s ease;
    }

    /* ✅ Botones */
    .stButton > button {
        transition: all 0.3s ease;
        border-radius: 6px;
        background-color: #1b263b !important;
        color: #e0e6ed !important;
        border: 1px solid #415a77 !important;
        font-weight: 600;
    }

    .stButton > button:hover {
        transform: scale(1.05);
        background-color: #00bcd4 !important;
        color: white !important;
        border-color: #00bcd4 !important;
        box-shadow: 0 0 12px rgba(0, 188, 212, 0.6);
    }

    /* ✅ Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #0d1b2a !important;
        border-right: 1px solid #415a77;
        box-shadow: 4px 0 12px rgba(0,0,0,0.4);
    }

    </style>
    """, unsafe_allow_html=True)


# ============================================================
# ✅ LOGO Y TÍTULO
# ============================================================
def logo_title ():
# Crear columnas: una angosta para el logo y otra para el título
   col1, col2 = st.columns([1, 5])
   with col1:
    st.image("logo.png", width=200)  # ajusta el tamaño
   with col2:
    st.title("S&G Inventory Manager")



# ============================================================
# ✅ VALIDACIÓN DE USUARIO BÁSICA (CSV)
#    (versión simple, sin hash aún)
# ============================================================
def validar_usuario(usuario, clave):
    dfusuarios = pd.read_csv("usuarios.csv", encoding="utf-8")

    dfusuarios.columns = dfusuarios.columns.str.strip()
    dfusuarios = dfusuarios.applymap(lambda x: x.strip().lower() if isinstance(x, str) else x)

    usuario = usuario.strip().lower()
    clave = clave.strip().lower()

    fila = dfusuarios[
        (dfusuarios["usuario"] == usuario) &
        (dfusuarios["clave"] == clave)
    ]

    if fila.empty:
        return False, None

    # Si más adelante agregas columna "rol", la usamos
    rol = fila.iloc[0]["rol"] if "rol" in fila.columns else "usuario"
    return True, rol


# ============================================================
# ✅ RUTAS E INVENTARIO POR USUARIO
# ============================================================
def ruta_inventario(usuario):
    os.makedirs("inventarios", exist_ok=True)
    return os.path.join("inventarios", f"{usuario}.json")


def cargar_inventario_usuario(usuario):
    archivo = ruta_inventario(usuario)
    if os.path.exists(archivo):
        with open(archivo, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def guardar_inventario_usuario(usuario, inventario):
    archivo = ruta_inventario(usuario)
    with open(archivo, "w", encoding="utf-8") as f:
        json.dump(inventario, f, indent=4, ensure_ascii=False)

# ============================================================
# ✅ MENÚ PRINCIPAL (CON INVENTARIO POR USUARIO)
# ============================================================
import streamlit as st

def menu(usuario, rol):

    st.sidebar.title("📌 Menú principal")
    st.sidebar.markdown(f"👤 **Usuario:** {usuario}")
    st.sidebar.markdown(f"🔑 **Rol:** {rol.upper()}")

    opciones = ["Inicio"]

    if tiene_permiso(rol, "inventario", "ver"):
        opciones.append("Inventario")

    if tiene_permiso(rol, "reportes", "ver"):
        opciones.append("Reportes")

    if tiene_permiso(rol, "compras", "ver"):
        opciones.append("Compras")

    if tiene_permiso(rol, "ventas", "ver"):
        opciones.append("Ventas")

    if tiene_permiso(rol, "usuarios", "ver"):
        opciones.append("Administración de usuarios")

    opcion = st.sidebar.selectbox(
        "Selecciona una opción",
        opciones,
        key="menu_principal"
    )

    if st.sidebar.button("Cerrar sesión", key="logout_btn"):
        st.session_state.clear()
        st.rerun()

    return opcion

   

    # --------------------------------------------------------
    # ✅ BOTÓN SALIR
    # --------------------------------------------------------
    if st.button("Salir"):
        st.session_state.clear()
        st.rerun()





































