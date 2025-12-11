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
def logo_title():
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown('<div class="pulse">', unsafe_allow_html=True)
        st.image("logo.png", width=200)
        st.markdown('</div>', unsafe_allow_html=True)

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
# ✅ PERMISOS POR ROL (base para escalar)
# ============================================================
PERMISOS = {
    "admin": ["Inventario", "Ventas", "Compras", "Reportes"],
    "usuario": ["Inventario", "Reportes"],  # rol por defecto
    "vendedor": ["Inventario", "Ventas"],
    "auditor": ["Reportes"],
}


def seleccionar_usuario_para_admin(rol, usuario_actual):
    """
    Si es admin, puede elegir a qué usuario ver.
    Si no, siempre ve su propio inventario.
    """
    if rol != "admin":
        return usuario_actual

    if not os.path.exists("usuarios.csv"):
        return usuario_actual

    df = pd.read_csv("usuarios.csv", encoding="utf-8")
    if "usuario" not in df.columns:
        return usuario_actual

    usuarios = df["usuario"].dropna().unique().tolist()

    st.sidebar.markdown("---")
    usuario_objetivo = st.sidebar.selectbox(
        "👁️ Usuario a administrar:",
        usuarios,
        index=usuarios.index(usuario_actual) if usuario_actual in usuarios else 0
    )
    return usuario_objetivo


# ============================================================
# ✅ TARJETAS KPI ESTILO POWER BI
# ============================================================
def kpi_cards(df):
    if df.empty:
        st.info("No hay datos para mostrar KPIs.")
        return

    total_productos = len(df)
    valor_total = df["valor_total"].sum()
    precio_promedio = df["precio_unitario"].mean()
    total_marcas = df["marca"].nunique()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("📦 Total productos", total_productos)
    col2.metric("💰 Valor total", f"${valor_total:,.2f}")
    col3.metric("💲 Precio promedio", f"${precio_promedio:,.2f}")
    col4.metric("🏷️ Marcas únicas", total_marcas)


# ============================================================
# ✅ DASHBOARD AVANZADO ESTILO POWER BI
# ============================================================
def dashboard_graficos(inventario):

    if not inventario:
        st.info("No hay datos en el inventario para mostrar gráficos.")
        return

    st.subheader("📊 Dashboard Avanzado S&G (Estilo Power BI)")

    df = pd.DataFrame(inventario)

    # Asegurar columnas mínimas
    for col in ["nombre", "marca", "cantidad", "precio_unitario", "valor_total"]:
        if col not in df.columns:
            st.error(f"Falta la columna '{col}' en el inventario.")
            return

    # ✅ Tarjetas KPI
    kpi_cards(df)

    st.markdown("---")

    # ✅ Gráfico 1 — Barras horizontales (Top productos por valor)
    st.markdown("### 💰 Top productos por valor total")
    fig1 = px.bar(
        df.sort_values("valor_total", ascending=True),
        x="valor_total",
        y="nombre",
        orientation="h",
        color="valor_total",
        color_continuous_scale="Teal",
        title="Productos con mayor valor en inventario"
    )
    st.plotly_chart(fig1, use_container_width=True)

    # ✅ Gráfico 2 — Pie estilo donut
    st.markdown("### 🏷️ Distribución por marca")
    fig2 = px.pie(
        df,
        names="marca",
        values="cantidad",
        hole=0.4,
        color_discrete_sequence=px.colors.sequential.Blues,
        title="Participación por marca"
    )
    st.plotly_chart(fig2, use_container_width=True)

    # ✅ Gráfico 3 — Scatter profesional
    st.markdown("### 📈 Relación entre cantidad y precio unitario")
    fig3 = px.scatter(
        df,
        x="precio_unitario",
        y="cantidad",
        size="valor_total",
        color="marca",
        title="Relación entre precio y cantidad por producto",
        hover_name="nombre"
    )
    st.plotly_chart(fig3, use_container_width=True)

    # ✅ Gráfico 4 — Barras agrupadas por marca
    st.markdown("### 📊 Cantidad total por marca")
    df_marca = df.groupby("marca", as_index=False)["cantidad"].sum()
    fig4 = px.bar(
        df_marca,
        x="marca",
        y="cantidad",
        color="cantidad",
        color_continuous_scale="Blues",
        title="Cantidad total por marca"
    )
    st.plotly_chart(fig4, use_container_width=True)


# ============================================================
# ✅ MENÚ PRINCIPAL (CON INVENTARIO POR USUARIO)
# ============================================================
def menu(usuario, rol):

    # Determinar qué opciones ve según su rol
    opciones_permitidas = PERMISOS.get(rol, PERMISOS["usuario"])

    with st.sidebar:
        st.header(f"📦 Menú ({rol.upper()})")
        opcion = st.selectbox("Selecciona una opción:", opciones_permitidas)
        # Si es admin, puede elegir qué usuario ver
        usuario_objetivo = seleccionar_usuario_para_admin(rol, usuario)

    # Cargar inventario del usuario objetivo
    inventario = cargar_inventario_usuario(usuario_objetivo)

    # --------------------------------------------------------
    # ✅ INVENTARIO
    # --------------------------------------------------------
    if opcion == "Inventario":

        st.header(f"🖥 Inventario de {usuario_objetivo}")
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
                guardar_inventario_usuario(usuario_objetivo, inventario)
                st.success(f"✅ Producto '{nombre}' agregado al inventario de {usuario_objetivo}")

        # TAB 2 — Eliminar
        with tab2:
            if inventario:
                nombres = [p["nombre"] for p in inventario]
                producto_sel = st.selectbox("Seleccione producto a eliminar", nombres)
                if st.button("Eliminar", key="eliminar"):
                    inventario = [p for p in inventario if p["nombre"] != producto_sel]
                    guardar_inventario_usuario(usuario_objetivo, inventario)
                    st.success(f"Producto '{producto_sel}' eliminado del inventario de {usuario_objetivo}.")
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
                        guardar_inventario_usuario(usuario_objetivo, inventario)
                        st.success(f"Producto '{producto_sel}' actualizado en el inventario de {usuario_objetivo}.")
            else:
                st.info("Inventario vacío.")

        # TAB 4 — Consultar
        with tab4:
            if inventario:
                st.table(inventario)
            else:
                st.info("Inventario vacío.")

    # --------------------------------------------------------
    # ✅ REPORTES
    # --------------------------------------------------------
    if opcion == "Reportes":

        st.header(f"📊 Reportes de {usuario_objetivo}")
        tab_1, tab_2, tab_3 = st.tabs([
            "📥 Exportar a Excel",
            "📄 Exportar a PDF",
            "📈 Gráficas"
        ])

        # ✅ Exportar Excel
        with tab_1:
            if st.button("Exportar a Excel"):
                if inventario:
                    df = pd.DataFrame(inventario)
                    buffer = io.BytesIO()
                    df.to_excel(buffer, index=False, engine="openpyxl")
                    buffer.seek(0)

                    st.download_button(
                        label="📥 Descargar Excel",
                        data=buffer,
                        file_name=f"inventario_{usuario_objetivo}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                    st.success("✅ Inventario exportado a Excel")
                else:
                    st.info("No hay datos para exportar.")

        # ✅ Dashboard avanzado
        with tab_3:
            dashboard_graficos(inventario)

    # --------------------------------------------------------
    # ✅ BOTÓN SALIR
    # --------------------------------------------------------
    if st.button("Salir"):
        st.session_state.clear()
        st.rerun()




















