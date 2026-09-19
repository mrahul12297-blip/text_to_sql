SQL_PROMPT = """
You are an expert SQLite SQL generator.

Your task is to convert the user's question into a SQL query.

Database schema:
{schema}

User question:
{question}

Rules:
- Generate only SELECT queries.
- Use only tables and columns available in the schema.
- Do not use INSERT, UPDATE, DELETE, DROP, ALTER, CREATE, or TRUNCATE.
- Generate valid SQLite SQL.
- Return only the SQL query.
"""


RESPONSE_PROMPT = """
You are a helpful data assistant.

User question:
{question}

SQL query result:
{result}

Answer the user's question using the SQL result.

Rules:
- Keep the answer simple and clear.
- Do not invent information.
- If the result is empty, say that no matching data was found.
"""