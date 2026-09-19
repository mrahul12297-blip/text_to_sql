# from dotenv import load_dotenv
# from langchain_openai import ChatOpenAI
# from langgraph.graph import StateGraph, START, END

# from app.agent.state import AgentState
# from app.agent.prompts import SQL_PROMPT, RESPONSE_PROMPT
# from app.database.sqlite import get_schema, execute_query


# load_dotenv()

# llm = ChatOpenAI(model="gpt-5.6-luna")


# def get_database_schema(state: AgentState):
#     return {"schema": get_schema()}


# def generate_sql(state: AgentState):
#     prompt = SQL_PROMPT.format(
#         schema=state["schema"],
#         question=state["question"]
#     )

#     response = llm.invoke(prompt)

#     return {"sql": response.content.strip(), "error": ""}


# def validate_sql(state: AgentState):
#     sql = state["sql"].strip()
#     sql_lower = sql.lower()

#     if not sql_lower.startswith("select"):
#         return {"error": "Only SELECT queries are allowed."}

#     blocked_words = ["insert", "update", "delete", "drop","alter", "create", "truncate", "replace", "attach", "detach"]

#     for word in blocked_words:
#         if word in sql_lower:
#             return {"error": f"Unsafe SQL query detected: {word}"}

#     return {"error": ""}


# def execute_sql(state: AgentState):
#     try:
#         sql = state["sql"].strip()

#         if "limit" not in sql.lower():
#             sql = sql.rstrip(";") + " LIMIT 100"

#         result = execute_query(sql)

#         return {"sql": sql, "result": result, "error": ""}

#     except Exception as e:
#         return {"result": [], "error": str(e)}


# def fix_sql(state: AgentState):
#     prompt = f"""
# You are an expert SQLite SQL developer.

# User question:
# {state["question"]}

# Generated SQL:
# {state["sql"]}

# Error:
# {state["error"]}

# Database schema:
# {state["schema"]}

# Fix the SQL query.

# Rules:
# - Generate only SELECT queries.
# - Use only tables and columns available in the schema.
# - Generate valid SQLite SQL.
# - Do not use INSERT, UPDATE, DELETE, DROP, ALTER, CREATE,
#   TRUNCATE, REPLACE, ATTACH, or DETACH.
# - Return only the corrected SQL query.
# """

#     response = llm.invoke(prompt)

#     return {
#         "sql": response.content.strip(),
#         "error": "",
#         "retry_count": state["retry_count"] + 1
#     }


# def check_validation(state: AgentState):
#     if state["error"] and state["retry_count"] < 3:
#         return "fix_sql"

#     if state["error"]:
#         return "generate_response"

#     return "execute_sql"


# def check_execution(state: AgentState):
#     if state["error"] and state["retry_count"] < 3:
#         return "fix_sql"

#     return "generate_response"


# def generate_response(state: AgentState):
#     if state["error"]:
#         return {"answer": "Sorry, I could not generate a valid SQL query after 3 attempts."}

#     prompt = RESPONSE_PROMPT.format(
#         question=state["question"],
#         result=state["result"]
#     )

#     response = llm.invoke(prompt)

#     return {"answer": response.content}


# graph_builder = StateGraph(AgentState)

# graph_builder.add_node("get_schema", get_database_schema)
# graph_builder.add_node("generate_sql", generate_sql)
# graph_builder.add_node("validate_sql", validate_sql)
# graph_builder.add_node("execute_sql", execute_sql)
# graph_builder.add_node("fix_sql", fix_sql)
# graph_builder.add_node("generate_response", generate_response)

# graph_builder.add_edge(START, "get_schema")
# graph_builder.add_edge("get_schema", "generate_sql")
# graph_builder.add_edge("generate_sql", "validate_sql")

# graph_builder.add_conditional_edges(
#     "validate_sql",
#     check_validation,
#     {
#         "fix_sql": "fix_sql",
#         "execute_sql": "execute_sql",
#         "generate_response": "generate_response"
#     }
# )

# graph_builder.add_conditional_edges(
#     "execute_sql",
#     check_execution,
#     {
#         "fix_sql": "fix_sql",
#         "generate_response": "generate_response"
#     }
# )

