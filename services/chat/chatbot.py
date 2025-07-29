from langchain_core.messages import AIMessage, SystemMessage
from models.schema import State
from services.llm_connector.llm_connector import llm, retrieve_context

def chatbot(state: State) -> State:
    """Handle chatbot interactions with RAG-enhanced prompting"""
    user_msg = state["messages"][-1]
    user_input = user_msg.content

    # Retrieve relevant context from FAISS
    context = retrieve_context(user_input)

    # Construct prompt for Gemini
    prompt = f"""
    Answer the question based on the context provided below. 
    If the answer is not in the context, say "I don't know".

    Context:
    {context}

    Question:
    {user_input}

    Answer:
    """

    # Stream response from Gemini
    response_text = ""
    print("Assistant (streaming): ", end="", flush=True)
    for chunk in llm.stream([SystemMessage(content=prompt)]):
        print(chunk.content, end="", flush=True)
        response_text += chunk.content
    print()

    ai_msg = AIMessage(content=response_text)
    state["messages"].append(ai_msg)
    state["memory"] = state["memory"] + [user_msg, ai_msg]
    return state
