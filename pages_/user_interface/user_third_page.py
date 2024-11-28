import streamlit as st
from pages_.admin_interface.admin_third_page import admin_third_page

def user_third_page(df_inventario):
  try:
    admin_third_page(df_inventario)
  except Exception as e:
    st.error(f"Error: {e}")
