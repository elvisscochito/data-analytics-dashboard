import streamlit as st
from pages_.admin_interface.admin_fifth_page import admin_fifth_page

def user_fifth_page(df_ventas):
  try:
    admin_fifth_page(df_ventas)
  except Exception as e:
    st.error(f"Error: {e}")
