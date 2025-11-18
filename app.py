# app.py
# -*- coding: utf-8 -*-
"""
Streamlit app para el Sistema de Inventario Textil
Mantiene SQLite, todas las funciones (CRUD, stock, búsqueda combinada, gráficos, export).
Estilo: Dashboard moderno (sidebar navigation).
"""

import streamlit as st
from datetime import datetime
from io import BytesIO
import pandas as pd

# Importa tu lógica existente
from inventario import Inventario
from producto import Producto

# Utilidades de export (usa el export_utils.py que ya te di; si no existe lo implementé abajo)
try:
    from export_utils import export_to_csv, export_to_excel, export_to_pdf
except Exception:
    # fallback mínimo si no existe (crea CSV in-memory)
    import csv, os
    def export_to_csv(rows, path):
        with open(path, 'w', newline='', encoding='utf-8') as f:
            if not rows:
                f.write('')
                return True
            cols = list(rows[0].keys())
            import csv
            writer = csv.DictWriter(f, fieldnames=cols)
            writer.writeheader()
            writer.writerows(rows)
        return True

    def export_to_excel(rows, path):
        try:
            import pandas as pd
        except Exception:
            raise RuntimeError("Instala pandas+openpyxl para exportar Excel")
        df = pd.DataFrame(rows)
        df.to_excel(path, index=False)
        return True

    def export_to_pdf(rows, path):
        raise RuntimeError("Instala fpdf2 para exportar PDF")

# Librerías para gráficos: plotly preferente (interactivo)
HAS_PLOTLY = True
try:
    import plotly.express as px
except Exception:
    HAS_PLOTLY = False

# Instancia del inventario (usa la DB por defecto)
inv = Inventario()

# -----------------------------------
# Helpers: convertir listas de objetos a DataFrame / bytes
# -----------------------------------
def productos_to_df(productos):
    """Convierte lista de Producto a DataFrame"""
    rows = []
    for p in productos:
        rows.append({
            "ID": p.id,
            "Nombre": p.nombre,
            "TipoTela": p.tipo_tela,
            "Talla": p.talla,
            "Color": p.color,
            "Stock": p.cantidad
        })
    return pd.DataFrame(rows)

def df_to_csv_bytes(df):
    return df.to_csv(index=False).encode('utf-8')

def df_to_excel_bytes(df):
    out = BytesIO()
    with pd.ExcelWriter(out, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Inventario')
    out.seek(0)
    return out.getvalue()

def df_to_pdf_bytes(rows):
    """
    Crea un PDF in-memory usando fpdf2 si está disponible.
    Si no, lanza error para que el calling function muestre mensaje.
    """
    try:
        from fpdf import FPDF
    except Exception as e:
        raise RuntimeError("fpdf2 no instalado")
    pdf = FPDF(orientation='L', unit='mm', format='A4')
    pdf.set_auto_page_break(auto=True, margin=8)
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 8, txt="Inventario - Exportado: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"), ln=True)
    if not rows:
        pdf.ln(4)
        pdf.cell(0, 8, txt="No hay datos", ln=True)
        out = BytesIO()
        pdf.output(out)
        out.seek(0)
        return out.read()
    cols = list(rows[0].keys())
    page_width = 287
    col_w = max(20, int(page_width / max(1, len(cols))) - 4)
    # header
    pdf.set_font("Arial", "B", 10)
    for c in cols:
        pdf.cell(col_w, 8, txt=str(c), border=1, align='C')
    pdf.ln()
    # rows
    pdf.set_font("Arial", size=9)
    for r in rows:
        for c in cols:
            text = str(r.get(c, ""))
            if len(text) > 30:
                text = text[:27] + "..."
            pdf.cell(col_w, 8, txt=text, border=1)
        pdf.ln()
    out = BytesIO()
    pdf.output(out)
    out.seek(0)
    return out.read()

# -----------------------------------
# UI: Sidebar navigation
# -----------------------------------
st.set_page_config(page_title="Inventario Textil - Dashboard", layout="wide", initial_sidebar_state="expanded")
st.sidebar.title("Inventario Textil")
st.sidebar.caption("Dashboard — Gestión y reportes")

