
from typing_extensions import TypedDict
class State(TypedDict):
    question: str
    search_results: str  # Add this field to store search results
    summarized_result: str
