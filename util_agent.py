from langchain.agents import initialize_agent, Tool
from langchain.llms import OpenAI
from langchain.utilities import SerpAPIWrapper
import os
from langchain_groq import ChatGroq

class LangChainAgent:
    """LangChain Agent for web search and targeted data extraction."""

    def __init__(self, groq_key: str, serpapi_key: str):


        os.environ["SERPAPI_API_KEY"] = serpapi_key
        os.environ['GROQ_API_KEY'] =groq_key


        self.serpapi = SerpAPIWrapper(serpapi_api_key=serpapi_key)

        # Initialize LangChain LLM
        # self.llm = OpenAI(model="gpt-4o-mini", temperature=0)
        self.llm = ChatGroq(model_name="mixtral-8x7b-32768",temperature = 0)

        self.tools = [
            Tool(
                name="Web Search",
                func=self.fetch_search_results,
                description="Search the web for information using SerpAPI."
            )
        ]

        # Initialize the agent
        self.agent = initialize_agent(self.tools, self.llm, agent="zero-shot-react-description", verbose=True)

    def fetch_search_results(self, query: str) -> str:
        """Perform a search using SerpAPI and return results as text."""
        results: str = self.serpapi.run(query)
        return results
        # Extract key information (e.g., titles, snippets, links)
        # return "\n".join(
        #     [
        #         f"Title: {item.get('title', 'N/A')}\nSnippet: {item.get('snippet', 'N/A')}\nLink: {item.get('link', 'N/A')}\n"
        #         for item in results.get("organic_results", [])
        #     ]
        # )

    def extract_info_with_prompt(self, search_results: str, prompt: str) -> str:
        """Extract specific information from search results using the provided prompt."""
        try:
            full_prompt = f"{prompt}\n\n Web Search Results:\n{search_results} "
            messages = [
                (
                    "system",
                    """ You are a helpful assistant that extracts specific information from web search results.
                        You must Respond in JSON format with the structure
                        {
                            "Query asked" : "Extracted info from web search results"
                        }
                        - If any value is missing use None
                        - You strictly answer from the given Web search results 
                        - If there are multiple values you use a list in the value part of the json and not violate the structure
                        - You only respond in JSON format
                        
                    """,
                ),
                ("human", full_prompt),
            ]
            return self.llm.invoke(messages).content
        except Exception as e:
            return f"Error during information extraction: {e}"