# graph_builder.add_edge("fix_sql", "validate_sql")
# graph_builder.add_edge("generate_response", END)

# graph = graph_builder.compile()



from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END

from app.agent.state import AgentState
from app.agent.prompts import SQL_PROMPT, RESPONSE_PROMPT
from app.database.sqlite import get_schema, execute_query


load_dotenv()

llm = ChatOpenAI(model="gpt-5.6-luna")


def get_database_schema(state: AgentState):
    return {"schema": get_schema()}


def generate_sql(state: AgentState):
    prompt = SQL_PROMPT.format(
        schema=state["schema"],
        question=state["question"]
    )

    response = llm.invoke(prompt)

    return {
        "sql": response.content.strip(),
        "error": ""
    }


def validate_sql(state: AgentState):
    sql = state["sql"].strip()
    sql_lower = sql.lower()

    # -------------------------
    # 1. Security validation
    # -------------------------

    if not sql_lower.startswith("select"):
        return {"error": "Only SELECT queries are allowed."}

    blocked_words = [
        "insert", "update", "delete", "drop", "alter",
        "create", "truncate", "replace", "attach", "detach"
    ]

    for word in blocked_words:
        if word in sql_lower:
            return {"error": f"Unsafe SQL query detected: {word}"}

    # -------------------------
    # 2. Schema validation
    # -------------------------

    schema = state["schema"]

    # Check whether SQL actually references
    # at least one real database table.
    referenced_table = False

    for table_name in schema.keys():
        if table_name.lower() in sql_lower:
            referenced_table = True
            break

    if not referenced_table:
        return {
            "error": (
                "SQL does not reference any valid database table. "
                "The query must retrieve data from the database."
            )
        }

    # -------------------------
    # 3. Basic SQL validation
    # -------------------------

    if ";" in sql.rstrip(";"):
        return {"error": "Multiple SQL statements are not allowed."}

    return {"error": ""}


def execute_sql(state: AgentState):
    try:
        sql = state["sql"].strip()

        # Limit result size
        if "limit" not in sql.lower():
            sql = sql.rstrip(";") + " LIMIT 50"

        result = execute_query(sql)

        return {
            "sql": sql,
            "result": result,
            "error": ""
        }

    except Exception as e:
        return {
            "result": [],
            "error": str(e)
        }


def fix_sql(state: AgentState):
    prompt = f"""
You are an expert SQLite SQL developer.

User question:
{state["question"]}

Generated SQL:
{state["sql"]}

Error:
{state["error"]}

Database schema:
{state["schema"]}

Fix the SQL query.

Rules:
- Generate only SELECT queries.
- The query must retrieve information from the provided database.
- Use only tables and columns available in the schema.
- Generate valid SQLite SQL.
- Do not generate SELECT queries containing only hardcoded values or strings.
- Do not use INSERT, UPDATE, DELETE, DROP, ALTER, CREATE,
  TRUNCATE, REPLACE, ATTACH, or DETACH.
- Do not generate multiple SQL statements.
- Return only the corrected SQL query.
"""

    response = llm.invoke(prompt)

    return {
        "sql": response.content.strip(),
        "error": "",
        "retry_count": state.get("retry_count", 0) + 1
    }

def check_validation(state: AgentState):

    retry_count = state.get("retry_count", 0)

    if state.get("error") and retry_count < 3:
        return "fix_sql"

    if state.get("error"):
        return "generate_response"

    return "execute_sql"
# def check_validation(state: AgentState):
#     if state["error"] and state["retry_count"] < 3:
#         return "fix_sql"

#     if state["error"]:
#         return "generate_response"

#     return "execute_sql"


# def check_execution(state: AgentState):
#     if state["error"] and state["retry_count"] < 3:
#         return "fix_sql"

#     return "generate_response"
def check_execution(state: AgentState):

    retry_count = state.get("retry_count", 0)

    if state.get("error") and retry_count < 3:
        return "fix_sql"

    return "generate_response"


# def generate_response(state: AgentState):
#     # Prevent the LLM from inventing an answer
#     # when SQL returned nothing.
#     if not state["result"]:
#         return {"answer": "No matching data was found."}

#     prompt = RESPONSE_PROMPT.format(
#         question=state["question"],
#         result=state["result"]
#     )

