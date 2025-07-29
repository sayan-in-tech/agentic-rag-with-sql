from langchain_core.prompts import ChatPromptTemplate
from models.schema import State  # Your existing State definition

# Chinook-based schema snippet (you can extend this or load dynamically)
SCHEMA = """
Table: Customer
Columns:
  - CustomerId (INTEGER) [PK] [NOT NULL]
  - FirstName (NVARCHAR(40)) [NOT NULL]
  - LastName (NVARCHAR(20)) [NOT NULL]
  - Email (NVARCHAR(60)) [NOT NULL]
  - SupportRepId (INTEGER)
Foreign Keys:
  - SupportRepId → Employee.EmployeeId

Table: Invoice
Columns:
  - InvoiceId (INTEGER) [PK] [NOT NULL]
  - CustomerId (INTEGER) [NOT NULL]
  - InvoiceDate (DATETIME) [NOT NULL]
  - Total (NUMERIC(10,2)) [NOT NULL]
Foreign Keys:
  - CustomerId → Customer.CustomerId
"""

def generate_sql_query(state: State) -> dict:
    """
    Generates an SQL query using the provided schema and the latest user message.
    """

    system_prompt = """
You are a world-class SQL expert.
Using ONLY the following schema, write a correct, optimized SQL query that answers the user’s question.

Schema:
{schema}
"""

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{question}")
    ])

    latest_user_message = state["messages"][-1].content

    return {
        "messages": prompt.format_messages(
            schema=SCHEMA,
            question=latest_user_message
        )
    }
