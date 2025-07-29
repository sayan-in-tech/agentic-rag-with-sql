from langchain_core.messages import AIMessage, SystemMessage, HumanMessage
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
    
    # Construct messages for Gemini
    messages = []
    
    # Add system message if we have SQL output
    if sql_output:
        system_content = f"""You are a helpful assistant. Answer the user's question based on the SQL results provided below.
If the answer is not in the SQL results, provide a helpful response based on your knowledge.

SQL Results:
{sql_output}"""
        messages.append(SystemMessage(content=system_content))
    
    # Add the user message
    messages.append(HumanMessage(content=user_input))

    # Stream response from Gemini
    response_text = ""
    print("Assistant (streaming): ", end="", flush=True)
    try:
        # Debug: Print the messages being sent
        print(f"\nDEBUG: Number of messages: {len(messages)}")
        for i, msg in enumerate(messages):
            print(f"DEBUG: Message {i+1} type: {type(msg).__name__}, content length: {len(msg.content)}")
        
        # Use invoke with the properly formatted messages
        response = llm.invoke(messages)
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
