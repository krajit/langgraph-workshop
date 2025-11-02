
# pick a model
from langchain.chat_models import init_chat_model
llm = init_chat_model("gpt-4o", model_provider="openai")

from langchain_core.tools import tool

@tool
def multiply(a: int, b: int) -> int:
    """Multiply a and b.

    Args:
        a: first int
        b: second int
    """
    return a * b

# This will be a tool
@tool
def add(a: int, b: int) -> int:
    """Adds a and b.

    Args:
        a: first int
        b: second int
    """
    return a + b

@tool
def divide(a: int, b: int) -> float:
    """Divide a and b.

    Args:
        a: first int
        b: second int
    """
    return a / b


from langchain_tavily import TavilySearch

@tool   
def web_search(query: str) -> str:
    """Search the web for the query."""
    tavily = TavilySearch(max_results = 3)
    response = tavily.invoke(query)
    response_combined = ""
    for result in response["results"]:
        response_combined += result["title"] + "\n" + result["url"] + "\n" + result["content"] + "\n\n"
    return response_combined

tools = [add, multiply, divide, web_search]

from langgraph.graph import MessagesState
from langchain_core.messages import HumanMessage, SystemMessage

from prompts import research_agent_prompt as sys_msg_template
from utility import get_today_str

# System message
#sys_msg = SystemMessage(content="You are a helpful assistant. You have acces to web search tool and some arithmetic tool. Feel free to use these tools if you can not answer the question directly.")
sys_msg = SystemMessage(content= sys_msg_template.format(date=get_today_str()))

# Node
def assistant(state: MessagesState):
   llm_with_tools = llm.bind_tools([add, multiply, divide,web_search],parallel_tool_calls=False)
   return {"messages": [llm_with_tools.invoke([sys_msg] + state["messages"])]}

from langgraph.graph import START, StateGraph
from langgraph.prebuilt import tools_condition
from langgraph.prebuilt import ToolNode

# Graph
builder = StateGraph(MessagesState)

# Define nodes: these do the work
builder.add_node("assistant", assistant)
builder.add_node("tools", ToolNode([add, multiply, divide,web_search]))

# Define edges: these determine how the control flow moves
builder.add_edge(START, "assistant")
builder.add_conditional_edges(
    "assistant",
    # If the latest message (result) from assistant is a tool call -> tools_condition routes to tools
    # If the latest message (result) from assistant is a not a tool call -> tools_condition routes to END
    tools_condition,
)
builder.add_edge("tools", "assistant")
react_graph = builder.compile()
