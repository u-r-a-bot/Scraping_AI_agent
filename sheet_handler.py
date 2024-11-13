import streamlit as st
import auth


def handle_google_sheet():
    creds_file = st.file_uploader("Upload credentials.json file", type="json")

    @st.cache_resource
    def get_credentials(file_obj):
        return auth.load_credentials(file_obj)

    if creds_file:
        credentials = get_credentials(creds_file)
        st.write("Credentials loaded successfully.")

        try:
            files = auth.list_all_drive_files(credentials)
            file_names = [file['name'] for file in files]
            file_ids = [file['id'] for file in files]

            selected_file_name = st.selectbox("Select a Google Sheet file:", file_names)

            selected_file_id = file_ids[file_names.index(selected_file_name)]

            if st.button("Load Sheet Data"):
                try:
                    sheet_data = auth.open_sheet_by_id(credentials, selected_file_id)
                    headers = sheet_data[0]
                    st.write("Google Sheet Columns:", headers)
                    selected_column = st.selectbox("Select a useful column:", headers)
                    st.write(f"You selected: {selected_column}")
                    st.session_state['selected_column'] = selected_column

                except Exception as e:
                    st.error(f"Failed to load data from the selected Google Sheet: {e}")
        except Exception as e:
            st.error(f"Failed to list Google Drive files: {e}")
