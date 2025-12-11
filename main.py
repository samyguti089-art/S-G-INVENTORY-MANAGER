import streamlit as st
import pandas as pd
import login as lgn
from utils import logo_title, animaciones, menu
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
                "valor_total": cantidad * precio
            }
            inventario.append(producto)
            guardar_inventario(usuario_actual, inventario)
            st.success(f"✅ Producto '{nombre}' agregado.")

    # --------------------------------------------------------
    # ✅ TAB 2 — Eliminar producto
    # --------------------------------------------------------
    with tab2:
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
                    producto["valor_total"] = nueva_cantidad * nuevo_precio
                    guardar_inventario(usuario_actual, inventario)
                    st.success(f"✅ Producto '{producto_sel}' actualizado.")
        else:
            st.info("Inventario vacío.")

    # --------------------------------------------------------
    # ✅ TAB 4 — Consultar inventario
    # --------------------------------------------------------
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

    usuario_actual = st.session_state["usuario"]
    st.header(f"📊 Reportes de {usuario_actual}")

    # ============================
    # ✅ Cargar inventario del usuario
    # ============================
    def cargar_inventario(usuario):
        try:
            df = pd.read_csv(f"inventario_{usuario}.csv")
            return df
        except:
            return pd.DataFrame()

    df = cargar_inventario(usuario_actual)

    # ============================
    # ✅ Tabs de reportes
    # ============================
    tab1, tab2, tab3 = st.tabs([
        "📥 Exportar a Excel",
        "📄 Exportar a PDF",
        "📈 Gráficas"
    ])

    # --------------------------------------------------------
    # ✅ TAB 1 — Exportar a Excel
    # --------------------------------------------------------
    with tab1:
        st.subheader("📥 Exportar inventario a Excel")

        if df.empty:
            st.info("No hay datos para exportar.")
        else:
            buffer = io.BytesIO()
            df.to_excel(buffer, index=False, engine="openpyxl")
            buffer.seek(0)

            st.download_button(
                label="📥 Descargar Excel",
                data=buffer,
                file_name=f"inventario_{usuario_actual}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    # --------------------------------------------------------
    # ✅ TAB 2 — Exportar a PDF
    # --------------------------------------------------------
    with tab2:
        st.subheader("📄 Exportar inventario a PDF")

        if df.empty:
            st.info("No hay datos para exportar.")
        else:
            from fpdf import FPDF

            if st.button("Generar PDF"):
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=12)

                pdf.cell(200, 10, txt=f"Inventario de {usuario_actual}", ln=True, align="C")
                pdf.ln(10)

                for index, row in df.iterrows():
                    pdf.cell(200, 8, txt=f"{row['nombre']} - {row['marca']} - Cant: {row['cantidad']} - Precio: {row['precio_unitario']}", ln=True)

                pdf_output = pdf.output(dest="S").encode("latin1")

                st.download_button(
                    label="📄 Descargar PDF",
                    data=pdf_output,
                    file_name=f"inventario_{usuario_actual}.pdf",
                    mime="application/pdf"
                )

    # --------------------------------------------------------
    # ✅ TAB 3 — Dashboard de gráficas
    # --------------------------------------------------------
    with tab3:
        st.subheader("📈 Dashboard de Inventario")

        if df.empty:
            st.info("No hay datos para graficar.")
        else:
            import plotly.express as px

            # Valor total por producto
            fig1 = px.bar(
                df,
                x="nombre",
                y="valor_total",
                title="Valor total por producto",
                text="valor_total"
            )
            st.plotly_chart(fig1, use_container_width=True)

            # Cantidad por producto
            fig2 = px.pie(
                df,
                names="nombre",
                values="cantidad",
                title="Distribución de cantidades"
            )
            st.plotly_chart(fig2, use_container_width=True)

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
    from admin_user import admin_usuarios
    admin_user()





