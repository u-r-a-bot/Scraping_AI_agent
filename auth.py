import os
import json
import gspread
import typing
from oauth2client.service_account import ServiceAccountCredentials

scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"

]
file_path = 'C:\\Users\\PhantomGrogu\\Documents\\Submission\\secret-key.json'
def load_credentials(file_path_or_obj = file_path, scopes=scopes):
    if isinstance(file_path_or_obj, (str, os.PathLike)):
        creds = ServiceAccountCredentials.from_json_keyfile_name(file_path_or_obj, scopes)
    else:
        file_content = file_path_or_obj.read().decode('utf-8')
        creds_dict = json.loads(file_content)
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scopes)
    return creds
def list_all_drive_files(credentials: ServiceAccountCredentials ):
    file = gspread.authorize(credentials = credentials)
    return file.list_spreadsheet_files()

def open_sheet_by_id(credentials, sheet_id):
    client = gspread.authorize(credentials)
    sheet = client.open_by_key(sheet_id)
    worksheet = sheet.get_worksheet(0)
    data = worksheet.get_all_records()
    return data


file = gspread.authorize(load_credentials())
print(file.list_spreadsheet_files(file))
# workbook = file.open('Student_info')
# sheet = workbook.sheet
# from googleapiclient.discovery import build
# from google.oauth2.service_account import Credentials
#
# def list_all_drive_files_v2(credentials: ServiceAccountCredentials):
#     # Create the Drive API service
#     drive_service = build('drive', 'v3', credentials=credentials)
#
#     # Request the list of files (including files that are not Google Sheets)
#     results = drive_service.files().list(
#         q="mimeType='application/vnd.google-apps.spreadsheet'",  # Only Google Sheets
#         spaces='drive'
#     ).execute()
#
#     items = results.get('files', [])
#     if not items:
#         print("No Google Sheets files found.")
#     else:
#         print(f"Found {len(items)} Google Sheets files.")
#         for item in items:
#             print(f"File Name: {item['name']}, File ID: {item['id']}")
#     return items
# list_all_drive_files_v2(load_credentials())


