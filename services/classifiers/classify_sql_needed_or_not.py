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

    classifier_llm = llm.with_structured_output(bool)
    try:
        result = classifier_llm.invoke(
            [
                SystemMessage(
                    content="Classify whether SQL is needed or not based on the user's last message."
                ),
                HumanMessage(content=last_user_message.content),
            ]
        )
        return {"sql_needed_or_not": result}
    
    except Exception as e:
        print(f"Error in classification: {e}")
        return {"sql_needed_or_not": False}