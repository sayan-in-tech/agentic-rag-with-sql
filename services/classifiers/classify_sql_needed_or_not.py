from langchain_core.messages import HumanMessage, SystemMessage
from models.schema import State
from services.llm_connector.llm_connector import llm
from pydantic import BaseModel

class SQLClassificationResult(BaseModel):
    sql_needed: bool

def classify_sql_needed_or_not(state: State) -> dict:
    """Classify if SQL is needed or not based on the user's last message"""
    
    last_user_message = next(
        (msg for msg in reversed(state["messages"]) if isinstance(msg, HumanMessage)),
        None,
    )
    
    if not last_user_message:
        return {"sql_needed_or_not": False}

    try:
        # Use structured output with proper boolean handling
        classifier_llm = llm.with_structured_output(SQLClassificationResult)
        result = classifier_llm.invoke(
            [
                SystemMessage(
                    content="Classify whether SQL is needed or not based on the user's last message. Return true if the user is asking for data, database information, or wants to query the database. Return false for general conversation."
                ),
                HumanMessage(content=last_user_message.content),
            ]
        )
        return {"sql_needed_or_not": result.sql_needed}
    
    except Exception as e:
        print(f"❌ [services/classifiers/classify_sql_needed_or_not.py:classify_sql_needed_or_not] Error in classification: {e}")
        # Fallback: check for common SQL-related keywords
        user_text = last_user_message.content.lower()
        sql_keywords = ['show', 'select', 'find', 'get', 'list', 'count', 'customer', 'invoice', 'employee', 'track', 'album', 'artist']
        has_sql_keywords = any(keyword in user_text for keyword in sql_keywords)
        return {"sql_needed_or_not": has_sql_keywords}