from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph import add_messages

class State(TypedDict):
    messages: Annotated[list, add_messages]
    memory: list
    sql_needed_or_not: bool = False
    sql_query: str = ""
    sql_output: str = ""