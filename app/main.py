from app.agent.graph import graph

question = input("Ask your question: ")

result = graph.invoke({
    "question": question,
    "schema": {},
    "sql": "",
    "result": [],
    "answer": "",
    "error": "",
    "retry_count": 0
})

print("\nGenerated SQL:")
print(result["sql"])

print("\nSQL Result:")
print(result["result"])

print("\nAnswer:")
print(result["answer"])

