import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# define the function to the first page of the admin interface and be called in the main file
def admin_first_page(df_ventas, df_compras, df_inventario, df_coordenadas):

    df_ventas['SalesDate'] = pd.to_datetime(df_ventas['SalesDate'])
    df_compras['ReceivingDate'] = pd.to_datetime(df_compras['ReceivingDate'])

    df_ventas = df_ventas.loc[~df_ventas["City"].isin([
        "Alnwick", "Blackpool", "Hornsea", "Cardiff", "Leeds", "West Bromwich",
        "Banbury", "Lundy", "Oldham", "Barrow-in-Furness","Winterton"
    ])]

    if st.session_state.username == "admin":
        st.title(" Rendimiento 2016 - Danu Bebidas")
    elif st.session_state.username == "user":
        st.title("Rendimiento 2016 - Escocia")

    #region Sidebar

    #sidebar icon
    st.logo(
        "danu.png",
        icon_image="logo_copy.png",
        size="large"
    )

    #Filtros en sidebar
    st.sidebar.header("Filtros")

    # Lista de meses en español
    meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
    mes = st.sidebar.selectbox("Selecciona un mes", meses)

    # Mapeo de los meses a números en español
    meses_dict = {
        'Enero': '2016-01', 'Febrero': '2016-02', 'Marzo': '2016-03', 'Abril': '2016-04', 'Mayo': '2016-05', 'Junio': '2016-06',
        'Julio': '2016-07', 'Agosto': '2016-08', 'Septiembre': '2016-09', 'Octubre': '2016-10', 'Noviembre': '2016-11', 'Diciembre': '2016-12'
    }

    # Usar el mes seleccionado para filtrar los datos
    mes_numero = meses_dict[mes]

    #Pais
    if st.session_state.username == "admin":
        pais = st.sidebar.selectbox("País", ["Todos"] + sorted(list(df_ventas['Country'].unique())))
    else:
        pais = "Escocia"

    #Pais selecciona por DB
    df_pais_selec_v = df_ventas if pais == "Todos" else df_ventas[df_ventas['Country'] == pais]
    df_pais_selec_c = df_compras if pais == "Todos" else df_compras[df_compras['Country'] == pais]
    df_pais_selec_i = df_inventario if pais == "Todos" else df_inventario[df_inventario['Country'] == pais]

    ciudad = st.sidebar.selectbox("Ciudad", ["Todas"] + sorted(list(df_pais_selec_v['City'].unique())))

    #Df a trabajar filtrado por pais y ciudad
    df_final_ventas = df_pais_selec_v if ciudad == "Todas" else df_pais_selec_v[df_pais_selec_v['City'] == ciudad]
    df_final_compras = df_pais_selec_c if ciudad == "Todas" else df_pais_selec_c[df_pais_selec_c['City'] == ciudad]
    df_final_inventario = df_pais_selec_i if ciudad == "Todas" else df_pais_selec_i[df_pais_selec_i['City'] == ciudad]

    #Mensual
    df_final_compras = df_final_compras.copy()
    df_final_ventas = df_final_ventas.copy()
    df_final_compras['YearMonth'] = df_final_compras['ReceivingDate'].dt.to_period('M')
    df_final_ventas['YearMonth'] = df_final_ventas['SalesDate'].dt.to_period('M')

    df_final_compras = df_final_compras[df_final_compras['YearMonth'] <= mes_numero]
    df_final_ventas = df_final_ventas[df_final_ventas ['YearMonth'] <= mes_numero]

    #Mes actual y anterior
    mes_index = meses.index(mes)
    mes1 = mes_numero
    mes_anterior = meses[mes_index - 1]
    mes2 = meses_dict[mes_anterior]
    # Seleccionar la métrica dentro de la gráfica
    métrica = st.sidebar.radio(
        "Seleccione la métrica:",
        options=["Unidades vendidas", "Ganancia"],
        index=1,
        key="metric_selector"
        )

    #endregion

    if st.sidebar.button("Logout", key="admin_logout_button_1"):
        st.session_state.authenticated = False
        st.success("Logout successful")

    #region Metrics
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)

    #Mes 1 y Mes2 para metricas
    df_mes1 = df_final_ventas[df_final_ventas['YearMonth'] == mes1]
    df_mes2 = df_final_ventas[df_final_ventas['YearMonth'] == mes2]
    df_mesp1 = df_final_compras[df_final_compras['YearMonth'] == mes1]
    df_mesp2 = df_final_compras[df_final_compras['YearMonth'] == mes2]

    #Condicional para el primer mes
    if mes1 != '2016-01':
        uni_mes = ((df_mes1['SalesQuantity'].sum()- df_mes2['SalesQuantity'].sum()) / df_mes2['SalesQuantity'].sum()).round(2)
        delta_valor = f"{uni_mes:,}% comparado al último mes"
        sales_value = (((df_mes1['SalesDollars'].sum())- df_mes2['SalesDollars'].sum()) / df_mes2['SalesDollars'].sum()).round(2)
        delta_sales = f"{sales_value:,}% comparado al último mes"
        purchases_value = (((df_mesp1['Dollars'].sum())- df_mesp2['Dollars'].sum()) / df_mesp2['Dollars'].sum()).round(2)
        delta_purchase = f"{purchases_value:,}% comparado al último mes"
        estatus_value = 'inverse'
        estatus = 'normal'
    else:
        delta_valor = 'Primer mes'
        delta_sales = 'Primer mes'
        delta_purchase = 'Primer mes'
        estatus_value = 'off'
        estatus = 'off'

    with kpi1:
        st.metric(label="Unidades Vendidas", value=f"{((df_final_ventas['SalesQuantity'].sum()) /1000000).round(2).astype('float'):,}M",delta = delta_valor, delta_color= estatus)

    with kpi2:
