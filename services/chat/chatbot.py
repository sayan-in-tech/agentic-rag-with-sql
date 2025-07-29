from langchain_core.messages import AIMessage, SystemMessage
from models.schema import State
from services.llm_connector.llm_connector import llm

def chatbot(state: State) -> State:
    """Handle chatbot interactions"""
    # Get the last user message
    user_msg = state["messages"][-1]
    
    # Prepare the conversation memory
    memory = state["memory"] + [user_msg]
    
    # Get response from LLM
    response_text = ""
    print("Assistant (streaming): ", end="", flush=True)
    for chunk in llm.stream(memory):
        print(chunk.content, end="", flush=True)
        response_text += chunk.content
    print()
    
    # Create AI message
    ai_msg = AIMessage(content=response_text)
    
    # Update state
    state["messages"].append(ai_msg)
    state["memory"] = memory + [ai_msg]
    
    return state 