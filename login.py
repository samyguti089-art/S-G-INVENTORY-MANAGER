import streamlit as st
from utils import menu,validar_usuario
import pandas as pd

def user_password():
    # Usar siempre la misma clave en session_state
    if "usuario_autenticado" in st.session_state:
        st.success(f"Bienvenido {st.session_state['usuario_autenticado']}")
        menu(st.session_state["usuario_autenticado"])
    else:
        col1, col2, col3 = st.columns([2, 5, 2])  # Ajusta proporciones si quieres moverlo más

        with col1:
            st.markdown("### 🔐 Iniciar sesión")
            usuario = st.text_input("Usuario")
            clave = st.text_input("Clave", type="password")
            if st.button("Ingresar"):
                if validar_usuario(usuario, clave):
                    st.session_state["usuario_autenticado"] = usuario
                    st.rerun()  # recarga la app para ocultar login
                else:
                    st.error("Usuario o clave incorrectos")
                    st.rerun()
                    


        