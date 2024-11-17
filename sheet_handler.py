import streamlit as st
import auth
import pandas as pd

def handle_google_sheet():

        try:
            credentials = auth.load_credentials()
            auth.authorize_user()
            files = auth.list_all_drive_files()
            file_names = [file['name'] for file in files]
            file_ids = [file['id'] for file in files]

            selected_file_name = st.selectbox("Select a Google Sheet file:", file_names)

            selected_file_id = file_ids[file_names.index(selected_file_name)]
            try:
                sheet_data = auth.open_sheet_by_id(credentials, selected_file_id)
                sheet_df = pd.DataFrame(sheet_data)
                st.write(sheet_df)
                columns = sheet_df.columns
                selected_column = st.pills("Select a column:", columns,selection_mode="single")
                if selected_column:
                    st.session_state['selected_column'] = selected_column
                    st.write(sheet_df[selected_column].head())
                    st.session_state['loaded_data'] = sheet_df[selected_column].tolist()
                    st.session_state['full_data'] = sheet_df
                    st.session_state['credentials'] = credentials
                    st.session_state['sheet_id'] = selected_file_id


            except Exception as e:
                st.error(f"Failed to load data from the selected Google Sheet: {e}")
        except Exception as e:
            st.error(f"Failed to list Google Drive files: {e}")
