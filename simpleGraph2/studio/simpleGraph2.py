
from dotenv import load_dotenv
load_dotenv()

from typing import Annotated

from langchain.chat_models import init_chat_model
from typing_extensions import TypedDict
from langchain_core.messages import SystemMessage, HumanMessage, RemoveMessage

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver  # Add this import

from langgraph.graph import MessagesState
class State(MessagesState):
    summary: str


def chatbot(state: State):
    llm = init_chat_model("anthropic:claude-3-5-sonnet-latest")
    return {"messages": [llm.invoke(state["messages"])]}

def summarizer(state: State):
    llm = init_chat_model("anthropic:claude-3-5-sonnet-latest")
    summary_message = "Create a summary of the conversation above:"
    # Add prompt to our history
    messages = state["messages"] + [HumanMessage(content=summary_message)]
    response = llm.invoke(messages)
    return {"summary": response.content}


graph_builder = StateGraph(State)
# The first argument is the unique node name
# The second argument is the function or object that will be called whenever
# the node is used.
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("summarizer", summarizer)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", "summarizer")
graph_builder.add_edge("summarizer", END)


# Add checkpointer for persistence
checkpointer = MemorySaver()
#graph = graph_builder.compile(checkpointer=checkpointer)  # Add checkpointer her
graph = graph_builder.compile()  # Add checkpointer her
