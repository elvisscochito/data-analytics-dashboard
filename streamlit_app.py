import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import base64
import pathlib
from pages_.admin_interface.admin_first_page import admin_first_page
# from pages_.admin_interface.admin_second_page import admin_second_page
from pages_.admin_interface.admin_third_page import admin_third_page
from pages_.admin_interface.admin_fourth_page import admin_fourth_page
from pages_.admin_interface.admin_fifth_page import admin_fifth_page
from pages_.user_interface.user_first_page import user_first_page
from pages_.user_interface.user_third_page import user_third_page
from pages_.user_interface.user_fourth_page import user_fourth_page
from pages_.user_interface.user_fifth_page import user_fifth_page
from pages_.import_ import import_page
from pages_.export import export_page

# region auth
if "authenticated" in st.session_state and st.session_state.authenticated:
  st.set_page_config(layout="wide")
else:
  st.set_page_config(layout="centered", page_title="Login - Dashboard Danu Bebidas")

if "authenticated" not in st.session_state:
  st.session_state.authenticated = False
  st.session_state.username = ""
# endregion

#region DB
# cache our .csv global resources  to avoid loading them multiple times
@st.cache_resource(show_spinner=False)
def load_data():
  df_ventas = pd.read_csv("data/Ventas_profit.csv")
  df_compras = pd.read_csv("data/compras_dashboard.csv")
  df_inventario = pd.read_csv("data/Inventario_Nuevo_final.csv")
  df_coordenadas = pd.read_csv("data/df_coordenadas.csv")

  df_ventas['SalesDate'] = pd.to_datetime(df_ventas['SalesDate'])
  df_compras['ReceivingDate'] = pd.to_datetime(df_compras['ReceivingDate'])

  return df_ventas, df_compras, df_inventario, df_coordenadas

df_ventas, df_compras, df_inventario, df_coordenadas = load_data()
#endregion

# region styles
# css to change Streamlit's default styles behavior and our custom custom css styles
st.markdown("""
  <style>
    header[data-testid="stHeader"] {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    div.header {
      display: flex;
      flex-direction: row;
      justify-content: center;
      align-items: center;
      padding: 2rem;
      border-bottom: 1px solid #e4e4e7;
      width: 100% !important;
      height: 12vh !important;
      top: 0;
      left: 0;
      z-index: 100;
      position: fixed;

      img.danu {
        width: 9em;
      }
    }

    div.footer {
      display: flex;
      flex-direction: row;
      justify-content: center;
      align-items: center;
      padding: 1.8rem;
      color: rgb(113, 113, 121);
      width: 100%;
      height: 8vh;
      bottom: 0;
      left: 0;
      z-index: 100;
      position: fixed;
      border-top: 1px solid #e4e4e7;
      background-color: hsla(240, 9%, 98%, 0.8);
    }

    nav.navbar {
      width: 100vw;
      height: 10vh;
      top: 0;
      left: 0;
      z-index: 100;
      position: fixed;
      border-bottom: 1px solid #e4e4e7 !important;
      padding: 0 1rem;
      background-color: hsla(240, 9%, 98%, 0.8) !important;
      backdrop-filter: blur(8px);
      display: flex;
      align-items: center;
      justify-content: space-between;

      ul.navbar-container {
        list-style-type: none;
        display: flex;
        lex-direction: row;
        align-items: center;
        justify-content: space-between; /* Asegura espacio entre logo y perfil */
        width: 100% !important;
        height: 100% !important;

        li.navbar-item:first-child {
          flex: 1; /* Deja espacio para centrar el logo */
          display: flex;
          align-items: center;
          justify-content: center; /* Centra el logo */

          img.logo {
            width: 3em;
            height: 3em;
            aspect-ratio: 1/1;
            align-self: center;
          }
        }

        li.navbar-item:last-child {
          display: flex;
          flex-direction: row;
          align-items: center;
          justify-content: flex-end; /* Coloca el perfil a la derecha */
          gap: 1rem;

          span.name {
            font-weight: 600 !important;
            text-transform: capitalize;
          }

          img.profile {
            width: 3em;
            height: 3em;
            border-radius: 50%;
            aspect-ratio: 1/1;
          }
        }
      }
    }

    .stSidebar.st-emotion-cache-11wc8as {
      [data-testid="stLogo"] {
        height: 4rem !important;
        transition: all 0.3s ease-in-out !important;
      }
    }

    .chatling-open-chat-icon {
        width: 100%;
				height: 100%;
				position: fixed;
				top: 0;
				left: 0;
				z-index: 9999;
				background: rgba(255, 255, 255, 0.8);
    }
  </style>
""", unsafe_allow_html=True)
# endregion styles

