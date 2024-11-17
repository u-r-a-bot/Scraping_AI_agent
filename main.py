import streamlit as st
from util_agent import LangChainAgent
from csv_handler import handle_csv
import re
from sheet_handler import handle_google_sheet

st.secrets.load_if_toml_exists()
st.title("Web Retriever")

# Initialize the agent
agent = LangChainAgent(st.secrets['GroqAPI'], st.secrets['SerpAPI_key'])

# Manage session state for data
if 'loaded_data' not in st.session_state:
    st.session_state['loaded_data'] = False

# Step 1: Data Source Selection
data_source = st.selectbox("Select Data Source:", options=["Upload CSV", "Connect Google Sheet"])
if data_source == "Upload CSV":
    handle_csv()
elif data_source == "Connect Google Sheet":
    handle_google_sheet()

# Step 2: Query Input
if 'selected_column' in st.session_state:
    st.success("Data loaded successfully! You can now enter your query.")

    # Display a text area for the user to enter the query
    query_box = st.text_area(
        label="Enter the query you want to search for",
        placeholder="Some Query",
        help="Replace the entity you want to search for in {}. Example: Get me the email address of {Company}",
        label_visibility='visible'
    )
    # Check if the query is not empty
    if query_box.strip():
        # Now we replace `{Company}` in the query with the actual entity from the selected column
        selected_data = st.session_state['loaded_data']  # assuming it's a list of companies or entities
        place_holder = re.findall(r'\{(.*?)\}', query_box)[0]
        # Loop through selected data (the entities) and replace the placeholder
        queries_with_entities = [query_box.replace(f"{{{place_holder}}}", entity) for entity in selected_data]

        # Store the queries in session state
        st.session_state['queries'] = queries_with_entities

        st.success("Query is valid. Proceeding with the search!")

        # Optionally display the processed queries
        st.write("Processed queries:", queries_with_entities)
    else:
        # Optionally, display a message to prompt the user to enter a query
        st.warning("Please enter a query to proceed.")


# Step 3: Perform Searches
if 'queries' in st.session_state:  # Check if queries exist in session state
    search_results = {}  # Use a dictionary to store results for each entity

    # Ensure 'loaded_data' is in the correct format (list of entities)
    loaded_data = st.session_state['loaded_data']
    queries = st.session_state['queries']

    # Ensure that the number of queries matches the number of entities
    if len(queries) == len(loaded_data):
        # Iterate over the entities and corresponding queries
        for entity, query in zip(loaded_data, queries):
            st.write(f"Searching for: {query}")  # Debugging/logging
            search_results[entity] = agent.fetch_search_results(query)

        # Store results in session state
        st.session_state['search_results'] = search_results
        st.write("Search Results:", search_results)

    else:
        st.warning("The number of queries does not match the number of entities. Please check your inputs.")

# Step 4: Extract Information Using LLM

if 'search_results' in st.session_state and 'queries' in st.session_state:
    base_prompt = st.text_input(
        label='LLM Prompt',
        placeholder="Enter prompt",
        help="Use placeholder like {entity} for entity-specific prompts.",
        label_visibility='visible'
    )

    if base_prompt:
        llm_results = {}

        # Extract the placeholder from the base prompt (e.g., {entity})
        placeholder = re.findall(r'\{(.*?)\}', base_prompt)

        if placeholder:  # Ensure we have at least one placeholder
            placeholder = placeholder[0]  # Get the first placeholder (assuming only one placeholder)

            # Ensure that the number of queries matches the number of search results
            if len(st.session_state['queries']) == len(st.session_state['search_results']):
                # Iterate over entities, formatted queries, and their search results
                for entity, search_data in st.session_state['search_results'].items():
                    # Get the corresponding query for the entity
                    query = st.session_state['queries'][list(st.session_state['search_results'].keys()).index(entity)]

                    # Replace the placeholder with the actual entity in the query
                    prompt = base_prompt.replace(f"{{{placeholder}}}" , entity)

                    # Construct the LLM input
                    full_input = f"{prompt}\n\nSearch Results:\n{search_data}"

                    # Extract the information from the LLM using the agent
                    response = agent.extract_info_with_prompt(search_data, prompt)  # Use the agent

                    llm_results[entity] = response

                # Store LLM results in session state
                st.session_state['llm_results'] = llm_results
                st.write("LLM Results:", llm_results)
            else:
                st.warning(
                    "The number of queries does not match the number of search results. Please check your inputs.")
        else:
            st.warning(
                "No placeholders found in the prompt. Please ensure the prompt contains a placeholder like {entity}.")

