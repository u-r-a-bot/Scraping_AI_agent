import streamlit as st

### Sidebar not to be used for that
def sidebar():
    default_prompt = "Get me the Email address of the {Company}"
    if "prompt" not in st.session_state:
        st.session_state["prompt"] = default_prompt
    def reset_prompt():
        st.session_state["prompt"] = default_prompt
    with st.sidebar:
        st.write("Enter Prompt Template")
        prompt = st.text_input('Prompt Input', key="prompt")
        st.button("Reset Prompt", on_click=reset_prompt, type="primary")
        global prompt


