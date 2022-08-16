import pickle
from pathlib import Path

import pandas as pd  # pip install pandas openpyxl
import streamlit as st  # pip install streamlit
import streamlit_authenticator as stauth  # pip install streamlit-authenticator
from io import StringIO

# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Mapre arquivos", page_icon=":bar_chart:", layout="wide")


# --- USER AUTHENTICATION ---
names = ["Felipe Lisboa", "Marconi Medeiros"]
usernames = ['flisboa', 'mmedeiros']

# load hashed passwords
file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)

authenticator = stauth.Authenticate(names, usernames, hashed_passwords, "Mapfre arquivos", "admin") # , cookie_expiry_days=30

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status == False:
    st.error("Username/password é inválido")

if authentication_status == None:
    st.warning("Informe seu nome de usuário e password")

if authentication_status:
    # ---- UPLOAD FILE ----
    uploaded_file = st.file_uploader("Escolha o arquivo TXT")
    if uploaded_file is not None:
     # To read file as bytes:
     bytes_data = uploaded_file.getvalue()
     st.write(bytes_data)

     # To convert to a string based IO:
     stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
     st.write(stringio)

     # To read file as string:
     string_data = stringio.read()
     st.write(string_data)

    # ---- SIDEBAR ----
    authenticator.logout("Logout", "sidebar")
    st.sidebar.title(f"Bem Vindo {name}")
    
    # ---- MAINPAGE ----
    st.title("Aquivo Texto Mapfre")
        
    st.markdown("""---""")

    
    # ---- HIDE STREAMLIT STYLE ----
    hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
    st.markdown(hide_st_style, unsafe_allow_html=True)