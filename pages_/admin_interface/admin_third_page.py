import streamlit as st
import pandas as pd

# define the function to the third page of the admin interface and be called in the main file
def admin_third_page(df_inventario):
    st.logo(
        "danu.png",
        icon_image="logo_copy.png",
        size="large"
    )

    if st.sidebar.button("Logout", key="admin_logout_button_3"):
        st.session_state.authenticated = False
        st.success("Logout successful")

    # Filtrar ciudades no deseadas
    df_inventario = df_inventario[~df_inventario["City"].isin([
        "Alnwick", "Blackpool", "Hornsea", "Cardiff", "Leeds", "West Bromwich",
        "Banbury", "Lundy", "Oldham", "Barrow-in-Furness", "Winterton"
    ])]

    st.markdown("<h1 style='text-align: center;'>Consulta tu Inventario Actual</h1>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # Crear columnas para organizar layout
    content_col, filter_col = st.columns([3, 1], gap="medium")

    # Filtros en la barra lateral
    with filter_col:
        # País
        if st.session_state.username == "admin":
            pais = st.selectbox("País", ["Todos"] + sorted(list(df_inventario['Country'].unique())))
            df_pais_selec_i = df_inventario if pais == "Todos" else df_inventario[df_inventario['Country'] == pais]
        else:
            df_pais_selec_i = df_inventario[df_inventario['Country'] == "Escocia"]

        # Ciudad
        ciudad = st.selectbox("Ciudad", ["Todas"] + sorted(list(df_pais_selec_i['City'].unique())))
        df_final_ciudad = df_pais_selec_i if ciudad == "Todas" else df_pais_selec_i[df_pais_selec_i['City'] == ciudad]

        #  Inventario Recomendado mínimo
        inventario_optimo_min = st.number_input("Inventario recomendado en relación al año pasado", min_value=0.1, value=1.0, step=0.1)

    # Eliminar filas con datos nulos
    df_final_ciudad = df_final_ciudad.dropna()

    acumulados = df_final_ciudad.groupby('Types').agg({
        'SalesQuantity': 'sum',
        'In Stock': 'sum'
    }).reset_index()

    # Datos y cálculos adicionales
    acumulados['SalesQuantity'] = acumulados['SalesQuantity'].astype(int)
    acumulados['In Stock'] = acumulados['In Stock'].astype(int)
    acumulados['Inventory Coverage % (Units Available)'] = (acumulados['In Stock'] / (acumulados['SalesQuantity'] * inventario_optimo_min)) * 100
    acumulados['Annual Sales %'] = (acumulados['SalesQuantity'] / (acumulados['SalesQuantity'] + acumulados['In Stock'])) * 100
    acumulados['Recommended Inventory'] = (acumulados['SalesQuantity'] * inventario_optimo_min).round(0)

    # Ajustar formatos
    acumulados['Recommended Inventory'] = acumulados['Recommended Inventory'].astype(int)
    acumulados['Inventory Coverage % (Units Available)'] = acumulados['Inventory Coverage % (Units Available)'].round(2)
    acumulados['Annual Sales %'] = acumulados['Annual Sales %'].round(2)

    # Crear columna de indicador basada en rangos
    def indicador_color(row):
        cobertura = float(row['Inventory Coverage % (Units Available)'])
        if cobertura > 110:
            return '❌'
        elif 90 < cobertura <= 110:
            return '✅'
        else:
            return '❗'

    acumulados['Estado'] = acumulados.apply(indicador_color, axis=1)

    # Reordenar columnas
    acumulados = acumulados[['Types', 'SalesQuantity', 'Annual Sales %', 'In Stock', 'Recommended Inventory', 'Inventory Coverage % (Units Available)', 'Estado']]

    acumulados = acumulados.sort_values(by='Inventory Coverage % (Units Available)', ascending=False)

    # Convertir valores a formato string con porcentaje
    acumulados['Inventory Coverage % (Units Available)'] = acumulados['Inventory Coverage % (Units Available)'].astype(str) + '%'
    acumulados['Annual Sales %'] = acumulados['Annual Sales %'].astype(str) + '%'

    # Formatear columnas numéricas con punto como separador de miles
    acumulados['SalesQuantity'] = acumulados['SalesQuantity'].apply(lambda x: f"{x:,.0f}".replace(",", "."))
    acumulados['In Stock'] = acumulados['In Stock'].apply(lambda x: f"{x:,.0f}".replace(",", "."))
    acumulados['Recommended Inventory'] = acumulados['Recommended Inventory'].apply(lambda x: f"{x:,.0f}".replace(",", "."))

    acumulados = acumulados.rename(columns ={'SalesQuantity': 'Unidades Vendidas',
                                             'Types': 'Tipo de bebida',
                                             'Annual Sales %':  '% Unidades Vendidas en el año',
                                             'In Stock': 'Unidades en Stock',
                                             'Recommended Inventory': 'Inventario óptimo recomendado',
                                             'Inventory Coverage % (Units Available)' : '% Inventario actualmente cubierto por Unidades en Stock'})


    # Calcular números de cada color
    num_rojo = sum(acumulados['Estado'] == '❌')
    num_verde = sum(acumulados['Estado'] == '✅')
    num_amarillo = sum(acumulados['Estado'] == '❗')

    # Mostrar conteo de colores debajo de los filtros
    with filter_col:
        st.markdown(f"""
            **Códigos por tipo de bedida:**
            - ✅   Inventario Recomendado: {num_verde}
            - ❌   Exceso de inventario: {num_rojo}
            - ❗   Falta de inventario: {num_amarillo}
        """)

    # Estilo ajustado para la tabla
    acumulados_styled = acumulados.style\
        .set_properties(**{'text-align': 'center'})\
        .set_table_styles([{'selector': 'th', 'props': [('font-weight', 'bold'), ('text-align', 'center')]}])\
        .hide(axis="index")

    # Mostrar la tabla en Streamlit
    with content_col:
        st.write(acumulados_styled.to_html(), unsafe_allow_html=True)
