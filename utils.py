import requests
import os
import streamlit as st
import openai


openai.api_key = st.secrets["OpenAI_key"]
def search_serpapi(query, api_key):

    url = "https://serpapi.com/search"
    params = {
        "q": query,
        "api_key": api_key,
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Search API failed with status {response.status_code}")
        return None


def automated_web_search(selected_column_data):
    serp_api_key = st.secrets["SerpAPI_key"]
    user_query_template = st.session_state['user_query_template']

    results = []
    for entity in selected_column_data:
        # Replace placeholder with actual entity name
        query = user_query_template.replace("{entity}", entity)
        st.write(f"Searching for: {query}")

        search_result = search_serpapi(query, serp_api_key)

        if search_result:
            top_result = search_result.get("organic_results", [{}])[:2]
            extracted_data = {
                "Entity": entity,
                "Title": top_result.get("title", "N/A"),
                "Link": top_result.get("link", "N/A"),
                "Snippet": top_result.get("snippet", "N/A")
            }
            results.append(extracted_data)

    return results


def send_to_openai(results, entity_name ):


    try:
        # Create a prompt to summarize the search results
        base_prompt = st.session_state['user_prompt']
        prompt = f"Summarize the following search results: {results}"

        # Send the prompt to OpenAI's API (using text-davinci-003 or GPT-4)
        response = openai.Completion.create(
            model="gpt-4o",  # You can replace this with GPT-4 if you have access
            prompt=prompt,
            max_tokens=150  # Adjust token limit as needed
        )

        # If successful, return OpenAI's response
        return response.choices[0].text.strip()

    except openai.error.OpenAIError as e:
        st.error(f"Error sending data to OpenAI: {e}")
        return None