
from models.schema import State
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from services.llm_connector.llm_connector import llm
import os

def start_node(state: State) -> State:
    """Initialize the workflow and route to the first step"""
    # Initialize SQL-related state variables if not present
    if "sql_needed_or_not" not in state:
        state["sql_needed_or_not"] = False
    if "sql_query" not in state:
        state["sql_query"] = ""
    if "sql_output" not in state:
        state["sql_output"] = ""
    
    return state

def route_sql_needed_or_not(state: State) -> str:
    if state["sql_needed_or_not"] == True:
        return "generate_sql_query"
    else:
        return "chatbot"