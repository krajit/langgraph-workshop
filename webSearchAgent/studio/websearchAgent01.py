
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

from studio.webnode import web_search

class State(TypedDict):
    question: str
    search_results: str  # Add this field to store search results
    summarized_result: str


def summarizer(state: State):
    llm = init_chat_model("anthropic:claude-3-5-sonnet-latest")

    prompt_template = """
    You are  a helpful assistant. You are will be given a question the context to answer the question. Give a short concise answer to the question based on the context. 
    If you don't know the answer, just say so.

    Question: {question}
    Context: {context}
    Ans: 
    """
    response = llm.invoke(prompt_template.format(question=state["question"], context=state["search_results"]))
    return {"summarized_result": response.content}


graph_builder = StateGraph(State)
# The first argument is the unique node name
# The second argument is the function or object that will be called whenever
# the node is used.
graph_builder.add_node("web_search", web_search)
graph_builder.add_node("summarizer", summarizer)

# Simple flow: web search -> chatbot with search results -> summarizer
graph_builder.add_edge(START, "web_search")
graph_builder.add_edge("web_search", "summarizer")
graph_builder.add_edge("summarizer", END)

# Add checkpointer for persistence
checkpointer = MemorySaver()
#graph = graph_builder.compile(checkpointer=checkpointer)  # Add checkpointer her
graph = graph_builder.compile()  # Add checkpointer her
