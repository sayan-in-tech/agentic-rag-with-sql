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
    
    # Validate input
    if not latest_user_message or not latest_user_message.strip():
        error_msg = "No valid user message found for SQL generation."
        return {
            "sql_query": "",
            "messages": state["messages"] + [SystemMessage(content=error_msg)]
        }
    
    # Retrieve relevant database schema context from RAG
    try:
        rag_context = retrieve_context(latest_user_message)
        if not rag_context:
            rag_context = "No relevant database schema found."
    except Exception as e:
        rag_context = f"Error retrieving schema context: {str(e)}"
    
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
        if llm is None:
            raise ValueError("LLM not available")
            
        response = llm.invoke([
            SystemMessage(content=system_prompt.format(
                rag_context=rag_context,
                question=latest_user_message
            ))
        ])
        
        sql_query = response.content.strip()
        
        # Validate generated SQL
        if not sql_query or sql_query.lower() in ['', 'none', 'null', 'no sql generated']:
            raise ValueError("No valid SQL query was generated")
        
        # Add the generated SQL to the state
        return {
            "sql_query": sql_query,
            "messages": state["messages"] + [SystemMessage(content=f"Generated SQL using RAG context: {sql_query}")]
        }
    except Exception as e:
        error_msg = f"Error generating SQL: {str(e)}"
        print(f"❌ [services/sql/generate_sql_query.py:generate_sql_query] {error_msg}")
        return {
            "sql_query": "",
            "messages": state["messages"] + [SystemMessage(content=error_msg)]
        }
