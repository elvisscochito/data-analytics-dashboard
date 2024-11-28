import streamlit as st
from pages_.admin_interface.admin_first_page import admin_first_page

def user_first_page(df_ventas, df_compras, df_inventario, df_coordenadas):

    try:
        admin_first_page(df_ventas, df_compras, df_inventario, df_coordenadas)
    except Exception as e:
        st.error(f"Error: {e}")
