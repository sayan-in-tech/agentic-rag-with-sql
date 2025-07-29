import sqlite3
import re
from typing import List, Dict, Any
from models.schema import State

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
    # Extract SQL query from state
    sql_query = extract_sql_query(state)
    
    if not sql_query:
        return {
            "status": "error", 
            "results": "No SQL query found in the conversation. Please provide a valid SQL query."
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
        
        return {
            "status": "success",
            "results": result_text,
            "sql_query": sql_query,
            "row_count": len(rows)
        }
        
    except sqlite3.Error as e:
        return {
            "status": "error",
            "results": f"Database error: {str(e)}",
            "sql_query": sql_query
        }
    except Exception as e:
        return {
            "status": "error", 
            "results": f"Error executing SQL query: {str(e)}",
            "sql_query": sql_query
        }  