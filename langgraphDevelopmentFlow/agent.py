

from dotenv import load_dotenv
load_dotenv()

# A simple test graph
from langgraph.graph import StateGraph, START, END


from states import State
from webnode import web_search_node
from summarizer import summarizer_node

graph_builder = StateGraph(State)

graph_builder.add_node("web_search", web_search_node)
graph_builder.add_node("summarize", summarizer_node)

graph_builder.add_edge(START, "web_search")
graph_builder.add_edge("web_search","summarize")
graph_builder.add_edge("summarize", END)
graph = graph_builder.compile() 
