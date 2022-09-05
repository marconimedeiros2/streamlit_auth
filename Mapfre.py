import pyrebase
import streamlit as st
import pandas as pd
import pandas
from st_aggrid import AgGrid, GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder

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
    
# download dataframe
@st.cache
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv(sep=';', encoding='latin1', header=True, decimal=',')

# editable table
def editable_df(df):
  gd = GridOptionsBuilder.from_dataframe(df)
  gd.configure_pagination(enabled=True)
  gd.configure_default_column(editable=True, groupable=True, headerCheckboxSelection=True)
  
  sel_mode = st.radio('Selecione o tipo', options=['single','multiple'])
  gd.configure_selection(selection_mode=sel_mode, use_checkbox=True)
  grid_options = gd.build()
  # grid_table = AgGrid(df, theme='dark', try_to_convert_back_to_original_types=False, gridOptions=grid_options, update_mode= GridUpdateMode.SELECTION_CHANGED | GridUpdateMode.VALUE_CHANGED, allow_unsafe_jscode=True, height=500 )
  # sel_row = grid_table['selected_rows']
  
  # df_grid = pd.DataFrame(sel_row)
  
  csv = convert_df(df)
  st.download_button(
    label="Download tabela modificada como CSV",
    data=csv,
    file_name='dados_alterados.csv',
    mime='text/csv',  
  )
  st.subheader('Linhas atualizadas: ')
  # st.table(data=df_grid)
    
  








