import streamlit as st

def export_page(df_ventas, df_compras, df_inventario, df_coordenadas):
  # sidebar icon
  st.logo(
		"danu.png",
		icon_image="logo_copy.png",
		size="large"
	)

  if st.sidebar.button("Logout", key="team_logout_button"):
    st.session_state.authenticated = False
    st.success("Logout successful")

  st.title("Export data")

  """ @st.cache_resource(show_spinner=False)
  def df_to_csv():
    ventas_csv_path = 'data/Ventas_profit.csv'
    compras_csv_path = 'data/compras_dashboard.csv'
    inventario_csv_path = 'data/Inventario_Nuevo_final.csv'
    coordenadas_csv_path = 'data/df_coordenadas.csv'

    ventas_csv = df_ventas.to_csv(ventas_csv_path, index=False)
    compras_csv = df_compras.to_csv(compras_csv_path, index=False)
    inventario_csv = df_inventario.to_csv(inventario_csv_path, index=False)
    coordenadas_csv = df_coordenadas.to_csv(coordenadas_csv_path, index=False)

    return ventas_csv_path, compras_csv_path, inventario_csv_path, coordenadas_csv_path

  ventas_csv, compras_csv, inventario_csv, coordenadas_csv = df_to_csv() """

  def export_csv(df, df_name, file_path, file_name, key_download):
    st.write(df.head())
    if st.download_button("Download full csv", open(file_path, 'rb').read(), file_name, "text/csv", key=key_download):
      st.success("Dataset exported successfully to CSV.")

  with st.expander("**Ventas**"):
    export_csv(df_ventas, "df_name", 'data/Ventas_profit.csv', 'ventas.csv', 'download_ventas')

  with st.expander("**Compras**"):
    export_csv(df_compras, "df_compras", 'data/compras_dashboard.csv', 'compras.csv', 'download_compras')

  with st.expander("**Inventario**"):
    export_csv(df_inventario, "df_inventario", 'data/Inventario_Nuevo_final.csv', 'inventario.csv', 'download_inventario')

  with st.expander("**Coordenadas de ciudades**"):
      export_csv(df_coordenadas, "df_coordenadas", 'data/df_coordenadas.csv', 'coordenadas.csv', 'download_coordenadas')
