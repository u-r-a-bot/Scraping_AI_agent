import streamlit as st
import sidebar
from csv_handler import handle_csv
from sheet_handler import handle_google_sheet

st.title("Web Retriever")

data_source = st.selectbox("Select Data Source:", options=["Upload CSV", "Connect Google Sheet"])
sidebar.sidebar()
if data_source == "Upload CSV":
    handle_csv()

elif data_source == "Connect Google Sheet":
    handle_google_sheet()
