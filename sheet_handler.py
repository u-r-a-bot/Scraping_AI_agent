import streamlit as st
import auth
import pandas as pd

def handle_google_sheet():
    creds_file = st.file_uploader("Upload credentials.json file", type="json")

    @st.cache_resource
    def get_credentials(file_obj):
        return auth.load_credentials(file_obj)

    if creds_file:
        credentials = get_credentials(creds_file)
        st.write("Credentials loaded successfully.")

        try:

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


            except Exception as e:
                st.error(f"Failed to load data from the selected Google Sheet: {e}")
        except Exception as e:
            st.error(f"Failed to list Google Drive files: {e}")
