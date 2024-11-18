import os
import json
import gspread
from gspread.auth import OAuthCredentials,Client,FlowCallable,local_server_flow,HTTPClient,HTTPClientType
import streamlit as st
from typing import Optional, Mapping, Iterable, Callable, Tuple,Any, Dict

DEFAULT_SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"

]
file_path = os.path.join(os.getcwd(), 'credentials.json')
def load_credentials(fileobj = file_path, scopes = DEFAULT_SCOPES):
    creds_dict = None
    if isinstance(fileobj, (str, os.PathLike)):
        with open(fileobj, 'r') as f:
            creds_dict = json.load(f)
        return creds_dict
    else:
        file_content = fileobj.read().decode('utf-8')
        creds_dict = json.loads(file_content)
        return creds_dict


def oauth_from_dict(
    credentials: Optional[Mapping[str, Any]] = None,
    authorized_user_info: Optional[Mapping[str, Any]] = None,
    scopes: Iterable[str] = DEFAULT_SCOPES,
    flow: FlowCallable = local_server_flow,
    http_client: HTTPClientType = HTTPClient,
) -> Tuple[Client, Dict[str, Any]]:
    creds  = None
    if authorized_user_info is not None:
        creds = OAuthCredentials.from_authorized_user_info(authorized_user_info, scopes)

    if not creds and credentials is not None:
        creds = flow(client_config=credentials, scopes=scopes)

    client = Client(auth=creds, http_client=http_client)

    return (client, creds.to_json("token"))

@st.cache_resource
def authorize_user(fileobj= file_path):
    file, auth_user = oauth_from_dict(credentials=load_credentials(fileobj))#
    st.session_state['token'] = file

def list_all_drive_files():
    file = st.session_state['token']
    return file.list_spreadsheet_files()

def sheet_object_by_id(credentials, sheet_id):
    client = st.session_state['token']
    sheet = client.open_by_key(sheet_id)
    worksheet = sheet.get_worksheet(0)
    return worksheet

def open_sheet_by_id(credentials, sheet_id):
    client = st.session_state['token']
    sheet = client.open_by_key(sheet_id)
    worksheet = sheet.get_worksheet(0)
    data = worksheet.get_all_records()
    return data