def x():
  from google.colab import drive
  import pandas 
  drive.mount('/content/drive/')

  import pandas

  dfTxtInput = pandas.read_csv('/content/drive/MyDrive/beAnalytic/MAPFRE/731Leao Moveis03032022636.TXT', encoding='unicode_escape', delimiter='\n', header=None)
  dfTxtInput['Tipo do Registro'] = dfTxtInput[0].str[:2]
  dfTxtInput['Tipo do Registro'] = dfTxtInput['Tipo do Registro'].astype(int)
  dfTxtInput.columns = ['Coluna', 'Tipo do Registro']
  dfTxtInput

  arquivo = pandas.ExcelFile('https://docs.google.com/spreadsheets/d/e/2PACX-1vT1xXjTF3sn4EvdNoJY0VO1o-8aSoGGabwUNvVGkI760QW4naMHAHt-iABIeEtT3g/pub?output=xlsx')

  modelosDicionario = {}
  modelosDicionario[0] = pandas.read_excel(arquivo, sheet_name='Header').dropna(subset=['Campo']).to_json(orient='records') # Header
  modelosDicionario[1] = pandas.read_excel(arquivo, sheet_name='Detalhe Adesão|Cancelamento').dropna(subset=['Campo']).to_json(orient='records') # Detalhe Adesão|Cancelamento
  modelosDicionario[99] = pandas.read_excel(arquivo, sheet_name='Trailer').dropna(subset=['Campo']).to_json(orient='records') # Trailer

  arquivo = pandas.ExcelFile('https://docs.google.com/spreadsheets/d/e/2PACX-1vTTjAV0veqw_oLMlihU3pnVBwU83r5KREBs2acCUbljiKOsBqS1ACptn03uQzWzoQ/pub?output=xlsx')

  modelosDicionarioOutput = {}
  modelosDicionarioOutput[0] = pandas.read_excel(arquivo, sheet_name='Header').dropna(subset=['Campo']).to_json(orient='records')
  modelosDicionarioOutput[1] = pandas.read_excel(arquivo, sheet_name='Dados da Apólice').dropna(subset=['Campo']).to_json(orient='records')
  modelosDicionarioOutput[2] = pandas.read_excel(arquivo, sheet_name='Tomador_Segurado').dropna(subset=['Campo']).to_json(orient='records')
  modelosDicionarioOutput[8] = pandas.read_excel(arquivo, sheet_name='Dados Variáveis EQ 770').dropna(subset=['Campo']).to_json(orient='records')
  modelosDicionarioOutput[95.1] = pandas.read_excel(arquivo, sheet_name='Dados de Cobertura').dropna(subset=['Campo']).to_json(orient='records')
  modelosDicionarioOutput[95.2] = pandas.read_excel(arquivo, sheet_name='Dados de Cobertura').dropna(subset=['Campo']).to_json(orient='records')
  modelosDicionarioOutput[96] = pandas.read_excel(arquivo, sheet_name='Dados de Cobrança').dropna(subset=['Campo']).to_json(orient='records')
  modelosDicionarioOutput[99] = pandas.read_excel(arquivo, sheet_name='Trailler').dropna(subset=['Campo']).to_json(orient='records')

  dadosInput = {}

  for indexInput, linhaInput in dfTxtInput.iterrows(): #olhando linha a linha do modelo input 731

    if linhaInput['Tipo do Registro'] in [0, 99]:
      tipo = linhaInput['Tipo do Registro']
      modelo = modelosDicionario[tipo] #pegando o modelo do dicionario com base em casa linha do input 731
      dfModeloTemp = pandas.read_json(modelosDicionario[tipo], orient='records')
      dadosInput[tipo] = {}
    else:
      tipo = indexInput
      modelo = modelosDicionario[1] #pegando o modelo do dicionario com base em casa linha do input 731
      dfModeloTemp = pandas.read_json(modelosDicionario[1], orient='records')
      dadosInput[tipo] = {}
    
    for indexModelo, linhaModelo in dfModeloTemp.iterrows():
      chave = linhaModelo['Campo'].strip()

      # if linhaModelo['Tam'] == "N":
        # valor = str(linhaInput['Coluna'][int(linhaModelo['De'])-1:int(linhaModelo['Até'])]).zfill(linhaInput['Tam'])
      # else:
      valor = linhaInput['Coluna'][int(linhaModelo['De'])-1:int(linhaModelo['Até'])]
      
      dadosInput[tipo][chave] = valor

      if dadosInput[tipo]['Tipo do Registro'] == '00':
        dadosInput[tipo]['Total de Registros Enviados'] = str(dfTxtInput.shape[0]).zfill(7) #menos o head e trailer
        dadosInput[tipo]['Total de Certificados Enviados'] = str(dfTxtInput.shape[0] - 2).zfill(7) #menos o head e trailer
        dadosInput[tipo]['Total de Itens Enviados'] = str(dfTxtInput.shape[0] - 2).zfill(7) #menos o head e trailer
        dadosInput[tipo]['Número Sequencial do Registro (header)'] = '0000001'

      elif dadosInput[tipo]['Tipo do Registro'] == '01':
        try:
          dadosInput[tipo]['Produto'] = '0007'
          dadosInput[tipo]['Tipo de Emissão'] = 'R'
          dadosInput[tipo]['Tipo de Apólice'] = 'F'
          dadosInput[tipo]['Codigo de Moeda'] = '01'
          dadosInput[tipo]['Tipo de Coseguro'] = '0'
          dadosInput[tipo]['Data de Início de Vigência'] = str(dadosInput[tipo].get('Data de Início de Vigência')).replace('/', '')
          dadosInput[tipo]['Data de Final de Vigência'] = str(dadosInput[tipo].get('Data de Final de Vigência')).replace('/', '')
          dadosInput[tipo]['Código de Negócio'] = '2'
          dadosInput[tipo]['Codigo do Corretor'] = '44373'
          dadosInput[tipo]['Código da Sucursal'] = '0'
          dadosInput[tipo]['Tipo de Pessoa'] = 'J'
          dadosInput[tipo]['Data de Nascimento'] = '00000000'
          dadosInput[tipo]['Sexo'] = '0'
          dadosInput[tipo]['Profissão'] = '99999'
          dadosInput[tipo]['Ocupação'] = '99999'
          dadosInput[tipo]['Tipo de Logradouro'] = '1 '
          dadosInput[tipo]['Endereço Logradouro'] = 'Rua Capitão Jose Maria                                      '
          dadosInput[tipo]['Endereço Número'] = '1071      '
          dadosInput[tipo]['Endereço Complemento'] = '          '
          dadosInput[tipo]['Endereço Bairro'] = 'Centro               '
          dadosInput[tipo]['Endereço Cidade'] = 'Linhares            '
          dadosInput[tipo]['Endereço CEP'] = '29900171'
          dadosInput[tipo]['Endereço UF'] = 'ES'
          dadosInput[tipo]['Telefone para contato - DDD'] = '0021'
          dadosInput[tipo]['Telefone para contato - Número'] = '88020288'
          dadosInput[tipo]['Estado Civil'] = '0'
          dadosInput[tipo]['Código da Atividade Econômica'] = '          52.42-6-01'
          dadosInput[tipo]['Tipo de Documento'] = ''
          dadosInput[tipo]['Número do Documento'] = ''
          dadosInput[tipo]['Orgão Expedidor'] = ''
          dadosInput[tipo]['UF do Orgão Expedidor'] = ''
          dadosInput[tipo]['Data da Expedição'] = '01012000'
          dadosInput[tipo]['Faixa de Renda'] = '01'
          dadosInput[tipo]['País de Residência'] = 'BRASIL'
          dadosInput[tipo]['Data de Nascimento (Cliente)'] = '01011990'
          dadosInput[tipo]['Sexo (Cliente)'] = '0'
          dadosInput[tipo]['Profissão (Cliente)'] = '99999'
          dadosInput[tipo]['Ocupação (Cliente)'] = '99999'
          dadosInput[tipo]['Tipo de Logradouro (Cliente)'] = '1 '
          dadosInput[tipo]['Estado Civil (Cliente)'] = '0'
          dadosInput[tipo]['Código da Atividade Econômica (Cliente)'] = '52.42-6-01'
          dadosInput[tipo]['Tipo de Documento (Cliente)'] =  str(dadosInput[tipo].get('Tipo de Documento (Cliente)')).replace('_', ' ')
          dadosInput[tipo]['Data da Expedição (Cliente)'] =  '01012000'
          dadosInput[tipo]['Faixa de Renda (Cliente)'] =  '01'
          dadosInput[tipo]['UF do Orgão Expedidor (Cliente)'] =  'SP'
          dadosInput[tipo]['Código do Revendedor / Estipulante (completo)'] =  str(int(dadosInput[tipo].get('Código do Revendedor / Estipulante (completo)')))
          
          dadosInput[tipo]['Numero do Item'] =  '000001' #fixo??
          dadosInput[tipo]['Número da Proposta'] =  '00000096060715' #nao foi encontrado no 731
          dadosInput[tipo]['Número do Certificado'] =  str(dadosInput[tipo].get('Número do Certificado (Cliente)'))
          dadosInput[tipo]['Data da Proposta'] =  str(dadosInput[tipo].get('Data de Início de Vigência')) #precisa colocar 30 dias a mais
          dadosInput[tipo]['Código do Convênio/Banco'] =  ''
          dadosInput[tipo]['Identificador do Convênio'] =  ''
          dadosInput[tipo]['Comissão'] =  '54.01' #fixo??
          dadosInput[tipo]['Custo de Apólice'] =  '' 
          dadosInput[tipo]['Número da Proposta Convênio'] =  str(dadosInput[tipo].get('Número da Proposta')) #igual ao numero da proposta?!
          dadosInput[tipo]['Número de Série'] =  ''
          dadosInput[tipo]['Número do Sorteio'] =  ''
          dadosInput[tipo]['Perfil'] =  '00' #fixo?
          dadosInput[tipo]['PLANO DE CONTRATACAO'] =  '0000000001'
          dadosInput[tipo]['DESCRICAO DO RISCO'] =  'SMARTPHONE' #não foi encontrado no 731
          dadosInput[tipo]['NOME DO FABRICANTE'] =  '' 
          dadosInput[tipo]['MODELO DO BEM'] =  ''  #NÃO DEVERIA SER 1, DE ACORDO COM AS INSTRUÇÕES?
          dadosInput[tipo]['DESCRICAO MODELO DO BEM'] =  'G3 - D855P'  #FIXO?????
          dadosInput[tipo]['TIPO DO BEM'] =  '02'  #FIXO?????
          dadosInput[tipo]['NUMERO DA NOTA FISCAL'] =  str(dadosInput[tipo].get('Número da Nota Fiscal ou Cupon Fiscal')).replace('/', '')
          dadosInput[tipo]['DATA NOTA FISCAL'] =  str(dadosInput[tipo].get('Data da Venda da Garantia Estendida')).replace('/', '')
          dadosInput[tipo]['CODIGO SERIAL DO APARELHO'] =  ''  #NAÕ FOI ENCONTRADO NO 731
          dadosInput[tipo]['RISCO FACULTATIVO (S/N)'] =  'N'  

          dadosInput[tipo]['Código da Cobertura'] =  '447' #é isso mesmo? não tem na tabela   
          dadosInput[tipo]['Prêmio Líquido'] =  '' #não tem no 731 
          dadosInput[tipo]['Código da Franquia'] =  '' #não tem no 731 
          dadosInput[tipo]['Valor da Franquia'] =  '' #tá errado, n?
          dadosInput[tipo]['Valor P.O.S'] =  '' #não tem no 731
          dadosInput[tipo]['Carência'] =  '' #não identificamos no 731

          dadosInput[tipo]['Tipo de Gestor de Cobrança'] =  'DF' #esse valor fixo? ou outra opção?
          dadosInput[tipo]['Código do Plano de Pagamento'] =  '723' #não tem no 731 
          dadosInput[tipo]['Código do Gestor de Pagamento'] =  '99990319' #não tem no 731 
          dadosInput[tipo]['Tipo de Documento'] =  'CGC' #esse valor fixo? não tem no 731 
          dadosInput[tipo]['Vencimento da Primeira Parcela'] =  str(dadosInput[tipo].get('Vencimento da Primeira Parcela')).replace('/', '')
          dadosInput[tipo]['Dia de Vencimento das Parcelas'] =  '28' #esse valor fixo? 
          dadosInput[tipo]['Bandeira'] =  '' #não tem no 731 
          dadosInput[tipo]['Número do Cartão'] =  '' #não tem no 731 
          dadosInput[tipo]['Validade do Cartão'] =  '' #não tem no 731 
          dadosInput[tipo]['Código de Segurança'] =  '' #não tem no 731 
          dadosInput[tipo]['Gestor FCA'] =  '' #não tem no 731 
          dadosInput[tipo]['Número FCA'] =  '' #não tem no 731 
          dadosInput[tipo]['Valor da FCA'] =  '' #não tem no 731 
        
        except:
          pass

        
        
      elif dadosInput[tipo]['Tipo do Registro'] == '99':
        dadosInput[tipo]['Total de Registros Enviados'] = str(dfTxtInput.shape[0]).zfill(7) #menos o head e trailer
        dadosInput[tipo]['Total de Certificados Enviados'] = str(dfTxtInput.shape[0] - 2).zfill(7) #menos o head e trailer
        dadosInput[tipo]['Total de Itens Enviados'] = str(dfTxtInput.shape[0] - 2).zfill(7) #menos o head e trailer

  dadosInput

  dadosOutput = {}

  for tipoRegistro in modelosDicionarioOutput:
    vetorUpload = []
    
    if tipoRegistro in [0, 99]: # se for HEADER ou TRAILER
      dadosOutput[tipoRegistro] = {}
      dfModeloTemp = pandas.read_json(modelosDicionarioOutput[tipoRegistro], orient='records')
      for indexModelo, linhaModelo in dfModeloTemp.iterrows():
        
        chave = linhaModelo['Campo'].strip()
        valor = dadosInput[tipoRegistro][chave]

        # print(chave, valor)

        if chave == 'Tipo do Registro':
          valor = str(tipoRegistro).zfill(2)

        vetorUpload.append(valor)
        # print(vetorUpload)
      linhaOutput = "".join(vetorUpload)
      print(linhaOutput)
      dadosOutput[tipoRegistro] = linhaOutput

  for indexInput, col in dfTxtInput.iterrows():
    vetorFinal = []
    if col['Tipo do Registro'] not in [0, 99]:
      # print('indexInput', indexInput)
      for tipoRegistro in modelosDicionarioOutput:
        vetorUpload = []
        
        if tipoRegistro not in [0, 99]: # se não for HEADER ou TRAILER

          dadosInputFull = dict(dadosInput[indexInput].items() | dadosInput[0].items())
          dfModeloTemp = pandas.read_json(modelosDicionarioOutput[tipoRegistro], orient='records')
          dfModeloTemp[['Tam', 'De', 'Até']] = dfModeloTemp[['Tam', 'De', 'Até']].astype(int)
          for indexModelo, linhaModelo in dfModeloTemp.iterrows():
            chave = linhaModelo['Campo'].strip()
            
            ignorarFormatacao = ['RISCO FACULTATIVO (S/N)', 'DESCRICAO MODELO DO BEM','Descrição do Produto', 'DESCRICAO DO RISCO', 'NOME DO FABRICANTE', 'Número do Sorteio', 'Número de Série', 'Código da Atividade Econômica', 'Código do Revendedor / Estipulante (completo)', 'Nome da Revendedor / Estipulante', 'Tipo de Logradouro', 'Endereço Logradouro', 'Endereço Número', 'Endereço Complemento', 'Endereço Bairro', 'Endereço Cidade', 'Endereço CEP', 'Endereço UF', 'Telefone para contato - DDD', 'Telefone para contato - Número', 'Estado Civil', 'Código da Atividade Econômica', 'Tipo de Documento', 'Número do Documento', 'Orgão Expedidor', 'UF do Orgão Expedidor', 'Data da Expedição', 'Faixa de Renda', 'País de Residência', 'Nome do Segurado / Tomador (Cliente)', 'Tipo de Logradouro (Cliente)', 'Endereço Cidade (Cliente)', 'Endereço Bairro (Cliente)', 'Endereço Complemento (Cliente)', 'Endereço Número (Cliente)', 'Endereço Logradouro (Cliente)', 'Tipo de Documento (Cliente)', 'País de Residência (Cliente)']
            if chave in ignorarFormatacao:
              valor = str(dadosInputFull[chave][:int(linhaModelo['Tam'])].strip().ljust(linhaModelo['Tam']))
            else:
              valor = str(dadosInputFull[chave][:int(linhaModelo['Tam'])].strip().zfill(linhaModelo['Tam']))
            
            # print(chave, valor, linhaModelo['Tipo'])


            if chave == 'Tipo do Registro':
              valor = str(tipoRegistro).zfill(2)[:2]

            vetorUpload.append(valor)
            # print(vetorUpload)
          linhaOutput = "".join(vetorUpload)
          vetorFinal.append(linhaOutput)
          # print(linhaOutput)
          # print()
          print(linhaOutput)
          dadosOutput[col['Tipo do Registro']] = vetorFinal
    
    dadosOutput = dict(sorted(dadosOutput.items()))
  return dadosOutput


















if st.session_state.key:
  placeholder.empty()
  c = st.container()
  # ---- MAINPAGE ----
  c.title("Arquivo Texto Mapfre")
  c.markdown("""---""")

  uploaded_file = c.file_uploader("Escolha o arquivo TXT/CSV", type=["txt", "csv"], on_change=None, key="my-file", accept_multiple_files=False)

  if uploaded_file:
    df = pd.read_csv(uploaded_file, sep=";", encoding='latin-1')
    
    df = x(df)
    editable_df(df)
    out = df.to_json(orient='records')[1:-1]
  

