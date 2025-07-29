import sqlite3
import re
from typing import List, Dict, Any
from models.schema import State
from langchain_core.messages import SystemMessage

def convert_sql_response_to_text(sql_results: str) -> str:
    """
    Convert SQL query results to natural language text.
    This represents the "Convert response to text" step in the flowchart.
    """
    if not sql_results:
        return "No results to convert."
    
    # Simple conversion - in a real implementation, you might use an LLM here
    # to convert the results to more natural language
    if "Query Results:" in sql_results:
        return f"Here are the results from your query:\n{sql_results}"
    elif "Query executed successfully" in sql_results:
        return f"Your query was executed successfully. {sql_results}"
    else:
        return f"Query result: {sql_results}"

def extract_sql_query(state: State) -> str:
    """
    Extract SQL query from the state messages.
    Looks for SQL queries in the latest AI message or user message.
    """
    if not state["messages"]:
        return ""
    
    latest_message = state["messages"][-1]
    content = latest_message.content
    
    sql_patterns = [
        r'```sql\s*(.*?)\s*```',  # SQL in code blocks
        r'```\s*(SELECT|INSERT|UPDATE|DELETE|CREATE|DROP|WITH).*?```',  # SQL without sql tag
        r'(SELECT|INSERT|UPDATE|DELETE|CREATE|DROP|WITH)\s+.*?(?:;|$)',  # SQL statements
    ]
    
    for pattern in sql_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE | re.DOTALL)
        if matches:
            return matches[0].strip()
    
    return ""

def execute_sql_query(state: State) -> dict:
    """
    Execute a SQL query based on the state and return the results in text format.
    """
    # First, try to get SQL from the state
    sql_query = state.get("sql_query", "")
    
    # If not in state, try to extract from messages
    if not sql_query:
        sql_query = extract_sql_query(state)
    
    if not sql_query:
        return {
            "status": "error", 
            "results": "No SQL query found in the conversation. Please provide a valid SQL query.",
            "sql_output": "No SQL query available to execute."
        }
    
    try:
        # Connect to the SQLite database
        db_path = "persistence/db/Chinook_Sqlite.db"
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Execute the query
        cursor.execute(sql_query)
        
        # Get column names
        columns = [description[0] for description in cursor.description] if cursor.description else []
        
        # Fetch results
        rows = cursor.fetchall()
        
        # Print execution results
        print(f"✅ Query executed successfully!")
        print(f"📊 Results: {len(rows)} rows returned")
        if columns:
            print(f"📋 Columns: {', '.join(columns)}")
        
        # Format results as text
        if not rows:
            result_text = "Query executed successfully. No results returned."
        else:
            # Create a formatted table
            if columns:
                # Calculate column widths
                col_widths = [len(col) for col in columns]
                for row in rows:
                    for i, cell in enumerate(row):
                        col_widths[i] = max(col_widths[i], len(str(cell)))
                
                # Create header
                header = " | ".join(f"{col:<{col_widths[i]}}" for i, col in enumerate(columns))
                separator = "-" * len(header)
                
                # Create rows
                formatted_rows = []
                for row in rows:
                    formatted_row = " | ".join(f"{str(cell):<{col_widths[i]}}" for i, cell in enumerate(row))
                    formatted_rows.append(formatted_row)
                
                result_text = f"Query Results:\n{separator}\n{header}\n{separator}\n"
                result_text += "\n".join(formatted_rows)
                result_text += f"\n{separator}\nTotal rows: {len(rows)}"
            else:
                # For queries that don't return data (INSERT, UPDATE, DELETE, etc.)
                result_text = f"Query executed successfully. {len(rows)} rows affected."
        
        # Close connection
        conn.close()
        
        # Convert results to natural language text
        natural_language_result = convert_sql_response_to_text(result_text)
        
        return {
            "status": "success",
            "results": result_text,
            "sql_query": sql_query,
            "sql_output": natural_language_result,
            "row_count": len(rows),
            "messages": state["messages"] + [SystemMessage(content=natural_language_result)]
        }
        
    except sqlite3.Error as e:
        error_msg = f"Database error: {str(e)}"
        print(f"❌ [services/sql/execute_sql_query.py:execute_sql_query] {error_msg}")
        return {
            "status": "error",
            "results": error_msg,
            "sql_query": sql_query,
            "sql_output": error_msg,
            "messages": state["messages"] + [SystemMessage(content=error_msg)]
        }
    except Exception as e:
        error_msg = f"Error executing SQL query: {str(e)}"
        print(f"❌ [services/sql/execute_sql_query.py:execute_sql_query] {error_msg}")
        return {
            "status": "error", 
            "results": error_msg,
            "sql_query": sql_query,
            "sql_output": error_msg,
            "messages": state["messages"] + [SystemMessage(content=error_msg)]
        }  