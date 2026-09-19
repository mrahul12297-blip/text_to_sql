# import streamlit as st

# from app.agent.graph import graph


# st.set_page_config(
#     page_title="Text-to-SQL Agent",
#     page_icon="🤖",
#     layout="wide"
# )

# st.title("🤖 Text-to-SQL Agent")
# st.write("Ask questions about your e-commerce database using natural language.")


# question = st.text_input(
#     "Ask your question",
#     placeholder="Example: Who are my top 5 customers?"
# )


# if st.button("Run Query"):

#     if not question:
#         st.warning("Please enter a question.")
#     else:
#         with st.spinner("Thinking..."):

#             result = graph.invoke({
#                 "question": question,
#                 "schema": {},
#                 "sql": "",
#                 "result": [],
#                 "answer": "",
#                 "error": "",
#                 "retry_count": 0
#             })

#         st.subheader("Generated SQL")
#         st.code(result["sql"], language="sql")

#         st.subheader("SQL Result")
#         st.dataframe(result["result"])

#         st.subheader("Answer")
#         st.write(result["answer"])



import streamlit as st

from app.agent.graph import graph
from app.database.sqlite import get_schema


st.set_page_config(
    page_title="Text-to-SQL Agent",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Text-to-SQL Agent")
st.write("Ask questions about your e-commerce database using natural language.")


# Initialize query history
if "query_history" not in st.session_state:
    st.session_state.query_history = []


# Get database schema
schema = get_schema()


# Sidebar
st.sidebar.title("📊 Database Schema")

for table_name, columns in schema.items():
    with st.sidebar.expander(f"📁 {table_name}"):
        for column in columns:
            st.write(f"• {column}")


st.sidebar.divider()

st.sidebar.title("🕘 Query History")

if st.session_state.query_history:

    for item in reversed(st.session_state.query_history):
        st.sidebar.write(f"• {item}")

else:
    st.sidebar.caption("No queries yet.")


# Main area
question = st.text_input(
    "Ask your question",
    placeholder="Example: Who are my top 5 customers?"
)


if st.button("Run Query"):

    if not question:
        st.warning("Please enter a question.")

    else:

        with st.spinner("Thinking..."):

            result = graph.invoke({
                "question": question,
                "schema": {},
                "sql": "",
                "result": [],
                "answer": "",
                "error": "",
                "retry_count": 0
            })

        # Add question to history
        st.session_state.query_history.append(question)

        st.subheader("Generated SQL")
        st.code(result["sql"], language="sql")

        st.subheader("SQL Result")

        if result["result"]:
            st.dataframe(
                result["result"],
                use_container_width=True
            )
        else:
            st.info("No matching data found.")

        st.subheader("Answer")
        st.write(result["answer"])