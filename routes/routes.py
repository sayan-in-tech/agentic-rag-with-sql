
from models.schema import State, IntentLoginOrRegisterClassifier
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from services.llm_connector.llm_connector import llm
import os

def route_sql_needed_or_not(state: State) -> str:
    if state["sql_needed_or_not"] == True:
        return "generate_sql_query"
    else:
        return "chatbot"