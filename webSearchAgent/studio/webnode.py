
from dotenv import load_dotenv
load_dotenv()

from typing import Annotated

from langchain.chat_models import init_chat_model
from typing_extensions import TypedDict
from langchain_core.messages import SystemMessage, HumanMessage, RemoveMessage
from langchain_tavily import TavilySearch

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver  # Add this import

from langgraph.graph import MessagesState

class State(TypedDict):
    question: str
    search_results: str  # Add this field to store search results
    summarized_result: str


def web_search(state: State):

    # Initialize Tavily search
    search = TavilySearch(max_results=3)  # Limit to 3 results for brevity

    try:
        # Perform the search
        response = search.invoke(state["question"])

        print(response)

        # Format the results
        formatted_results = []
        for result in response["results"]:
            formatted_results.append(f"Title: {result.get('title', 'N/A')}\nURL: {result.get('url', 'N/A')}\nContent: {result.get('content', 'N/A')}\n")

        search_summary = "\n".join(formatted_results)

        return {"search_results": search_summary}

    except Exception as e:
        return {"search_results": f"Search failed: {str(e)}"}
