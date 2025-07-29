from models.schema import State
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from services.llm_connector.llm_connector import llm
from graph.graph import graph

# Initialize the graph
app = graph()

def run_chatbot():
    """Run the chatbot application"""
    state: State = {
        "messages": [],
        "memory": []
    }

    while True:
        user_input = input("\n\nMessage: ")
        if user_input.lower() in ["exit", "quit", "bye", "/bye"]:
            print("Bye Bye!")
            break

        # Add user message to state
        state["messages"].append(HumanMessage(content=user_input))
        
        # Execute graph
        output = app.invoke(state)
        state.update(output)