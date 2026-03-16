import streamlit as st
import pandas as pd
import login as lgn
from utils import logo_title, animaciones, menu
from mod_reportes import reportes
from permisos import tiene_permiso
from conexion_supabase import cargar_inventario, guardar_inventario
import io
from fpdf import FPDF
import plotly.express as px

st.set_page_config(
    page_title="S&G INVENTORY MANAGER",
    page_icon="🖥",
    layout="wide"
)

animaciones()
logo_title()

autenticado = lgn.user_password()
if not autenticado:
    st.stop()

opcion = menu(st.session_state["usuario"], st.session_state["rol"])

# --------------------------------------------------------
# ✅ INICIO
# --------------------------------------------------------
if opcion == "Inicio":
    st.header("🏠 Página Principal")

# --------------------------------------------------------
# ✅ INVENTARIO
# --------------------------------------------------------
elif opcion == "Inventario":

    usuario_actual = st.session_state["usuario"]
    rol = st.session_state["rol"]

    st.header(f"🖥 Inventario de {usuario_actual}")

    # ============================
    # ✅ Cargar inventario del usuario
    # ============================
    def cargar_inventario(usuario):
        try:
            df = pd.read_csv(f"inventario_{usuario}.csv")
            return df.to_dict(orient="records")
        except:
            return []

    # ============================
    # ✅ Guardar inventario del usuario
    # ============================
    def guardar_inventario(usuario, inventario):
        df = pd.DataFrame(inventario)
        df.to_csv(f"inventario_{usuario}.csv", index=False)

    # ✅ AQUÍ SE CREA LA VARIABLE inventario
    inventario = cargar_inventario(usuario_actual)

    # ============================
    # ✅ Tabs
    # ============================
    tab1, tab2, tab3, tab4 = st.tabs([
        "➕ Agregar producto",
        "🗑 Eliminar producto",
        "✏️ Actualizar producto",
        "📋 Consultar inventario"
    ])

    # --------------------------------------------------------
    # ✅ TAB 1 — Agregar producto
    # --------------------------------------------------------
    with tab1:
        if not tiene_permiso(rol, "inventario", "agregar"):
            st.warning("No tienes permiso para agregar productos.")
        else:
            nombre = st.text_input("Nombre del producto")
            marca = st.text_input("Marca del producto")
            cantidad = st.number_input("Cantidad", min_value=1, step=1)
            precio = st.number_input("Precio unitario", min_value=0.0, step=0.1)

            if st.button("Guardar", key="guardar_producto"):
                producto = {
                    "nombre": nombre.title().strip(),
                    "marca": marca.title().strip(),
                    "cantidad": cantidad,
                    "precio_unitario": precio,
                    "valor_total": round (cantidad * precio,2)
                }
                inventario.append(producto)
                guardar_inventario(usuario_actual, inventario)
                st.success(f"✅ Producto '{nombre}' agregado.")

    # --------------------------------------------------------
    # ✅ TAB 2 — Eliminar producto
    # --------------------------------------------------------
    with tab2:
        if not tiene_permiso(rol, "inventario", "eliminar"):
            st.warning("No tienes permiso para eliminar productos.")
        else:
            if inventario:
                nombres = [p["nombre"] for p in inventario]
                producto_sel = st.selectbox("Seleccione producto a eliminar", nombres)

                if st.button("Eliminar", key="eliminar_producto"):
                    inventario = [p for p in inventario if p["nombre"] != producto_sel]
                    guardar_inventario(usuario_actual, inventario)
                    st.success(f"✅ Producto '{producto_sel}' eliminado.")
            else:
                st.info("Inventario vacío.")

    # --------------------------------------------------------
    # ✅ TAB 3 — Actualizar producto
    # --------------------------------------------------------
    with tab3:
        if not tiene_permiso(rol, "inventario", "editar"):
            st.warning("No tienes permiso para editar productos.")
        else:
            if inventario:
                nombres = [p["nombre"] for p in inventario]
                producto_sel = st.selectbox("Seleccione producto a actualizar", nombres)

                producto = next((p for p in inventario if p["nombre"] == producto_sel), None)

                if producto:
                    nueva_cantidad = st.number_input("Nueva cantidad", value=producto["cantidad"], min_value=1)
                    nuevo_precio = st.number_input("Nuevo precio", value=producto["precio_unitario"], min_value=0.0)

                    if st.button("Actualizar", key="actualizar_producto"):
                        producto["cantidad"] = nueva_cantidad
                        producto["precio_unitario"] = nuevo_precio
                        producto["valor_total"] = round(nueva_cantidad * nuevo_precio, 2)
                        guardar_inventario(usuario_actual, inventario)
                        st.success(f"✅ Producto '{producto_sel}' actualizado.")
            else:
                st.info("Inventario vacío.")

    # --------------------------------------------------------
    # ✅ TAB 4 — Consultar inventario
    # --------------------------------------------------------
    with tab4:
        if not tiene_permiso(rol, "inventario", "ver"):
            st.warning("No tienes permiso para ver el inventario.")
        else:
            if inventario:
                st.table(inventario)
            else:
                st.info("Inventario vacío.")
# --------------------------------------------------------
# ✅ REPORTES
# --------------------------------------------------------
elif opcion == "Reportes":
    reportes(st.session_state["usuario"])
# --------------------------------------------------------
# ✅ COMPRAS
# --------------------------------------------------------
elif opcion == "Compras":
    st.header("🛒 Compras")
    # módulo de compras

# --------------------------------------------------------
# ✅ VENTAS
# --------------------------------------------------------
elif opcion == "Ventas":
    st.header("💰 Ventas")
    # módulo de ventas

# --------------------------------------------------------
# ✅ ADMINISTRACIÓN DE USUARIOS
# --------------------------------------------------------
elif opcion == "Administración de usuarios":
    rol = st.session_state["rol"]
    if not tiene_permiso(rol, "usuarios", "ver"):
        st.error("No tienes permisos para acceder a esta sección.")
    else:
        from admin_user import admin_usuarios
        admin_usuarios()











