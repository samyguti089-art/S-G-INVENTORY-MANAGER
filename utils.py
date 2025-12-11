import streamlit as st
import pandas as pd
import json
import os
import io


def animaciones ():
    st.markdown("""
<style>

/* ✅ Fondo animado sci‑fi */
html, body, .stApp {
    background: linear-gradient(-45deg, #0a0f1f, #0d1b2a, #1b263b, #415a77);
    background-size: 400% 400%;
    animation: gradientBG 12s ease infinite !important;
}

@keyframes gradientBG {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* ✅ Fondo transparente para el contenedor principal */
.main {
    background: transparent !important;
}

/* ✅ Fade-in */
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

/* ✅ Inputs con efecto */
input:focus {
    border-color: #00bcd4 !important;
    box-shadow: 0 0 5px rgba(0, 188, 212, 0.5) !important;
    transition: all 0.3s ease;
}

/* ✅ Botón de Streamlit */
.stButton > button {
    transition: all 0.3s ease;
    border-radius: 6px;
}

/* ✅ Hover visible y elegante */
.stButton > button:hover {
    transform: scale(1.05);
    background-color: #00bcd4 !important;
    color: white !important;
    border-color: #00bcd4 !important;
}

</style>
""", unsafe_allow_html=True)

def logo_title ():
# Crear columnas: una angosta para el logo y otra para el título
   col1, col2 = st.columns([1, 5])
   with col1:
    st.image("logo.png", width=200)  # ajusta el tamaño
   with col2:
    st.title("S&G Inventory Manager")


def validar_usuario(usuario, clave):
    dfusuarios = pd.read_csv("usuarios.csv", encoding="utf-8")
    # Normalizar columnas y valores
    dfusuarios.columns = dfusuarios.columns.str.strip()
    dfusuarios = dfusuarios.applymap(lambda x: x.strip().lower() if isinstance(x, str) else x)
    # Normalizar también lo que ingresa el usuario
    usuario = usuario.strip().lower()
    clave = clave.strip().lower()
    return len(dfusuarios[(dfusuarios['usuario'] == usuario) & (dfusuarios['clave'] == clave)]) > 0
  


def cargar_inventario(archivo="inventario.json"):
    if os.path.exists(archivo):
        with open(archivo, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def guardar_inventario(inventario, archivo="inventario.json"):
    with open(archivo, "w", encoding="utf-8") as f:
        json.dump(inventario, f, indent=4, ensure_ascii=False)

def menu(usuario):
    with st.sidebar:
        st.header("📦 Menú Principal")
        opcion = st.selectbox("Selecciona una opción:", ["Inventario", "Ventas", "Compras", "Reportes"])
        st.write(f"Has elegido: {opcion}")

    if opcion == "Inventario":
        st.header("🖥 Inventario")

        # 👉 Crear pestañas
        tab1, tab2, tab3, tab4 = st.tabs([
            "➕ Agregar producto",
            "🗑 Eliminar producto",
            "✏️ Actualizar producto",
            "📋 Consultar inventario"
        ])

        inventario = cargar_inventario()

        # --- TAB 1: Agregar producto ---
        with tab1:
            nombre = st.text_input("Nombre del producto")
            marca= st.text_input("marca del prodcuto")
            cantidad = st.number_input("Cantidad", min_value=1, step=1)
            precio = st.number_input("Precio unitario", min_value=0.0, step=0.1)

            if st.button("Guardar", key="guardar"):
                producto = {
                    "nombre":nombre.title().strip(),
                    "marca":marca.title().strip(),
                    "cantidad": cantidad,
                    "precio_unitario": precio,
                    "valor_total": cantidad * precio
                }
                inventario.append(producto)
                guardar_inventario(inventario)
                st.success(f"✅ Producto '{nombre}' agregado al inventario")

        # --- TAB 2: Eliminar producto ---
        with tab2:
            if inventario:
                nombres = [p["nombre"] for p in inventario]
                producto_sel = st.selectbox("Seleccione producto a eliminar", nombres)
                if st.button("Eliminar", key="eliminar"):
                    inventario = [p for p in inventario if p["nombre"] != producto_sel]
                    guardar_inventario(inventario)
                    st.success(f"Producto '{producto_sel}' eliminado.")
            else:
                st.info("Inventario vacío.")

        # --- TAB 3: Actualizar producto ---
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
                        producto["precio_unitario"] = nuevo_precio
                        producto["valor_total"] = nueva_cantidad * nuevo_precio
                        guardar_inventario(inventario)
                        st.success(f"Producto '{producto_sel}' actualizado.")
            else:
                st.info("Inventario vacío.")

        # --- TAB 4: Consultar inventario ---
        with tab4:
            if inventario:
                st.table(inventario)
            else:
                st.info("Inventario vacío.")
    if opcion == "Reportes":
        st.header("🖥 reportes")
        tab_1, tab_2,tab_3  = st.tabs([
            "exportar a excel",
            "exportar a pdf ",
            "graficas"   
        ])
    
        inventario = cargar_inventario()

        with tab_1:
         exportar_excel = st.button("Exportar a Excel")

        if exportar_excel:
        # Convertir inventario a DataFrame
         df = pd.DataFrame(inventario)

        # Crear un buffer en memoria
         buffer = io.BytesIO()
         df.to_excel(buffer, index=False, engine="openpyxl")
         buffer.seek(0)  # Volver al inicio del buffer

        # Botón de descarga
         st.download_button(
            label="📥 Descargar Excel",
            data=buffer,
            file_name="inventario.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
         st.success("✅ Inventario exportado a Excel")
        with tab_3 :
             if inventario:
                dashboard_graficos(inventario)
            def dashboard_graficos(inventario):

                st.subheader("📊 Dashboard Corporativo S&G")
    
                df = pd.DataFrame(inventario)
            
                # ✅ Gráfico 1: Cantidad por producto
                st.markdown("### 📦 Cantidad por producto")
                fig1 = px.bar(
                    df,
                    x="nombre",
                    y="cantidad",
                    color="cantidad",
                    color_continuous_scale="Blues",
                    title="Cantidad disponible por producto"
                )
                st.plotly_chart(fig1, use_container_width=True)
            
                # ✅ Gráfico 2: Valor total por producto
                st.markdown("### 💰 Valor total por producto")
                fig2 = px.bar(
                    df,
                    x="nombre",
                    y="valor_total",
                    color="valor_total",
                    color_continuous_scale="Teal",
                    title="Valor total del inventario por producto"
                )
                st.plotly_chart(fig2, use_container_width=True)
            
                # ✅ Gráfico 3: Distribución por marca
                st.markdown("### 🏷️ Distribución por marca")
                fig3 = px.pie(
                    df,
                    names="marca",
                    values="cantidad",
                    title="Participación por marca"
                )
                st.plotly_chart(fig3, use_container_width=True)
            else:
                st.info("No hay datos en el inventario para mostrar gráficos.")

    # Botón salir
    btn_salir = st.button("Salir")
    if btn_salir:
        st.session_state.clear()
        st.rerun()















