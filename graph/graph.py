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

    # Classify SQL needed or not
    workflow.add_node("classify_sql_needed_or_not", classify_sql_needed_or_not)

    # Generate SQL query
    workflow.add_node("generate_sql_query", generate_sql_query)

    # Execute SQL query
    workflow.add_node("execute_sql_query", execute_sql_query)

    # Conditional routings
    workflow.add_conditional_edges(
        "start_node",
        route_sql_needed_or_not,
        {
            "sql_needed_or_not": "classify_sql_needed_or_not",
            "no_sql_needed": "chatbot"
        }
    )
    workflow.add_edge("classify_sql_needed_or_not", "generate_sql_query")
    workflow.add_edge("generate_sql_query", "execute_sql_query")
    workflow.add_edge("execute_sql_query", "chatbot")

    # Set entry point
    workflow.set_entry_point("start_node")
    
    # Add terminal edges
    workflow.add_edge("chatbot", END)

    # Compile the graph with increased recursion limit
    app = workflow.compile()
    return app