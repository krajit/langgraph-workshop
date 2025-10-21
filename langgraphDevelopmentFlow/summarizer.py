

from dotenv import load_dotenv
load_dotenv()

from langchain.chat_models import init_chat_model
from states import State

def summarizer_node(state: State):
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
