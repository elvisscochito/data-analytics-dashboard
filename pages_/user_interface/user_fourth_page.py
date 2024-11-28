import streamlit as st
from pages_.admin_interface.admin_fourth_page import admin_fourth_page

def user_fourth_page():
  try:
    admin_fourth_page()
  except Exception as e:
    st.error(f"Error: {e}")
