# lets practice using Tavily

from langchain_tavily import TavilySearch

tool = TavilySearch(max_results = 5)
response = tool.invoke("Whats a node in Langgraph?")