menu = st.sidebar.radio("Ir a", ["Dashboard", "Productos", "Búsqueda", "Estadísticas", "Historial", "Exportar", "Ajustes"])

# -----------------------------------
# Dashboard: resumen con KPIs y gráficos pequeños
# -----------------------------------
if menu == "Dashboard":
    st.title("📋 Dashboard — Inventario Textil")
    stats = inv.bd.estadisticas_generales()
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total productos", stats.get('total_productos', 0))
    col2.metric("Total unidades", stats.get('total_unidades', 0))
    col3.metric("Tipos de tela", stats.get('tipos_tela', 0))
    col4.metric("Productos sin stock", stats.get('sin_stock', 0))

    st.markdown("---")
    st.subheader("Últimos movimientos")
    hist = inv.bd.obtener_historial(limite=10)
    if hist:
        df_hist = pd.DataFrame(hist)
        st.dataframe(df_hist[['fecha','nombre','tipo_movimiento','cantidad','cantidad_anterior','cantidad_nueva']].rename(columns={
            'fecha':'Fecha','nombre':'Producto','tipo_movimiento':'Movimiento','cantidad':'Cant','cantidad_anterior':'Ant','cantidad_nueva':'Nueva'
        }))
    else:
        st.write("No hay movimientos registrados.")

    st.markdown("---")
    st.subheader("Gráficos rápidos")
    telas = inv.bd.resumen_por_tela()
    tallas = inv.bd.resumen_por_talla()
    df_telas = pd.DataFrame(telas, columns=['Tela','Total']) if telas else pd.DataFrame(columns=['Tela','Total'])
    df_tallas = pd.DataFrame(tallas, columns=['Talla','Total']) if tallas else pd.DataFrame(columns=['Talla','Total'])

    if HAS_PLOTLY:
        if not df_telas.empty:
            fig1 = px.bar(df_telas, x='Tela', y='Total', title='Stock por tela')
            st.plotly_chart(fig1, use_container_width=True)
        if not df_tallas.empty:
            fig2 = px.bar(df_tallas, x='Talla', y='Total', title='Stock por talla')
            st.plotly_chart(fig2, use_container_width=True)
    else:
        st.write("Instala plotly para gráficos interactivos (`pip install plotly`)")

