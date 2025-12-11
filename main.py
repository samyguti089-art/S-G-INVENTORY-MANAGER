import streamlit as st
import pandas as pd
import login as lgn
from utils import logo_title, animaciones, menu

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
    st.header(f"🖥 Inventario de {st.session_state['usuario']}")
    tab1, tab2, tab3, tab4 = st.tabs([
            "➕ Agregar producto",
            "🗑 Eliminar producto",
            "✏️ Actualizar producto",
            "📋 Consultar inventario"
        ])

        # TAB 1 — Agregar
        with tab1:
            nombre = st.text_input("Nombre del producto")
            marca = st.text_input("Marca del producto")
            cantidad = st.number_input("Cantidad", min_value=1, step=1)
            precio = st.number_input("Precio unitario", min_value=0.0, step=0.1)

            if st.button("Guardar", key="guardar"):
                producto = {
                    "nombre": nombre.title().strip(),
                    "marca": marca.title().strip(),
                    "cantidad": cantidad,
                    "precio_unitario": precio,
                    "valor_total": cantidad * precio
                }
                inventario.append(producto)
                guardar_inventario_usuario(usuario, inventario)
                st.success(f"✅ Producto '{nombre}' agregado al inventario de {usuario}")
        with tab2:
            if inventario:
                nombres = [p["nombre"] for p in inventario]
                producto_sel = st.selectbox("Seleccione producto a eliminar", nombres)
                if st.button("Eliminar", key="eliminar"):
                    inventario = [p for p in inventario if p["nombre"] != producto_sel]
                    guardar_inventario_usuario(usuario, inventario)
                    st.success(f"Producto '{producto_sel}' eliminado del inventario de {usuario}.")
            else:
                st.info("Inventario vacío.")

        # TAB 3 — Actualizar
        with tab3:
            if inventario:
                nombres = [p["nombre"] for p in inventario]
                producto_sel = st.selectbox("Seleccione producto a actualizar", nombres)
                producto = next((p for p in inventario if p["nombre"] == producto_sel), None)

                if producto:
                    nueva_cantidad = st.number_input("Nueva cantidad", value=producto["cantidad"], min_value=1)
                    nuevo_precio = st.number_input("Nuevo precio", value=producto["precio_unitario"], min_value=0.0)

                    if st.button("Actualizar", key="actualizar"):
                        producto["cantidad"] = nueva_cantidad
                        producto["precio_unitario"] = nuevo_preccio = nuevo_precio
                        producto["valor_total"] = nueva_cantidad * nuevo_precio
                        guardar_inventario_usuario(usuario, inventario)
                        st.success(f"Producto '{producto_sel}' actualizado en el inventario de {usuario}.")
            else:
                st.info("Inventario vacío.")

        # TAB 4 — Consultar
        with tab4:
            if inventario:
                st.table(inventario)
            else:
                st.info("Inventario vacío.")
    # aquí copiaremos la lógica de tabs que tenías,
    # pero ya fuera de utils y sin usar usuario_objetivo “mágico”

# --------------------------------------------------------
# ✅ REPORTES
# --------------------------------------------------------
elif opcion == "Reportes":
    st.header(f"📊 Reportes de {st.session_state['usuario']}")
    # aquí colocas tus tabs de reportes

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
    from admin_usuarios import admin_usuarios
    admin_usuarios()
