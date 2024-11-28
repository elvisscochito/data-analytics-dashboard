import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

# define the function to the fourth page of the admin interface and be called in the main file
def admin_fourth_page():
  #region Carga de archivos PROPHET y SIDEBAR

	# Ruta de la carpeta con los archivos exportados
	output_dir = 'prophet_outputs'

	# Métricas
	metrics_path = f'{output_dir}/city_metrics.csv'
	df_metrics = pd.read_csv(metrics_path)

	# Lista de ciudades
	cities = sorted(df_metrics['City'].unique())

	# Diccionario de países y sus ciudades asociadas
	cities_by_country = {
			'Inglaterra': ['Penzance', 'Norfolk', 'Gargrave', 'Monmouth','Grays',
											'Guisborough', 'Drybrook', 'Bexhill', 'Lanteglos', 'Hartlepool', 'Cleethorpes',
											'Gloucester', 'Athelney', 'Southwark', 'Chesterfield',
											'Luton', 'Inverness', 'Salisbury', 'Stanmore', 'Keld', 'Clacton-on-Sea', 'Stanmore',
											'Huddersfield', 'Doncaster', 'Barnstaple', 'Tamworth', 'Eastbourne',
											'Sutton'],
			'Escocia': ['Aberdeen', 'Arran', 'Inverness', 'Kilmarnock'],
			'Irlanda del Norte': ['Ballymena'],
			'Gales': ['Pontypridd']
	}

	# Sidebar con país y ciudad
	st.logo(
		"danu.png",
		icon_image="logo_copy.png",
		size="large"
	)

	with st.sidebar:
		# Filtro de Mes
		month_names = [
        "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
        "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
    ]

		month = st.selectbox("Mes:", list(range(1, 13)), format_func=lambda x: month_names[x - 1])

		# Filtro de País
		if st.session_state.username == "admin":
			pais = st.selectbox("País:", sorted(list(cities_by_country.keys())),index=0) # Index 0 para que el default sea escocia
		else:
			pais = "Escocia"

    # Filtrar ciudades según el país seleccionado
		cities_filtered = sorted(cities_by_country[pais])

    # Filtro de Ciudad
		city = st.selectbox('Ciudad:', cities_filtered,index=0)   # Index 2 para que aparezca inverness por default

	if st.sidebar.button("Logout", key="admin_logout_button_4"):
		st.session_state.authenticated = False
		st.success("Logout successful")

	# Cargar archivos específicos de la ciudad seleccionada
	forecast_path = f'{output_dir}/{city}_forecast.csv'
	train_path = f'{output_dir}/{city}_train.csv'
	test_path = f'{output_dir}/{city}_test.csv'

	forecast = pd.read_csv(forecast_path)
	train = pd.read_csv(train_path)
	test = pd.read_csv(test_path)
	#endregion


	st.title(f"Predicciones de Ventas para el 2017")


	#region Gráfica - Serie de Tiempo
	fig1 = go.Figure()

	# Train
	fig1.add_trace(go.Scatter(
			x=train['ds'],
			y=train['y'],
			mode='lines',
			name='Datos Reales (2016)',
			line=dict(color='blue')
	))

	# Test
	fig1.add_trace(go.Scatter(
			x=test['ds'],
			y=test['y'],
			mode='lines',
			line=dict(color='blue'),
			showlegend=False
	))

	# Forecast
	fig1.add_trace(go.Scatter(
			x=forecast['ds'],
			y=forecast['yhat'],
			mode='lines',
			name='Predicción (2017)',
			line=dict(color='green')
	))

	# Configuración de la gráfica
	fig1.update_layout(
			xaxis_title="Fecha",
			yaxis_title="Ventas",
			legend_title="Leyenda",
			template="plotly_white",
			legend=dict(
					x=.85,  # Posición horizontal (0 = izquierda, 1 = derecha)
					y=1,  # Posición vertical (0 = arriba, 1 = abajo)
					bgcolor="rgba(255,255,255,0.8)",  # Fondo semitransparente
					bordercolor="black",
					borderwidth=1
			)
	)

	# Mostrar la gráfica en Streamlit (row1)
	st.plotly_chart(fig1, use_container_width=True)
	#endregion

	#region Gráfica - MES y FORECAST
	forecast['ds'] = pd.to_datetime(forecast['ds'])

	# Filtrar el forecast hasta el mes seleccionado (acumulado) y solo 2017
	forecast_acumulado = forecast[(forecast['ds'].dt.year == 2017) & (forecast['ds'].dt.month <= month)]

	# Crear gráfica acumulada
	fig2 = go.Figure()

	# Forecast acumulado
	fig2.add_trace(go.Scatter(
			x=forecast_acumulado['ds'],
			y=forecast_acumulado['yhat'],
			mode='lines',
			name='Predicción',
			line=dict(color='green')
	))


	# Configuración de la gráfica
	fig2.update_layout(
			title=f"Predicción de Ventas hasta {month_names[month - 1]} del 2017 en {city}",
			xaxis_title="Fecha",
			yaxis_title="Ventas",
			legend_title="Leyenda",
			template="plotly_white",
			legend=dict(
					x=0.02,
					y=0.98,
					bgcolor="rgba(255,255,255,0.8)",
					bordercolor="black",
					borderwidth=1
			)
	)

	# Mostrar la gráfica en Streamlit (row2 col1)

	col1, col2 = st.columns([2, 1])

	with col1:
			st.plotly_chart(fig2, use_container_width=True)
	#endregion

	#region KPIs en row2 col2
	with col2:
			# Filtrar las métricas de la ciudad seleccionada
			st.write("\n")
			city_metrics = df_metrics[df_metrics['City'] == city].iloc[0]

			st.header(f"**Métricas del modelo**")
			# Mostrar los valores de city_metrics.csv
			st.write(f"**MAE (Error Absoluto Medio):** {city_metrics['MAE']:.2f}")
			st.write(f"**RMSE (Raíz del Error Cuadrático Medio):** {city_metrics['RMSE']:.2f}")
			st.write(f"**MSE (Error Cuadrático Medio):** {city_metrics['MSE']:.2f}")

			# Calcular el Total de Ventas 2017
			total_ventas_2017 = forecast_acumulado['yhat'].sum()
			st.subheader(f"**Ventas hasta {month_names[month - 1]}:** {total_ventas_2017:,.2f}")

			#endregion
