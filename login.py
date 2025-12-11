import streamlit as st
from utils import menu, validar_usuario
import pandas as pd

def user_password():
    # Si ya está autenticado, mostrar menú
    if "usuario_autenticado" in st.session_state:
        st.success(f"Bienvenido {st.session_state['usuario_autenticado']}")
        menu(st.session_state["usuario_autenticado"])
        return True

    # Si NO está autenticado, mostrar login
    col1, col2, col3 = st.columns([2, 5, 2])

    with col1:
        # ✅ Fade-in correcto
        st.markdown('<div class="fade-in">', unsafe_allow_html=True)

        usuario = st.text_input("Usuario")
        clave = st.text_input("Clave", type="password")

        if st.button("Ingresar"):
            if validar_usuario(usuario, clave):
                st.session_state["usuario_autenticado"] = usuario
                st.rerun()
            else:
                st.error("Usuario o clave incorrectos")
                st.rerun()

        # ✅ Cierre correcto del div
        st.markdown('</div>', unsafe_allow_html=True)

    return False




        
