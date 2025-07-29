from langchain_core.messages import AIMessage, SystemMessage
from models.schema import State
from services.llm_connector.llm_connector import llm

def chatbot(state: State) -> State:
    """Handle chatbot interactions with enhanced prompting"""
    user_msg = state["messages"][-1]
    user_input = user_msg.content

    # Check if LLM is available
    if llm is None:
        error_msg = "LLM not available. Please check your Google API key configuration."
        print(f"Error: {error_msg}")
        ai_msg = AIMessage(content=error_msg)
        state["messages"].append(ai_msg)
        state["memory"] = state["memory"] + [user_msg, ai_msg]
        return state

    # Check if we have SQL output from previous execution
    sql_output = state.get("sql_output", "")
    
    # Construct prompt for Gemini
    if sql_output:
        # If we have SQL results, include them in the context
        prompt = f"""
        You are a helpful assistant. Answer the user's question based on the SQL results provided below.
        If the answer is not in the SQL results, provide a helpful response based on your knowledge.

        SQL Results:
        {sql_output}

        Question:
        {user_input}

        Answer:
        """
    else:
        # Standard assistant prompt
        prompt = f"""
        You are a helpful assistant. Answer the user's question in a clear and helpful manner.
        If you don't know the answer, say so.

        Question:
        {user_input}

        Answer:
        """

    # Stream response from Gemini
    response_text = ""
    print("Assistant (streaming): ", end="", flush=True)
    try:
        for chunk in llm.stream([SystemMessage(content=prompt)]):
            print(chunk.content, end="", flush=True)
            response_text += chunk.content
        print()
    except Exception as e:
        error_msg = f"Error generating response: {str(e)}"
        print(f"\nError: {error_msg}")
        response_text = error_msg

    ai_msg = AIMessage(content=response_text)
    state["messages"].append(ai_msg)
    state["memory"] = state["memory"] + [user_msg, ai_msg]
    return state
