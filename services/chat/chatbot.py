from langchain_core.messages import AIMessage, SystemMessage
from models.schema import State
from services.llm_connector.llm_connector import llm

def chatbot(state: State) -> State:
    """Handle chatbot interactions with enhanced prompting"""
    if not state["messages"]:
        error_msg = "No messages in state to process."
        print(f"❌ [services/chat/chatbot.py:chatbot] {error_msg}")
        ai_msg = AIMessage(content=error_msg)
        state["messages"].append(ai_msg)
        return state
    
    user_msg = state["messages"][-1]
    user_input = user_msg.content

    # Check if LLM is available
    if llm is None:
        error_msg = "LLM not available. Please check your Google API key configuration."
        print(f"❌ [services/chat/chatbot.py:chatbot] {error_msg}")
        ai_msg = AIMessage(content=error_msg)
        state["messages"].append(ai_msg)
        state["memory"] = state["memory"] + [user_msg, ai_msg]
        return state

    # Validate user input
    if not user_input or not user_input.strip():
        error_msg = "Please provide a valid message."
        print(f"❌ [services/chat/chatbot.py:chatbot] {error_msg}")
        ai_msg = AIMessage(content=error_msg)
        state["messages"].append(ai_msg)
        state["memory"] = state["memory"] + [user_msg, ai_msg]
        return state

    # Check if we have SQL output from previous execution
    sql_output = state.get("sql_output", "")
    
    # Construct prompt for Gemini
    if sql_output:
        # If we have SQL results, include them in the context
        prompt = f"""You are a helpful assistant. Answer the user's question based on the SQL results provided below.
If the answer is not in the SQL results, provide a helpful response based on your knowledge.

SQL Results:
{sql_output}

Question:
{user_input}

Answer:"""
    else:
        # Standard assistant prompt
        prompt = f"""You are a helpful assistant. Answer the user's question in a clear and helpful manner.
If you don't know the answer, say so.

Question:
{user_input}

Answer:"""

    # Validate prompt before sending to LLM
    if not prompt or not prompt.strip():
        error_msg = "Failed to construct valid prompt."
        print(f"❌ [services/chat/chatbot.py:chatbot] {error_msg}")
        ai_msg = AIMessage(content=error_msg)
        state["messages"].append(ai_msg)
        state["memory"] = state["memory"] + [user_msg, ai_msg]
        return state

    # Stream response from Gemini
    response_text = ""
    print("Assistant (streaming): ", end="", flush=True)
    try:
        # Create the system message
        system_message = SystemMessage(content=prompt)
        
        # Debug: Print the exact content being sent
        print(f"\nDEBUG: System message content length: {len(system_message.content)}")
        print(f"DEBUG: System message content: '{system_message.content[:100]}...'")
        
        if not system_message.content or not system_message.content.strip():
            raise ValueError("System message content is empty")
            
        # Try using invoke instead of stream first to test
        response = llm.invoke([system_message])
        response_text = response.content
        
        print(response_text)
        
    except Exception as e:
        error_msg = f"Error generating response: {str(e)}"
        print(f"\n❌ [services/chat/chatbot.py:chatbot] {error_msg}")
        response_text = "I'm sorry, I encountered an error while processing your request. Please try again."

    ai_msg = AIMessage(content=response_text)
    state["messages"].append(ai_msg)
    state["memory"] = state["memory"] + [user_msg, ai_msg]
    return state
