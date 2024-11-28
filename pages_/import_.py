import streamlit as st
import os

def import_page():
  # sidebar icon
  st.logo(
		"danu.png",
		icon_image="logo_copy.png",
		size="large"
	)

  if st.sidebar.button("Logout", key="team_logout_button"):
    st.session_state.authenticated = False
    st.success("Logout successful")

  st.title("Import data")

  """ st.write("Upload the datasets to import.")
  uploaded_files = st.file_uploader("Choose a file", accept_multiple_files=True)

  if uploaded_files:
    for file in uploaded_files:
      st.write(file.name)
      st.write(file.getvalue())
      st.success("File uploaded successfully.") """

  """ st.write("Or import each dataset individually.") """
  def save_uploaded_file(uploaded_file, folder="data"):
    if not os.path.exists(folder):
      os.makedirs(folder)
    file_path = os.path.join(folder, uploaded_file.name)
    with open(file_path, "wb") as f:
      f.write(uploaded_file.getvalue())
    return file_path

  def handle_file_upload(subheader, expected_filename, file_key):
    st.subheader(subheader)
    uploaded_file = st.file_uploader("Choose a file", type="csv", key=file_key)
    st.caption(f"Please upload the file named **'{expected_filename}'**")
    if uploaded_file:
      if uploaded_file.name == expected_filename:
        file_path = save_uploaded_file(uploaded_file)
        st.success(f"File replaced successfully at {file_path}.", icon="✅")
      else:
        st.warning(f"Please upload the correct file named **'{expected_filename}'**.", icon="⚠️")

  with st.container(border=True):
    handle_file_upload("Ventas", "Ventas_profit.csv", "ventas")

  with st.container(border=True):
    handle_file_upload("Compras", "compras_dashboard.csv", "compras")

  with st.container(border=True):
    handle_file_upload("Inventario", "Inventario_Nuevo_final.csv", "inventario")

  with st.container(border=True):
    handle_file_upload("Coordenadas de ciudades", "df_coordenadas.csv", "coordenadas")
