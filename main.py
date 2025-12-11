import streamlit as st
import pandas as pd
import login as lgn
from utils import logo_title

# Configuración de la página (debe ir primero)
st.set_page_config(
    page_title="S&G INVENTORY MANAGER",
    page_icon="🖥",
    layout="wide"
)

# Encabezado principal
st.header('Página :blue[Principal]')

# Llamada al login
lgn.user_password()

# Mostrar logo y título
logo_title()

