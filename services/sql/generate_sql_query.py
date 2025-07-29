from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage
from models.schema import State
from services.llm_connector.llm_connector import llm, retrieve_context

def generate_sql_query(state: State) -> dict:
    """
    Generates an SQL query using the database schema from RAG and the latest user message.
    Uses RAG to retrieve relevant database schema information.
    """
    latest_user_message = state["messages"][-1].content
    
    # Retrieve relevant database schema context from RAG
    rag_context = retrieve_context(latest_user_message)
    
    system_prompt = """
You are a world-class SQL expert.
Using the database schema information provided below, write a correct, optimized SQL query that answers the user's question.
Return ONLY the SQL query, no explanations or markdown formatting.

Database Schema Information:
{rag_context}

User Question: {question}

Generate the SQL query:
"""

    # Generate SQL using LLM with RAG context
    try:
        response = llm.invoke([
            SystemMessage(content=system_prompt.format(
                rag_context=rag_context,
                question=latest_user_message
            ))
        ])
        
        sql_query = response.content.strip()
        
        # Add the generated SQL to the state
        return {
            "sql_query": sql_query,
            "messages": state["messages"] + [SystemMessage(content=f"Generated SQL using RAG context: {sql_query}")]
        }
    except Exception as e:
        error_msg = f"Error generating SQL: {str(e)}"
        return {
            "sql_query": "",
            "messages": state["messages"] + [SystemMessage(content=error_msg)]
        }
