

from dotenv import load_dotenv
load_dotenv()

from langchain_tavily import TavilySearch

from states import State

def web_search_fun(query: str) -> str:
    search = TavilySearch(max_results = 5)
    try:
        response = search.invoke(query)
        formatted_results = []
        for result in response["results"]:
            formatted_results.append(f"Title:{result.get('title','N/A')}\nURL:{result.get('url','N/A')}\nContent: {result.get('content', 'N/A')}\n")

        search_summary = "\n".join(formatted_results)
        #return search_summary
    except Exception as e:
        search_summary = f"Search failed: {str(e)}"
    return search_summary


def web_search_node(state: State):
    return {"search_results": web_search_fun(state["question"]) }
