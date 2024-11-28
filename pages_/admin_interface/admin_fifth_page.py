import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LinearRegression

# define the function to the fifth_ page of the admin interface and be called in the main file

def admin_fifth_page(df_ventas):
	# sidebar icon
	st.logo(
		"danu.png",
		icon_image="logo_copy.png",
		size="large"
	)

	""" def process_data(df_ventas):
		# Paso 1: Identificar el producto menos vendido por ciudad y tipo
		# Agrupar por ciudad, tipo y producto (IdVentas), calcular las ventas totales por producto y elegir el menos vendido.
		least_sold = (
			df_ventas.groupby(['City', 'Types', 'IdVentas'], as_index=False)
			.agg({'SalesQuantity': 'sum', 'SalesDollars': 'first'})
			.sort_values(['City', 'Types', 'SalesQuantity'])
			.groupby(['City', 'Types'], as_index=False)
			.first()
		)

		# Paso 2: Preparar datos para la regresión
		# Selección de las variables predictoras y la variable objetivo
		X = df_ventas[['Types', 'City', 'Season', 'SalesDay', 'PurchasePrice', 'Profit']]
		y = df_ventas['SalesQuantity']

		# Codificar variables categóricas
		encoder = OneHotEncoder(drop='first', sparse_output=False)
		X_categorical = X[['Types', 'City', 'Season', 'SalesDay']]
		X_encoded = encoder.fit_transform(X_categorical)

		# Combinar variables numéricas y categóricas
		X_numeric = X[['PurchasePrice', 'Profit']].to_numpy()
		X_final = np.hstack((X_encoded, X_numeric))

		# Verificar y manejar valores nulos
		if np.isnan(X_final).any():
			print("Hay valores nulos en los datos. Procediendo a imputarlos.")
			# Imputar valores faltantes en las variables numéricas con la media
			X_numeric = np.nan_to_num(X_numeric, nan=np.nanmean(X_numeric, axis=0))
			# Volver a combinar
			X_final = np.hstack((X_encoded, X_numeric))

		# Entrenar el modelo de regresión lineal
		model = LinearRegression()
		model.fit(X_final, y)

		# Obtener los coeficientes de las variables
		coefficients = pd.DataFrame(
			{'Feature': list(encoder.get_feature_names_out()) + ['PurchasePrice', 'Profit'], 'Coefficient': model.coef_}
		).sort_values(by='Coefficient', ascending=False)

		# Paso 3: Calcular descuentos sugeridos
		# Calcular un descuento base del 10% del precio de venta
		least_sold['SuggestedDiscount'] = least_sold['SalesDollars'] * 0.1

		# Ajustar el descuento basado en la elasticidad
		elasticity_threshold = 0.05  # Umbral para la elasticidad
		purchase_price_idx = coefficients[coefficients['Feature'] == 'PurchasePrice'].index[0]
		elasticity_factor = model.coef_[purchase_price_idx]

		least_sold['AdjustedDiscount'] = np.where(
			least_sold['SalesQuantity'] * elasticity_factor < elasticity_threshold,
			least_sold['SalesDollars'] * 0.2,  # Incrementar descuento al 20% si es poco elástico
			least_sold['SuggestedDiscount']
		)

		# export the data
		result = least_sold[['City', 'Types', 'IdVentas', 'SalesQuantity', 'SalesDollars', 'SuggestedDiscount', 'AdjustedDiscount']]
		print("Coeficientes del modelo:")
		print(coefficients)
		print("\nResultados finales:")
		print(result)

		result.to_csv("data/least_sold_filtered.csv", index=False)

	process_data(df_ventas) """

	least_sold_filtered = pd.read_csv("data/least_sold_filtered.csv")

	# Interfaz de Streamlit
	st.title("Descuentos Sugeridos por Ciudad y Tipo de Producto")

	# Filtrar por país
	if st.session_state.username == "admin":
		paises = least_sold_filtered['Country'].unique()
		pais_seleccionado = st.sidebar.selectbox("Selecciona un país:", options=paises)
	else:
		pais_seleccionado = "Escocia"

	# Filtrar ciudades según el país seleccionado
	ciudades_filtradas = least_sold_filtered[least_sold_filtered['Country'] == pais_seleccionado]['City'].unique()
	ciudad_seleccionada = st.sidebar.selectbox("Selecciona una ciudad:", options=ciudades_filtradas)

	# Filtrar tipos según la ciudad seleccionada
	tipos_filtrados = least_sold_filtered[
			(least_sold_filtered['Country'] == pais_seleccionado) &
			(least_sold_filtered['City'] == ciudad_seleccionada)
	]['Types'].unique()
	tipo_seleccionado = st.sidebar.selectbox("Selecciona un tipo de producto:", options=tipos_filtrados)

	if st.sidebar.button("Logout", key="admin_logout_button_5"):
		st.session_state.authenticated = False
		st.success("Logout successful")

	# Filtrar resultados según selección
	resultado = least_sold_filtered[
			(least_sold_filtered['Country'] == pais_seleccionado) &
			(least_sold_filtered['City'] == ciudad_seleccionada) &
			(least_sold_filtered['Types'] == tipo_seleccionado)
	]

	# Mostrar resultados con estilo
	st.subheader("Resultados Filtrados")
	if not resultado.empty:
		# Redondear el descuento y añadir el símbolo de porcentaje
		resultado.loc[:, 'AdjustedDiscount'] = resultado['AdjustedDiscount'].round(0).astype(int)

		# Mostrar resultados estilizados
		for _, row in resultado.iterrows():
			st.markdown(
				f"""
				<div style="padding: 10px; border: 1px solid #ddd; border-radius: 5px; margin-bottom: 10px; background-color: #f9f9f9;">
					<h3 style="color: #333;">Ciudad: <span style="font-weight: bold;">{row['City']}</span></h3>
					<p style="font-size: 16px; color: #555;">Tipo de Producto: <span style="font-weight: bold;">{row['Types']}</span></p>
					<p style="font-size: 16px; color: #555;">Descuento Ajustado: <span style="font-weight: bold;">{row['AdjustedDiscount']}%</span></p>
				</div>
				""",
				unsafe_allow_html=True
			)
	else:
		# Mensaje técnico cuando no se requiere ajuste
		st.write(
			f"El producto del tipo '{tipo_seleccionado}' en la ciudad '{ciudad_seleccionada}' "
			"no requiere ajustes de demanda mediante la aplicación de descuentos."
		)
