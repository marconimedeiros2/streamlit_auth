from cgi import print_environ
from re import sub
from numpy import place
import pyrebase
import streamlit as st
from datetime import datetime
from io import StringIO
# import firebaseConfig as fc
import pandas as pd

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

# initialize state
if 'key' not in st.session_state:
  st.session_state.key = False

user = ''
if ~st.session_state.key:
  with placeholder.form(key="my-form"):
    options = st.selectbox('Entrar/Registrar', ['Entrar', 'Registrar'])
    email = st.text_input('Informar e-mail')
    password = st.text_input('Informar password', type='password')
    
    if options:
      submit = st.form_submit_button('Enviar')
      if submit:
        st.session_state.key = True
        if(options == 'Registrar'):
          #Signup 
          user = auth.create_user_with_email_and_password(email, password)
          st.success('Usuário criado com sucesso')
          st.balloons()
        else:
          # Login
          user = auth.sign_in_with_email_and_password(email, password)
          db.child(user['localId']).child("Handle").set(email)
          db.child(user['localId']).child("ID").set(user['localId'])
          
if st.session_state.key:
  placeholder.empty()
  c = st.container()
  # ---- MAINPAGE ----
  c.title("Aquivo Texto Mapfre")
  c.markdown("""---""")

  uploaded_file = c.file_uploader("Escolha o arquivo TXT/CSV", type=["txt", "csv"], on_change=None, key="my-file", accept_multiple_files=False)

  if uploaded_file:
    print('subiu arquivo')
    # c.write("Arquivo selecionado: " + uploaded_file)
    df = pd.read_csv(uploaded_file, sep=";", encoding='latin-1')
    c.write(df)


