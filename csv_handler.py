import streamlit as st
import pandas as pd


def handle_csv():
    with st.expander("Upload a CSV file"):
        uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
        if uploaded_file:
            st.write("CSV file uploaded successfully.")
            try:
                df = pd.read_csv(uploaded_file)
                st.write(df.head())
                columns = df.columns.tolist()
                selected_column = st.pills("Select a column:", columns, selection_mode="single")
                if selected_column:
                    st.write(df[selected_column].head())
                    st.session_state['selected_column'] = selected_column
                    st.session_state['loaded_data'] = df[selected_column].tolist()
                    st.session_state['full_data'] = df
            except Exception as e:
                st.error(f"Failed to load CSV file: {e}")
