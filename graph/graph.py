from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langgraph.graph import StateGraph, START, END, add_messages
from models.schema import State
from routes.routes import *
from services.chat.chatbot import chatbot
from services.classifiers import *
from services.sql.generate_sql_query import generate_sql_query
from services.sql.execute_sql_query import execute_sql_query
from services.classifiers.classify_sql_needed_or_not import classify_sql_needed_or_not

def graph():
    # Build the graph
    workflow = StateGraph(State)

    # Basic nodes
    workflow.add_node("start_node", start_node)
    workflow.add_node("chatbot", chatbot)
    workflow.add_node("classify_sql_needed_or_not", classify_sql_needed_or_not)
    workflow.add_node("generate_sql_query", generate_sql_query)
    workflow.add_node("execute_sql_query", execute_sql_query)

    # Set entry point
    workflow.set_entry_point("start_node")
    
    # Flow: start_node -> chatbot -> classify_sql_needed_or_not
    workflow.add_edge("start_node", "chatbot")
    workflow.add_edge("chatbot", "classify_sql_needed_or_not")
    
    # Conditional routing from classify_sql_needed_or_not
    workflow.add_conditional_edges(
        "classify_sql_needed_or_not",
        route_sql_needed_or_not,
        {
            "generate_sql_query": "generate_sql_query",
            "chatbot": "chatbot"
        }
    )
    
    # SQL flow: generate -> execute -> back to chatbot
    workflow.add_edge("generate_sql_query", "execute_sql_query")
    workflow.add_edge("execute_sql_query", "chatbot")

    # Add terminal edges
    workflow.add_edge("chatbot", END)

    # Compile the graph
    app = workflow.compile()
    return app