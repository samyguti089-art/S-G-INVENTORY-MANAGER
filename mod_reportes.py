import streamlit as st
import pandas as pd
import plotly.express as px
import io
from fpdf import FPDF
from permisos import tiene_permiso


# ============================================================
# ✅ TARJETAS KPI
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

    # ✅ Gráfico 1 — Barras horizontales
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

    # ✅ Gráfico 3 — Scatter
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

    # ✅ Gráfico 4 — Barras agrupadas
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
# ✅ MÓDULO PRINCIPAL DE REPORTES
# ============================================================
def reportes(usuario_actual):
    rol = st.session_state["rol"]
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
        "📈 Dashboard"
    ])

    # --------------------------------------------------------
    # ✅ TAB 1 — Exportar a Excel
    # --------------------------------------------------------
    with tab1:
        if not tiene_permiso(rol, "reportes", "exportar"):
            st.warning("No tienes permiso para exportar a Excel.")
        else:

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
        if not tiene_permiso(rol, "reportes", "exportar"):
            st.warning("No tienes permiso para exportar a PDF.")
        else:

            st.subheader("📄 Exportar inventario a PDF")
    
            if df.empty:
                st.info("No hay datos para exportar.")
            else:
                if st.button("Generar PDF"):
                    pdf = FPDF()
                    pdf.add_page()
                    pdf.set_font("Arial", size=12)
    
                    pdf.cell(200, 10, txt=f"Inventario de {usuario_actual}", ln=True, align="C")
                    pdf.ln(10)
    
                    for index, row in df.iterrows():
                        pdf.cell(
                            200,
                            8,
                            txt=f"{row['nombre']} - {row['marca']} - Cant: {row['cantidad']} - Precio: {row['precio_unitario']}",
                            ln=True
                        )
    
                    pdf_output = pdf.output(dest="S").encode("latin1")
    
                    st.download_button(
                        label="📄 Descargar PDF",
                        data=pdf_output,
                        file_name=f"inventario_{usuario_actual}.pdf",
                        mime="application/pdf"
                    )

    # --------------------------------------------------------
    # ✅ TAB 3 — Dashboard Avanzado
    # --------------------------------------------------------
    with tab3:
        if not tiene_permiso(rol, "reportes", "dashboard"):
            st.warning("No tienes permiso para ver el dashboard.")
        else:
            dashboard_graficos(df.to_dict(orient="records"))
