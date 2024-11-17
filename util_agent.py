from langchain.agents import initialize_agent, Tool
from langchain.llms import OpenAI
from langchain.utilities import SerpAPIWrapper
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

class LangChainAgent:
    """LangChain Agent for web search and targeted data extraction."""

    def __init__(self, groq_key: str, serpapi_key: str):
        # Set up API keys
        # os.environ["OPENAI_API_KEY"] = openai_key

        os.environ["SERPAPI_API_KEY"] = serpapi_key
        os.environ['GROQ_API_KEY'] =groq_key

        # Initialize SerpAPIWrapper
        self.serpapi = SerpAPIWrapper(serpapi_api_key=serpapi_key)

        # Initialize LangChain LLM
        # self.llm = OpenAI(model="gpt-4o-mini", temperature=0)
        self.llm = ChatGroq(model_name="mixtral-8x7b-32768",temperature = 0)
        # Define tools for the agent
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
            # Combine the prompt and search results
            full_prompt = f"{prompt}\n\n Web Search Results:\n{search_results}"
            messages = [
                (
                    "system",
                    "You are a helpful assistant who answers query based on Web search Results",
                ),
                ("human", full_prompt),
            ]
            print(full_prompt)
            return self.llm.invoke(messages)
        except Exception as e:
            return f"Error during information extraction: {e}"
