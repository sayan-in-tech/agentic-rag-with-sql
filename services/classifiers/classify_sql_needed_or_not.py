from langchain_core.messages import HumanMessage, SystemMessage
from models.schema import State
from services.llm_connector.llm_connector import llm

def classify_sql_needed_or_not(state: State) -> dict:
    """Classify if SQL is needed or not based on the user's last message"""
    
    last_user_message = next(
        (msg for msg in reversed(state["messages"]) if isinstance(msg, HumanMessage)),
        None,
    )
    
    if not last_user_message:
        return {"sql_needed_or_not": False}

    try:
        # Use a simple classification approach
        messages = [
            SystemMessage(
                content="You are a classifier. Analyze the user's message and respond with ONLY 'true' if the user is asking for data, database information, or wants to query the database. Respond with ONLY 'false' for general conversation. Do not include any other text in your response."
            ),
            HumanMessage(content=last_user_message.content),
        ]
        
        response = llm.invoke(messages)
        result_text = response.content.strip().lower()
        
        # Parse the response
        if result_text == "true":
            return {"sql_needed_or_not": True}
        elif result_text == "false":
            return {"sql_needed_or_not": False}
        else:
            # Fallback to keyword-based classification
            return _fallback_classification(last_user_message.content)
    
    except Exception as e:
        print(f"❌ [services/classifiers/classify_sql_needed_or_not.py:classify_sql_needed_or_not] Error in classification: {e}")
        return _fallback_classification(last_user_message.content)

def _fallback_classification(user_text: str) -> dict:
    """Fallback classification based on keywords"""
    user_text_lower = user_text.lower()
    sql_keywords = ['show', 'select', 'find', 'get', 'list', 'count', 'customer', 'invoice', 'employee', 'track', 'album', 'artist', 'data', 'database', 'query']
    has_sql_keywords = any(keyword in user_text_lower for keyword in sql_keywords)
    return {"sql_needed_or_not": has_sql_keywords}