#     response = llm.invoke(prompt)

#     return {"answer": response.content}




# def input_guardrail(state: AgentState):

#     question = state["question"].strip()

#     if not question:
#         return {
#             "error": "Please enter a question."
#         }

#     prompt_1 = f"""
# You are a classifier for a Text-to-SQL system.

# Determine whether the user's question is related to the database.

# Database contains e-commerce data about:
# - customers
# - products
# - orders
# - payments
# - reviews
# - shipments
# - suppliers

# User question:
# {question}

# Return ONLY one word:

# DATABASE
# or
# NOT_DATABASE
# """

#     response = llm.invoke(prompt_1)

#     classification = response.content.strip().upper()

#     if classification != "DATABASE":

#         return {
#             "error": (
#                 "This question is not related to the "
#                 "e-commerce database."
#             )
#         }

#     return {
#         "error": ""
#     }

# def check_input(state: AgentState):

#     if state.get("error"):
#         return "generate_response"

#     return "get_schema"


def input_guardrail(state: AgentState):
    question = state["question"].strip().lower()

    if not question:
        return {
            "error": "Please enter a question."
        }

    blocked_operations = [
        "delete",
        "drop",
        "update",
        "insert",
        "alter",
        "truncate",
        "create",
        "replace",
        "modify",
        "remove"
    ]

    for operation in blocked_operations:
        if operation in question:
            return {
                "error": (
                    "Only read-only database questions are allowed. "
                    f"The operation '{operation}' is not permitted."
                )
            }

    # Existing LLM-based database relevance check
    prompt = f"""
You are a classifier for a Text-to-SQL system.

Determine whether the user's question is related to the database.

Database contains e-commerce data about:
- customers
- products
- orders
- payments
- reviews
- shipments
- suppliers

User question:
{question}

Return ONLY one word:

DATABASE
or
NOT_DATABASE
"""

    response = llm.invoke(prompt)
    classification = response.content.strip().upper()

    if classification != "DATABASE":
        return {
            "error": (
                "This question is not related to the "
                "e-commerce database."
            )
        }

    return {"error": ""}

def check_input(state: AgentState):
    if state.get("error"):
        return "generate_response"

    return "get_schema"



def generate_response(state: AgentState):

    if state.get("error") and not state.get("result"):

        return {
            "answer": state["error"]
        }

    if not state["result"]:

        return {
            "answer": "No matching data was found."
        }

    prompt_2 = RESPONSE_PROMPT.format(
        question=state["question"],
        result=state["result"]
    )

    response = llm.invoke(prompt_2)

    return {
        "answer": response.content
    }








####### build nodes #######


graph_builder = StateGraph(AgentState)


graph_builder.add_node("input_guardrail",input_guardrail)
graph_builder.add_node("get_schema", get_database_schema)
graph_builder.add_node("generate_sql", generate_sql)
graph_builder.add_node("validate_sql", validate_sql)
graph_builder.add_node("execute_sql", execute_sql)
graph_builder.add_node("fix_sql", fix_sql)
graph_builder.add_node("generate_response", generate_response)



####### build edges for nodes #######

# Start
graph_builder.add_edge(START, "input_guardrail")


#conditional edges for input guardrail

graph_builder.add_conditional_edges(
    "input_guardrail",
    check_input,
    {
        "get_schema": "get_schema",
        "generate_response": "generate_response"
    }
)



# Schema → SQL
graph_builder.add_edge("get_schema", "generate_sql")

# SQL → validation
graph_builder.add_edge("generate_sql", "validate_sql")


# Validation routing
graph_builder.add_conditional_edges(
    "validate_sql",
    check_validation,
    {
        "fix_sql": "fix_sql",
        "execute_sql": "execute_sql",
        "generate_response": "generate_response"
    }
)


# Execution routing
graph_builder.add_conditional_edges(
    "execute_sql",
    check_execution,
    {
        "fix_sql": "fix_sql",
        "generate_response": "generate_response"
    }
)


# Fixed SQL goes through validation again
graph_builder.add_edge("fix_sql", "validate_sql")

# Final response
graph_builder.add_edge("generate_response", END)



graph = graph_builder.compile()