# -----------------------------------
# Productos: CRUD UI
# -----------------------------------
elif menu == "Productos":
    st.title("📦 Productos — Agregar / Editar / Stock")
    with st.expander("➕ Agregar nuevo producto", expanded=True):
        with st.form("form_add"):
            nombre = st.text_input("Nombre")
            tipo_tela = st.selectbox("Tipo de tela", options=['','algodón','poliéster','lino','seda','denim','lycra'])
            talla = st.selectbox("Talla", options=['','XS','S','M','L','XL','XXL','28','30','32','34','36'])
            color = st.text_input("Color", value="N/A")
            cantidad = st.number_input("Cantidad inicial", min_value=0, value=0, step=1)
            submitted = st.form_submit_button("Agregar Producto")
            if submitted:
                if not nombre or not tipo_tela or not talla:
                    st.warning("Completa nombre, tipo de tela y talla.")
                else:
                    ok = inv.agregar_producto(nombre, tipo_tela, talla, int(cantidad), color)
                    if ok:
                        st.success("Producto agregado.")
                    else:
                        st.error("Error al agregar producto.")
    st.markdown("---")

    st.subheader("Editar / actualizar stock / eliminar")
    productos = inv.bd.obtener_todos(ordenar_por='nombre')
    df_prod = productos_to_df(productos)
    if df_prod.empty:
        st.info("No hay productos. Agrega uno primero.")
    else:
        # Selección de producto por ID
        sel_id = st.selectbox("Selecciona producto (ID) para editar/stock", options=[p.id for p in productos])
        p_obj = inv.bd.buscar_por_id(sel_id)
        if p_obj:
            colA, colB = st.columns([2,1])
            with colA:
                nombre_e = st.text_input("Nombre", value=p_obj.nombre, key="e_nombre")
                tela_e = st.selectbox("Tipo tela", options=['','algodón','poliéster','lino','seda','denim','lycra'], index=0, key="e_tela")
                # set current tela selection if present
                if p_obj.tipo_tela and tela_e == '':
                    # streamlit selectbox doesn't allow direct set, so show current value below for info
                    st.write("Tipo actual:", p_obj.tipo_tela)
                talla_e = st.selectbox("Talla", options=['','XS','S','M','L','XL','XXL','28','30','32','34','36'], index=0, key="e_talla")
                if p_obj.talla and talla_e == '':
                    st.write("Talla actual:", p_obj.talla)
                color_e = st.text_input("Color", value=p_obj.color, key="e_color")
            with colB:
                st.write("**Stock actual**")
                st.metric("Stock", p_obj.cantidad)
                add_qty = st.number_input("Aumentar / Reducir (positivo aumenta, negativo reduce)", value=0, step=1)
                if st.button("Aplicar ajuste"):
                    if add_qty > 0:
                        if inv.aumentar_stock(p_obj.id, int(add_qty)):
                            st.success("Stock aumentado")
                        else:
                            st.error("No fue posible aumentar stock")
                    elif add_qty < 0:
                        if inv.reducir_stock(p_obj.id, int(abs(add_qty))):
                            st.success("Stock reducido")
                        else:
                            st.error("No fue posible reducir stock")
                    st.experimental_rerun()
                if st.button("Eliminar producto"):
                    if st.confirm("Confirmar eliminación", f"¿Eliminar producto ID {p_obj.id}?"):
                        if inv.eliminar_producto(p_obj.id):
                            st.success("Producto eliminado")
                            st.experimental_rerun()
                        else:
                            st.error("No se pudo eliminar")

            if st.button("Guardar cambios en producto"):
                # usar valores no vacíos; si user no selecciona tela/talla, mantiene valores previos
                new_tela = tela_e if tela_e else p_obj.tipo_tela
                new_talla = talla_e if talla_e else p_obj.talla
                # if nombre empty keep old
                new_nombre = nombre_e if nombre_e else p_obj.nombre
                if inv.editar_producto(p_obj.id, new_nombre, new_tela, new_talla, color_e):
                    st.success("Producto actualizado")
                    st.experimental_rerun()
                else:
                    st.error("No se pudo actualizar")

    st.markdown("---")
    st.subheader("Todos los productos")
    st.dataframe(df_prod)

# -----------------------------------
# Búsqueda: filtros combinados
# -----------------------------------
elif menu == "Búsqueda":
    st.title("🔍 Búsqueda combinada")
    with st.form("form_search"):
        tela = st.selectbox("Tipo de tela", options=['', 'algodón','poliéster','lino','seda','denim','lycra'])
        talla = st.selectbox("Talla", options=['', 'XS','S','M','L','XL','XXL','28','30','32','34','36'])
        stock_min = st.text_input("Stock mínimo (opcional)")
        submitted = st.form_submit_button("Buscar")
        if submitted:
            stock_val = None
            if stock_min.strip() != "":
                try:
                    stock_val = int(stock_min)
                except ValueError:
                    st.error("Stock mínimo debe ser entero")
                    stock_val = None
            results = inv.bd.buscar_combinado(tipo_tela=(tela or None), talla=(talla or None), stock_minimo=stock_val)
            df_r = productos_to_df(results)
            st.success(f"Se encontraron {len(results)} resultados")
            st.dataframe(df_r)
            # boton de descarga de resultados como CSV
            csv_bytes = df_to_csv_bytes(df_r)
            st.download_button("📥 Descargar resultados CSV", data=csv_bytes, file_name="resultados_busqueda.csv", mime="text/csv")

