import streamlit as st
import pandas as pd
import bcrypt
from utils import menu


# ============================================================
# ✅ Cargar usuarios desde CSV
# ============================================================
def cargar_usuarios():
    df = pd.read_csv("usuarios.csv", encoding="utf-8")
    df.columns = df.columns.str.strip()
    return df


# ============================================================
# ✅ Verificar contraseña con bcrypt
# ============================================================
def verificar_password(password_plano, password_hash):
    try:
        return bcrypt.checkpw(password_plano.encode("utf-8"), password_hash.encode("utf-8"))
    except:
        return False


# ============================================================
# ✅ Validar usuario con hash y rol
# ============================================================
def validar_usuario_hash(usuario, clave):
    df = cargar_usuarios()

    usuario = usuario.strip().lower()

    fila = df[df["usuario"].str.lower() == usuario]

    if fila.empty:
        return False, None

    password_hash = fila.iloc[0]["clave_hash"]
    rol = fila.iloc[0]["rol"]

    if verificar_password(clave, password_hash):
        return True, rol

    return False, None


# ============================================================
# ✅ Pantalla de Login (RESPETA TU ESTRUCTURA ORIGINAL)
# ============================================================
def user_password():

    # Si ya está autenticado, entrar directo
    if st.session_state.get("autenticado", False):
        menu(st.session_state["usuario"], st.session_state["rol"])
        return True
    col1, col2, col3 = st.columns([2, 5, 2])  # Ajusta proporciones si quieres moverlo más

    with col1:     

        st.subheader("🔐 Inicio de sesión")
    
        usuario = st.text_input("Usuario")
        clave = st.text_input("Contraseña", type="password")

    if st.button("Ingresar"):

        autenticado, rol = validar_usuario_hash(usuario, clave)

        if autenticado:

            # Guardar sesión
            st.session_state["usuario"] = usuario
            st.session_state["rol"] = rol
            st.session_state["autenticado"] = True

            st.success(f"✅ Bienvenido {usuario} — Rol: {rol.upper()}")
            st.rerun()

        else:
            st.error("❌ Usuario o contraseña incorrectos")

    return False




        



