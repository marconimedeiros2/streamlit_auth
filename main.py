from numpy import place
import pyrebase
import streamlit as st
from datetime import datetime
from io import StringIO

firebaseConfig = {
  'apiKey': "AIzaSyDmaICrJnzE6_mkwsFLwMGDHys-a-5cL1s",
  'authDomain': "streamlit-firebase-mapfre.firebaseapp.com",
  'projectId': "streamlit-firebase-mapfre",
  'databaseURL': "https://streamlit-firebase-mapfre-default-rtdb.firebaseio.com/",
  'storageBucket': "streamlit-firebase-mapfre.appspot.com",
  'messagingSenderId': "132852245968",
  'appId': "1:132852245968:web:231b2521c6870cbbccc5d5",
  'measurementId': "G-TWNT2X9R59"
}

# firebase authentication
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

# database
db = firebase.database()
storage = firebase.storage()

st.set_page_config(page_title="Mapfre arquivos", page_icon="🧊")
st.image("https://upload.wikimedia.org/wikipedia/commons/b/bf/Mapfre_logo.svg", width=200)

placeholder = st.empty()
authenticate = False
user = ''
if ~authenticate:
  with placeholder.form(key="my-form", clear_on_submit=True):
    choice = st.selectbox('Entrar/Registrar', ['Entrar', 'Registrar'])
    email = st.text_input('Informar e-mail')
    password = st.text_input('Informar password', type='password')

    if choice == 'Registrar':
      submit = st.form_submit_button('Registrar')
    
      if submit:
        user = auth.create_user_with_email_and_password(email, password)
        authenticate = True
        placeholder.success('Usuário criado com sucesso')
        placeholder.balloons()
    
    else:
      enter = st.form_submit_button('Entrar')
      if enter:  
        user = auth.sign_in_with_email_and_password(email, password)
        authenticate = True

if user:
  placeholder.empty()
# ---- MAINPAGE ----
  st.title("Aquivo Texto Mapfre")
  st.markdown("""---""")

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
      

    
# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)