import pandas as pd
import streamlit as st

import auth
from util_agent import LangChainAgent
from csv_handler import handle_csv
import re
import json
from sheet_handler import handle_google_sheet

st.secrets.load_if_toml_exists()
st.title("Web AI Agent ")

agent = LangChainAgent(st.secrets['GroqAPI'], st.secrets['SerpAPI_key'])

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
        help="Replace the entity you want to search for in {}. Example: Get me the email address of {Company}",
        label_visibility='visible'
    )
    if query_box.strip():
        selected_data = st.session_state['loaded_data']
        place_holder = re.findall(r'\{(.*?)\}', query_box)[0]
        queries_with_entities = [query_box.replace(f"{{{place_holder}}}", entity) for entity in selected_data]
        st.session_state['queries'] = queries_with_entities

        st.success("Query is valid. Proceeding with the search!")

    else:

        st.warning("Please enter a query to proceed.")


if 'queries' in st.session_state:
    search_results = {}

    loaded_data = st.session_state['loaded_data']
    queries = st.session_state['queries']

    if len(queries) == len(loaded_data):
        with st.status("Searching"):
            for entity, query in zip(loaded_data, queries):
                st.write(f"Searching for: {query}")
                search_results[entity] = agent.fetch_search_results(query)

        st.session_state['search_results'] = search_results

    else:
        st.warning("The number of queries does not match the number of entities. Please check your inputs.")


if 'search_results' in st.session_state and 'queries' in st.session_state:
    base_prompt = st.text_input(
        label='LLM Prompt',
        placeholder="Enter prompt",
        help="Use placeholder like {entity} for entity-specific prompts.",
        label_visibility='visible'
    )

    if base_prompt:
        llm_results = {}

        placeholder = re.findall(r'\{(.*?)\}', base_prompt)

        if placeholder:
            placeholder = placeholder[0]

            if len(st.session_state['queries']) == len(st.session_state['search_results']):
                for entity, search_data in st.session_state['search_results'].items():

                    query = st.session_state['queries'][list(st.session_state['search_results'].keys()).index(entity)]
                    prompt = base_prompt.replace(f"{{{placeholder}}}" , entity)
                    full_input = f"{prompt}\n\nSearch Results:\n{search_data}"


                    response = agent.extract_info_with_prompt(search_data, prompt)

                    llm_results[entity] = response


                st.session_state['llm_results'] = llm_results
            else:
                st.warning(
                    "The number of queries does not match the number of search results. Please check your inputs.")
        else:
            st.warning(
                "No placeholders found in the prompt. Please ensure the prompt contains a placeholder like {entity}.")

if 'llm_results' in st.session_state:
    llm_results = st.session_state['llm_results']
    data_dict = {}
    entities = st.session_state['loaded_data']

    for entity in entities:

        try:

            result_dict = json.loads(llm_results[entity])


            data_dict[entity] = [value for key, value in result_dict.items()]
        except json.JSONDecodeError:

            st.warning(f"Failed to decode JSON for {entity}. Skipping this entity.")
            data_dict[entity] = [None]

    selected_column = st.session_state['selected_column']
    series_dict = pd.Series(data_dict,name='results')
    data_df = st.session_state['full_data']
    merged_df = pd.merge(data_df, series_dict, left_on= st.session_state['selected_column'],right_index=True, how='left')
    if data_source == "Connect Google Sheet":
        if st.button('Update to Google sheet'):
            def convert_list_to_string(cell):
                if isinstance(cell, list):
                    return ', '.join(cell)
                return cell



            processed_df = merged_df.applymap(convert_list_to_string)

            worksheet = auth.sheet_object_by_id(st.session_state['credentials'], st.session_state['sheet_id'])
            worksheet.update([processed_df.columns.tolist()] + processed_df.values.tolist())

    st.write(merged_df)