# region login
def login():
  # css to hide the sidebar and navigation on the login page
  st.markdown("""
      <style>
      /* Hide the sidebar */
      [data-testid="stSidebar"] {
          display: none;
      }
      /* Hide the sidebar toggle button */
      [data-testid="stBaseButton-headerNoPadding"] {
          display: none;
      }
      </style>
  """, unsafe_allow_html=True)

  # code to show the danu logo in the login page
  danu_path = str(pathlib.Path(__file__).parent / "danu.png")

  with open(danu_path, "rb") as img_file:
    image_base64 = base64.b64encode(img_file.read()).decode('utf-8')
    danu_img = f'<img src="data:image/png;base64,{image_base64}" alt="Danu Logo" id="logo" class="danu">'

  st.markdown(f"""
    <div class="header">
      {danu_img}
    </div>
  """, unsafe_allow_html=True)

  st.markdown("<h1>Login - <span style='color: #07084D';>Dashboard Danu Analítica<span></h1>", unsafe_allow_html=True)
  username = st.text_input("Username")
  password = st.text_input("Password", type="password")

  # hardcoded login credentials (logic for dynamic ui)
  if st.button("Login"):
    if username == "admin" and password == "root":
      st.session_state.authenticated = True
      st.session_state.username = "admin"
      st.success("Login successful")
    elif username == "user" and password == "root":
      st.session_state.authenticated = True
      st.session_state.username = "user"
      st.success("Login successful")
    else:
      st.error("Invalid username or password")

  st.markdown(f"""
    <div class="footer">
      Copyright© 2024 Danu Analítica. Todos los derechos reservados.
    </div>
  """, unsafe_allow_html=True)
# endregion login

# navbar component
def nav_bar():
  # path to the image
  image_path = str(pathlib.Path(__file__).parent / "assets/avatar.png")
  logo_path = str(pathlib.Path(__file__).parent / "assets/logo.png")

  # read and encode the image in base64
  with open(image_path, "rb") as img_file:
    image_base64 = base64.b64encode(img_file.read()).decode('utf-8')
    image_html = f'<img src="data:image/png;base64,{image_base64}" alt="Profile image" id="profile" class="profile">'

  with open(logo_path, "rb") as img_file:
    logo_base64 = base64.b64encode(img_file.read()).decode('utf-8')
    logo_html = f'<img src="data:image/png;base64,{logo_base64}" alt="Danu Logo" id="logo" class="logo">'

  # use markdown to insert the HTML image in Streamlit
  username_display = st.session_state.get('username', 'Usuario')
  if username_display == "user":
    username_display += " Escocia"

  st.markdown(f"""
        <nav class="navbar">
          <ul class="navbar-container">
            <li class="navbar-item">
              {logo_html}
            </li>
            <li class="navbar-item">
              <span class="name">{username_display}</span>
              {image_html}
            </li>
          </ul>
        </nav>
  """, unsafe_allow_html=True)

# dynamic navigation component to handle the pages and the dataframes and avoid code repetition (DRY)
def navigation_func(first_page, third_page, fourth_page, fifth_page, import_page, export_page):
  # define the functions for each page and pass the dataframes
  def first_page_func():
    first_page(df_ventas, df_compras, df_inventario, df_coordenadas)

  # def second_page_func():
  #  second_page()

  def third_page_func():
    third_page(df_inventario)

  def fourth_page_func():
    fourth_page()

  def fifth_page_func():
    fifth_page(df_ventas)

  def import_page_func():
    import_page()

  def export_page_func():
    export_page(df_ventas, df_compras, df_inventario, df_coordenadas)

  pages = {
    "Páginas": [
      st.Page(first_page_func, title="Ganancia", icon="💸"),
      # st.Page(second_page_func, title="Chatbot", icon="🤖"),
      st.Page(third_page_func, title="Inventario", icon="📦"),
      st.Page(fourth_page_func, title="Predicciones", icon="📈"),
      st.Page(fifth_page_func, title="Descuentos", icon="🔖"),
    ],
    "Bases de Datos": [
      st.Page(import_page_func, title="Importar", icon="🔼"),
      st.Page(export_page_func, title="Exportar", icon="🔽"),
    ],
  }

  if st.session_state.username == "user":
    pages["Bases de Datos"].pop(0)

  pagination = st.navigation(pages)
  pagination.run()

def admin_interface():

  # call to nav_bar function
  nav_bar()

  # pass the pages to the pagination_func for the admin interface
  navigation_func(admin_first_page, admin_third_page, admin_fourth_page, admin_fifth_page, import_page, export_page)

def user_interface():

  # call to nav_bar function
  nav_bar()

  # pass the pages to the pagination_func for the user interface
  navigation_func(user_first_page, user_third_page, user_fourth_page, user_fifth_page, import_page, export_page)

# if the admin is logged in, show the admin interface, otherwise show the user page
def main_screen():
    if st.session_state.username == "admin":
        admin_interface()
    elif st.session_state.username == "user":
        user_interface()

# check if the user is authenticated, if so, show the main screen, otherwise show the login page
if st.session_state.authenticated:
  main_screen()
else:
  login()