# Calcular el profit y delta
        profit = df_final_ventas['Profit'].sum()
        meta_ing = 47283000
        meta_escocia = 10585000
        meta_gales = 1521000
        meta_irlanda = 750000

        # Mostrar el valor de profit y delta con color y flecha automática
        if (pais == 'Inglaterra') & (ciudad == 'Todas'):
            meta = meta_ing
        elif (pais == 'Inglaterra') & (ciudad != 'Todas'):
            meta = meta_ing / 5

        elif (pais == 'Escocia') & (ciudad == 'Todas'):
            meta = meta_escocia

        elif (pais == 'Escocia') & (ciudad != 'Todas'):
            meta = meta_escocia / 2

        elif pais == 'Gales':
            meta = meta_gales
        elif pais == 'Irlanda del Norte':
            meta = meta_irlanda
        else:
            meta = meta_ing + meta_irlanda + meta_escocia + meta_gales

        delt = (profit - meta)/meta*100

        st.metric(
            label="Ganancia",
            value=f"${((profit)/1000000).round(2):,}M",
            delta=f"{delt.round(2)}%",
            delta_color="normal"  # Automático: verde para positivo, rojo para negativo
        )

    with kpi3:
        sales_mes = ((df_mes1['SalesDollars'].sum()) / 1000).astype('float').round(2)
        st.metric(label= "Ingresos por ventas", value=f"${(df_final_ventas['SalesDollars'].sum()/ 1000000).round(2):,}M", delta = delta_sales, delta_color = estatus)

    with kpi4:
        st.metric(label= "Gastos en compras", value=f"${(df_final_compras['Dollars'].sum()/1000000).round(2):,}M", delta = delta_purchase, delta_color= estatus_value)

    #endregion

    #region P1
    #region Primera Fila
    col1, col2, col3 = st.columns(3)

    with col1:
        df_pro = df_final_ventas.copy()

        # Agrupar por YearMonth y calcular el profit mensual
        df_pro = df_pro.groupby('YearMonth')['Profit'].sum().reset_index()

        # Convertir YearMonth al nombre del mes en inglés
        df_pro['YearMonth'] = df_pro['YearMonth'].dt.strftime('%B')

        # Definir el mapeo de meses en inglés a español
        meses_mapeo = {
            "January": "Enero",
            "February": "Febrero",
            "March": "Marzo",
            "April": "Abril",
            "May": "Mayo",
            "June": "Junio",
            "July": "Julio",
            "August": "Agosto",
            "September": "Septiembre",
            "October": "Octubre",
            "November": "Noviembre",
            "December": "Diciembre"
        }

        # Reemplazar los valores en la columna 'YearMonth'
        df_pro['YearMonth'] = df_pro['YearMonth'].replace(meses_mapeo)


        # Crear la figura con Plotly
        fig = go.Figure()

        # Agregar la gráfica de puntos de Profit
        fig.add_trace(go.Scatter(
            x=df_pro['YearMonth'],
            y=df_pro['Profit'],
            mode='lines+markers',  # Mostrar líneas y puntos
            name='Profit Mensual',
            marker=dict(color='royalblue', size=8)
        ))

        # Configurar el layout del gráfico
        fig.update_layout(
            title="Ganancia Mensual",
            xaxis_title="Mes",
            yaxis_title="Ganancia en Dólares",
            template="plotly_dark",
            xaxis=dict(tickangle=45),
            showlegend=False
        )

        # Mostrar el gráfico en COL1
        st.plotly_chart(fig)

    with col2:
        if mes_index>0:
            profit_mes1=df_mes1
            profit_mes2= df_mes2

            profit_mes1.loc[:, 'WeekOfMonth'] = (profit_mes1['SalesDate'].dt.day - 1) // 7   # Agrupar en semanas dentro del mes (1 a 4)
            profit_mes2.loc[:, 'WeekOfMonth'] = (profit_mes2['SalesDate'].dt.day - 1) // 7   # Agrupar en semanas dentro del mes (1 a 4)

            #Semana 1
            profit_diario_mes1 = profit_mes1.groupby('WeekOfMonth')['Profit'].sum()
            profit_diario_mes1 = profit_diario_mes1.reset_index(name='Profit1')

            # Semana 2
            profit_diario_mes2 = profit_mes2.groupby('WeekOfMonth')['Profit'].sum()
            profit_diario_mes2 = profit_diario_mes2.reset_index(name='Profit2')

            df_profits = pd.merge(profit_diario_mes1, profit_diario_mes2, on='WeekOfMonth', how='outer')

            fig2 = go.Figure()

            # Agregar línea para mes1
            fig2.add_trace(go.Scatter(
                x=df_profits['WeekOfMonth'],
                y=df_profits['Profit1'],
                mode='lines+markers',
                name=f'Ganancia Actual'
            ))

            # Agregar línea para mes2
            fig2.add_trace(go.Scatter(
                x=df_profits['WeekOfMonth'],
                y=df_profits['Profit2'],
                mode='lines+markers',
                name=f'Ganancia Anterior'
            ))

            # Configuración de la gráfica
            fig2.update_layout(
                title="Comparativa: Ganancia Semanal por Mes",
                xaxis_title="Semana del Mes",
                yaxis_title="Ganancia en Dólares",
                legend_title="Mes",
                legend=dict(
                x=0,  
                y=0,  
                xanchor="center",  
                yanchor="middle", 
                bgcolor="rgba(255, 255, 255, 0.5)", 
                bordercolor="Black",  
                borderwidth=1        
    )
            )

            st.plotly_chart(fig2)
        else:
            st.markdown(
            """
            <div style="display: flex; height: 200px; align-items: center; justify-content: center;">
                <p>No hay mes anterior para el primer mes del año.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        df_ventas_col3 = df_final_ventas.copy()
        df_ventas_col3 = df_ventas_col3[df_ventas_col3['YearMonth'] == mes1]

        # Definir el mapeo de días en inglés a español
        dias_mapeo = {
            "Monday": "Lunes",
            "Tuesday": "Martes",
            "Wednesday": "Miércoles",
            "Thursday": "Jueves",
            "Friday": "Viernes",
            "Saturday": "Sábado",
            "Sunday": "Domingo"
        }

        # Reemplazar los valores en la columna 'SalesDay'
        df_ventas_col3['SalesDay'] = df_ventas_col3['SalesDay'].replace(dias_mapeo)

        # Definir el orden de los días de la semana en español
        dias_ordenado_esp = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        df_ventas_col3['SalesDay'] = pd.Categorical(df_ventas_col3['SalesDay'], categories=dias_ordenado_esp, ordered=True)

        # Agrupar por día de la semana y calcular las sumas de ventas y compras
        ventas_semana_3 = df_ventas_col3.groupby('SalesDay')['Profit'].sum().reset_index()


        fig3 = go.Figure()

        # Configuración de etiquetas
        fig3.update_layout(
            title="Ventas Mensuales por Día de la Semana",
            xaxis_title="Día de la Semana",
            yaxis_title="Ganancia en Dólares",
            showlegend= False
        )

        fig3.add_trace(go.Scatter(
        x=ventas_semana_3['SalesDay'],
        y=ventas_semana_3['Profit'],
        mode='lines+markers',
        ))
        st.plotly_chart(fig3)
    #endregion

    col4, col5 = st.columns(2)

    #region Segunda Fila
    with col5:
        if 'Country' in df_coordenadas.columns:
            df_coordenadas_filtrado = df_coordenadas if pais == "Todos" else df_coordenadas[df_coordenadas['Country'] == pais]
        else:
            df_coordenadas_filtrado = df_coordenadas

        # Filtrar las ciudades del país seleccionado
        df_coordenadas_filtrado = df_coordenadas_filtrado[df_coordenadas_filtrado['City'].isin(df_final_ventas['City'].unique())]

        mapa = df_coordenadas_filtrado[['latitude', 'longitude', 'SalesQuantity', 'City']]
        mapa['size'] = mapa['SalesQuantity'] / mapa['SalesQuantity'].max() * 100
        mapa = mapa.rename(columns={'SalesQuantity': 'Unidades Vendidas'})

        fig_map = px.scatter_mapbox(
            mapa,
            lat="latitude",
            lon="longitude",
            size="size",
            color="Unidades Vendidas",
            hover_name="City",
            hover_data={"Unidades Vendidas": True, "City": False, "size": False, "latitude": False, "longitude": False},
            size_max=14,
            zoom=3,
            mapbox_style="carto-positron",
            color_continuous_scale=px.colors.sequential.Blues[5:]
        )
        fig_map.update_layout(
            title=dict(
            text="Mapa de Unidades Vendidas por Ciudad",
            y=0.92 
            )
        )

        fig_map.update_traces(marker=dict(size=mapa['size']))

        st.plotly_chart(fig_map)
    with col4:
        # If para la métrica elegida
        if métrica == "Unidades vendidas":
            datos = df_final_ventas.groupby('Types')['SalesQuantity'].sum().reset_index()
            datos['SalesQuantity'] = datos['SalesQuantity']
            x_column = "SalesQuantity"
            y_label = "Unidades vendidas"
        else:
            # Profit
            ventas_por_tipo = df_final_ventas.groupby('Types')['Profit'].sum().reset_index()
            datos = ventas_por_tipo[['Types', 'Profit']]
            x_column = "Profit"
            y_label = "Ganancia"

        # Crear la figura con Plotly
        fig = px.bar(datos, x=x_column, y='Types', orientation='h',
                    title="Ganancia y Unidades Vendidas por Tipo de Bebida", labels={x_column: y_label})

        # Actualizar el diseño de la gráfica
        fig.update_layout(yaxis_title="Tipo de Alcohol", xaxis=dict(showgrid=True))

        # Mostrar el gráfico
        st.plotly_chart(fig, use_container_width=True)
    #endregion

    #endregion
