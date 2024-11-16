import os
import json
import gspread
import streamlit as st

scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"

]
file_path = "C:\\Users\\PhantomGrogu\\Documents\\Submission\\creds.json"
def load_credentials(fileobj , scopes = scopes):
    creds_dict = None
    if isinstance(fileobj, (str, os.PathLike)):
        with open(fileobj, 'r') as f:
            creds_dict = json.load(f)
        return creds_dict
    else:
        file_content = fileobj.read().decode('utf-8')
        creds_dict = json.loads(file_content)
        return creds_dict

@st.cache_resource
def authorize_user(fileobj= file_path):
    file, auth_user = gspread.oauth_from_dict(credentials=load_credentials(fileobj))# Changed source for cred error
    st.session_state['token'] = file

def list_all_drive_files():
    file = st.session_state['token']
    return file.list_spreadsheet_files()

def open_sheet_by_id(credentials, sheet_id):
    client = st.session_state['token']
    sheet = client.open_by_key(sheet_id)
    worksheet = sheet.get_worksheet(0)
    data = worksheet.get_all_records()
    return data



