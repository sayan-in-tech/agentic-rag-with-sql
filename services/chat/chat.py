from models.schema import State
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from services.llm_connector.llm_connector import llm
from graph.graph import graph

def run_chatbot():
    """Run the chatbot application"""
    # Initialize the graph inside the function to ensure latest modules are used
    app = graph()
    
    state: State = {
        "messages": [],
        "memory": []
    }

    print("Welcome to the Agentic RAG with SQL Chatbot!")
    print("Type 'exit', 'quit', 'bye', or '/bye' to exit.")
    print("-" * 50)

    while True:
        try:
            user_input = input("\nMessage: ")
            if user_input.lower() in ["exit", "quit", "bye", "/bye"]:
                print("Bye Bye!")
                break

            # Validate user input
            if not user_input or not user_input.strip():
                print("Please provide a valid message.")
                continue

            # Add user message to state
            state["messages"].append(HumanMessage(content=user_input))
            
            # Execute graph
            try:
                output = app.invoke(state)
                state.update(output)
            except Exception as e:
                error_msg = f"Error processing your request: {str(e)}"
                print(f"❌ [services/chat/chat.py:run_chatbot] {error_msg}")
                # Add error message to state
                state["messages"].append(SystemMessage(content=error_msg))
                
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"❌ [services/chat/chat.py:run_chatbot] Unexpected error: {str(e)}")
            continue