# -----------------------------------
# Estadísticas: gráficos completos
# -----------------------------------
elif menu == "Estadísticas":
    st.title("📊 Estadísticas & Gráficos")
    st.markdown("Calcula y muestra gráficos interactivos del inventario.")
    stats = inv.bd.estadisticas_generales()
    st.metric("Total productos", stats.get('total_productos',0))
    st.metric("Total unidades", stats.get('total_unidades',0))
    st.metric("Tipos de tela", stats.get('tipos_tela',0))
    st.metric("Sin stock", stats.get('sin_stock',0))

    # Data para graficar
    df_telas = pd.DataFrame(inv.bd.resumen_por_tela(), columns=['Tela','Total']) if inv.bd.resumen_por_tela() else pd.DataFrame(columns=['Tela','Total'])
    df_tallas = pd.DataFrame(inv.bd.resumen_por_talla(), columns=['Talla','Total']) if inv.bd.resumen_por_talla() else pd.DataFrame(columns=['Talla','Total'])

    if HAS_PLOTLY:
        if not df_telas.empty:
            fig = px.pie(df_telas, names='Tela', values='Total', title='Proporción por Tipo de Tela')
            st.plotly_chart(fig, use_container_width=True)
        if not df_tallas.empty:
            fig2 = px.bar(df_tallas, x='Talla', y='Total', title='Stock por Talla')
            st.plotly_chart(fig2, use_container_width=True)
    else:
        st.warning("Instala plotly para ver gráficos interactivos: pip install plotly")

# -----------------------------------
# Historial
# -----------------------------------
elif menu == "Historial":
    st.title("📜 Historial de movimientos")
    filtro_id = st.text_input("Filtrar por ID de producto (opcional)")
    try:
        limite = int(st.sidebar.number_input("Limite de registros", value=200, min_value=10, max_value=1000))
    except Exception:
        limite = 200

    if filtro_id.strip():
        try:
            pid = int(filtro_id)
            hist = inv.bd.obtener_historial(producto_id=pid, limite=limite)
            st.subheader(f"Historial producto ID {pid}")
        except ValueError:
            st.error("ID inválido")
            hist = []
    else:
        hist = inv.bd.obtener_historial(limite=limite)
        st.subheader(f"Últimos {len(hist)} movimientos")
    if hist:
        df_hist = pd.DataFrame(hist)
        st.dataframe(df_hist)
    else:
        st.info("No hay movimientos")

# -----------------------------------
# Exportar: exportaciones completas
# -----------------------------------
elif menu == "Exportar":
    st.title("📤 Exportar Inventario")
    st.markdown("Exporta inventario completo a CSV / Excel / PDF.")
    productos = inv.bd.obtener_todos(ordenar_por='nombre')
    df_prod = productos_to_df(productos)
    st.dataframe(df_prod)

    col1, col2, col3 = st.columns(3)
    with col1:
        csv_bytes = df_to_csv_bytes(df_prod)
        st.download_button("📥 Descargar CSV", data=csv_bytes, file_name="inventario.csv", mime="text/csv")
    with col2:
        # Excel
        try:
            excel_bytes = df_to_excel_bytes(df_prod)
            st.download_button("📥 Descargar Excel (.xlsx)", data=excel_bytes, file_name="inventario.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        except Exception as e:
            st.warning("Para exportar Excel instala pandas + openpyxl (pip install pandas openpyxl)")
    with col3:
        # PDF
        try:
            rows = df_prod.to_dict(orient='records')
            pdf_bytes = df_to_pdf_bytes(rows)
            st.download_button("📥 Descargar PDF", data=pdf_bytes, file_name="inventario.pdf", mime="application/pdf")
        except Exception as e:
            st.warning("Para exportar PDF instala fpdf2 (pip install fpdf2)")

# -----------------------------------
# Ajustes / About
# -----------------------------------
elif menu == "Ajustes":
    st.title("⚙️ Ajustes")
    st.markdown("""
    **Opciones**
    - Base de datos: SQLite (archivo en `datos/inventario.db`)
    - Export: CSV / Excel (pandas+openpyxl) / PDF (fpdf2)
    - Gráficos: plotly (recomendado)
    """)
    if st.button("Crear respaldo de la BD ahora"):
        ok = inv.bd.crear_respaldo()
        if ok:
            st.success("Respaldo creado en carpeta datos/")
        else:
            st.error("No fue posible crear respaldo")

# -----------------------------------
# Fin
# -----------------------------------
