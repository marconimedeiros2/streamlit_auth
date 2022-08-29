import streamlit as st 
import pandas as pd
from gsheetsdb import connect
import pyrebase
from google.oauth2 import service_account
import webbrowser

# Disable certificate verification (Not necessary always)
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

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


# initialize state
if 'key' not in st.session_state:
  st.session_state.key = False

placeholder = st.empty()
user = ''
if ~st.session_state.key:
  try:
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
  except ValueError:
    st.error('Verifique os dados: email e senha', icon="⚠️")
    user = ''
    st.session_state.key = False
    placeholder.empty()
    
def onClickHandle():
  url = 'https://docs.google.com/spreadsheets/d/1AojpoaM8_S1xIjXku3yAkut7zQx_9rb5ahHz5dWXevg/edit?usp=sharing'
  webbrowser.open_new_tab(url)

# download dataframe
@st.cache
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv(sep=';', encoding='utf-8', header=True, decimal=',')

# Perform SQL query on the Google Sheet.
# Uses st.cache to only rerun when the query changes or after 10 min.
@st.cache(ttl=600)
def run_query(query):
  rows = conn.execute(query, headers=1)
  rows = rows.fetchall()
  return rows

data_list = []
# Create a connection object.
credentials = service_account.Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=["https://www.googleapis.com/auth/spreadsheets"])
conn = connect(credentials=credentials)
df = pd.DataFrame()
if st.session_state.key:
  placeholder.empty()
  c = st.container()
  # ---- MAINPAGE ----
  c.title("Accesso a Planilha Google Sheet")
  c.markdown("""---""")
  col1, col2 = c.columns(2)
  with col1:  
    open_table = st.button('Inserir Dados', key='data_intro', on_click=onClickHandle)
    
  if open_table:
      sheet_url = st.secrets["private_gsheets_url"]
      rows = run_query(f'SELECT * FROM "{sheet_url}"')
      # Print results.
      for row in rows:
        data_list.append(row)
  # ---- MAINPAGE ----
  c.title("Planilha do GoogleSheet")
  c.markdown("""---""")
  df = pd.DataFrame(data_list)
  st.table(data=df)
  with col2:
    csv = convert_df(df)
    st.download_button(label="Download o GoogleSheet em formato csv", data=csv,file_name='google_sheet.csv', mime='text/csv')

