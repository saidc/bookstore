
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient import errors
import os.path
import tools
from tools import calcular_rango

def get_token_credentials(TOKEN_FILE, CLIENT_SECRET, SCOPES):

    print("path actual get_token_credentials: ", os.getcwd())
    creds = None 
 
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file( CLIENT_SECRET , scopes=SCOPES ) # 'credentials.json', SCOPES)
            authorization_url, state = flow.authorization_url(
                # Enable offline access so that you can refresh an access token without
                # re-prompting the user for permission. Recommended for web server apps.
                access_type='offline',
                # Enable incremental authorization. Recommended as a best practice.
                include_granted_scopes='true')
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
    return creds

def connect_to_sheet_api(creds):
  try:
    if creds != None or creds.valid:
      #creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
      service = build('sheets', 'v4', credentials=creds)
      return service
    return None
  except Exception as error:
    print(f"An error occurred: {error}")
    return None
  
def get_rows(service=None, spreadsheet_id=None, sheet_name=None):
  try:
    result = service.spreadsheets().values().get( spreadsheetId=spreadsheet_id, range=sheet_name).execute()
    rows = result.get('values', [])
    return rows
  except Exception as error:
    print(f"An error occurred: {error}")
    return None


def append_row_value(service=None, spreadsheet_id=None, sheet_name=None, value=None):
    # Add new row in the Google.
    try:
        values = [value]
        body = {
            'majorDimension': 'ROWS',
            'values': values
        }
        result = service.spreadsheets().values().append(
           spreadsheetId=spreadsheet_id,
           range=sheet_name,
           valueInputOption='USER_ENTERED',
           insertDataOption='INSERT_ROWS',
           body=body
        ).execute()
        msg = f"{(result.get('updates').get('updatedCells'))} cells updated."
        return msg
    except errors.HttpError as error:
        msg = f"An error occurred: {error}"
        print(msg)
        return msg
    except Exception as error:
        msg = f"An error occurred: {error}"
        print(msg)
        return msg
    
def batch_update_row_value(service=None, spreadsheet_id=None, sheet_name=None, row_to_update=None, value=None):
    """
      Update a row in the Google Sheets using the given credentials, spreadsheet ID, range name,
      and row values.
    """
    try:
        col_end = chr(ord('A') + len(value) - 1)
        
        #range_name = f"{sheet_name}!A{row_to_update}:{col_end}{row_to_update}"
        range_name = f"{sheet_name}!"+calcular_rango(row_to_update, len(value))
        
        values = [value]
        data = [
            {
                'range': range_name,
                'values': values
            }
        ]
        body = {
            'valueInputOption': "USER_ENTERED",
            'data': data
        }
        result = service.spreadsheets().values().batchUpdate( spreadsheetId=spreadsheet_id, body=body).execute()
        print(f"{(result.get('totalUpdatedCells'))} cells updated.")
        return result
    except errors.HttpError as error:
        msg = f"An error occurred: {error}"
        print(msg)
        return msg
    except Exception as error:
        print(f"An error occurred: {error}")
        return error

def send_email(creds,SCRIPT_ID,email,asunto,descripcion):
   try:
    service = build('script', 'v1', credentials=creds)
    request = {
       'function': 'enviarCorreoElectronico',
       "parameters": [{"email":email,"asunto":asunto, "descripcion":descripcion}],
       "devMode": True
       }
    response = service.scripts().run( scriptId=SCRIPT_ID, body=request).execute()
    print(response)
   except errors.HttpError as error:
    print(error.content)

def test_get_variables():
    TOKEN_FILE = "token.json"
    CLIENT_SECRET = "credentials.json"
    SCOPES = [
       'https://www.googleapis.com/auth/spreadsheets',
       'https://www.googleapis.com/auth/spreadsheets.readonly',
       'https://www.googleapis.com/auth/drive',
       'https://www.googleapis.com/auth/admin.directory.user',
       'https://www.googleapis.com/auth/script.projects',
       'https://www.googleapis.com/auth/script.send_mail'
       ]
    valores_spreadsheet_id = "1BWo5R_LGFy2ygnx9G_xMmws3hgWHSPN-MtOIy-Ku3EQ"
    valores_sheet_name = "variables"
    creds = get_token_credentials(TOKEN_FILE, CLIENT_SECRET, SCOPES)
    service = connect_to_sheet_api(creds)
    if(service):
       print("conexion exitosa")
       rows = get_rows(service ,valores_spreadsheet_id , valores_sheet_name)
       print(rows)
       index = -1
       for i in range(len(rows)):
          row = rows[i]
          if(row[0]=="count_down"):
             index = i
             break
       if index > 0:
          days_of_count_down_text = rows[index][1]
          seconds_remaining = tools.calculate_seconds_remaining(days_of_count_down_text)
          print("Segundos restantes:", seconds_remaining, " minutos:", int(seconds_remaining/60), " horas", int((seconds_remaining/60)/60) , " dias: ", int(((seconds_remaining/60)/60))/24)
       else:
          print("no se encontro la variable count_down")
    else:
       print("conexion fallida")

#def test_exec():
#    TOKEN_FILE = "token.json"
#    CLIENT_SECRET = "credentials.json"
#    SCOPES = [
#       'https://www.googleapis.com/auth/spreadsheets',
#       'https://www.googleapis.com/auth/spreadsheets.readonly',
#       'https://www.googleapis.com/auth/drive',
#       'https://www.googleapis.com/auth/admin.directory.user',
#       'https://www.googleapis.com/auth/script.projects',
#       'https://www.googleapis.com/auth/script.send_mail'
#       ]
#    email = "sayacorcal@gmail.com"
#    asunto = "correo test from bookstore "
#    descripcion = "descripcion test bookstore tienda el niño aquel"
#    SCRIPT_ID = "AKfycbwcHByCWYAlcyCNTXXzi_GDklb52oNZo3UJlDWjesDCj5tZIs_xFOobKW1Xdb1zrlSr"
#    creds = get_token_credentials(TOKEN_FILE, CLIENT_SECRET, SCOPES)
#    send_email(creds,SCRIPT_ID,email,asunto,descripcion)

#   TOKEN_FILE = "token.json"
#   CLIENT_SECRET = "credentials.json"
#   SCOPES = [
#       "https://www.googleapis.com/auth/spreadsheets",
#       "https://www.googleapis.com/auth/spreadsheets.readonly",
#       'https://www.googleapis.com/auth/drive']
#   spreadsheet_id = "1W2aORxcsPE6gdJdC7AttwrsNd_PMScjw2UlkLwsUVl0"
#   sheet_name = "pedidos_1"
#   creds = get_token_credentials(TOKEN_FILE, CLIENT_SECRET, SCOPES)
#   service = connect_to_sheet_api(creds)
#   if(service):
#       print("conexion exitosa")
#                   # 'id',           'nombre',         'precio', 'direccion',         'correo ',               'ciudad'
#       new_row = [ "elniñoaquel",  "El niño aquel",  80000,    "calle 20b#11-39",   "sayacorcal@gmail.com",  "Barranquilla" ]
#       #append_row_value(service, spreadsheet_id, sheet_name, new_row)
#       batch_update_row_value(service, spreadsheet_id, sheet_name, row_to_update=2, value=new_row)
#       rows = get_rows(service ,spreadsheet_id , sheet_name)
#       print(rows)
#   else:
#       print("conexion fallida")
