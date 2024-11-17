import streamlit as st

from csv_handler import handle_csv
from sheet_handler import handle_google_sheet

st.title("Web Retriever")
if 'loaded_data' not in st.session_state:
    st.session_state['loaded_data'] = False
data_source = st.selectbox("Select Data Source:", options=["Upload CSV", "Connect Google Sheet"])
if data_source == "Upload CSV":
    handle_csv()
elif data_source == "Connect Google Sheet":
    handle_google_sheet()

if 'selected_column' in st.session_state:
    st.success("Data loaded successfully! You can now enter your query.")
    query_box = st.text_area(
        label="Enter the query you want to search for",
        placeholder="Some Query",
        help="Replace the entity you want to search for in {}. Example: Get me the email address of {company}",
        label_visibility='visible'
    )
    st.session_state['query'] = query_box

if 'query' in st.session_state:
    