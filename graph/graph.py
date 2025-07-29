from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langgraph.graph import StateGraph, START, END, add_messages
from models.schema import State
from routes.routes import *
from services.chat.chatbot import chatbot
from services.classifiers import *

def graph():
    # Build the graph
    workflow = StateGraph(State)

    # Basic nodes
    workflow.add_node("start_node", start_node)
    workflow.add_node("chatbot", chatbot)

    # Logic nodes

    # Set entry point
    workflow.set_entry_point("start_node")
    
    # Add terminal edges
    workflow.add_edge("chatbot", END)

    # Compile the graph with increased recursion limit
    app = workflow.compile()
    return app