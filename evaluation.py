print("Evaluation started...", flush=True)

import time
from app.agent.graph import graph


# ============================================================
# TEST DATASET
# ============================================================

TEST_CASES = [
    {
        "question": "What are the names of the products?",
        "expected_sql_contains": ["products", "product_name"],
    },
    {
        "question": "Who are my top 5 customers by spending?",
        "expected_sql_contains": [
            "customers",
            "orders",
            "SUM",
            "ORDER BY",
            "LIMIT"
        ],
    },
    {
        "question": "Which product has the highest average rating?",
        "expected_sql_contains": [
            "products",
            "reviews",
            "AVG",
            "ORDER BY"
        ],
    },
    {
        "question": "What was the maximum number of orders in one day?",
        "expected_sql_contains": [
            "orders",
            "COUNT",
            "GROUP BY"
        ],
    },
    {
        "question": "Which suppliers provide the most products?",
        "expected_sql_contains": [
            "suppliers",
            "products",
            "COUNT"
        ],
    },
]


# ============================================================
# RUN ONE TEST
# ============================================================

def run_test(question):
    start_time = time.time()

    result = graph.invoke({
        "question": question,
        "schema": {},
        "sql": "",
        "result": [],
        "answer": "",
        "error": "",
        "retry_count": 0
    })

    end_time = time.time()

    latency = end_time - start_time

    return result, latency


# ============================================================
# SQL VALIDITY
# ============================================================

def check_sql_validity(result):
    sql = result.get("sql", "").strip()

    if not sql:
        return False

    sql_lower = sql.lower()

    # Must be SELECT
    if not sql_lower.startswith("select"):
        return False

    # Block dangerous operations
    blocked_words = [
        "insert",
        "update",
        "delete",
        "drop",
        "alter",
        "create",
        "truncate",
        "replace",
        "attach",
        "detach"
    ]

    for word in blocked_words:
        if word in sql_lower:
            return False

    return True


# ============================================================
# SCHEMA ACCURACY
# ============================================================

def check_schema_accuracy(result, expected_sql_contains):
    sql = result.get("sql", "").lower()

    if not sql:
        return False

    for item in expected_sql_contains:
        if item.lower() not in sql:
            return False

    return True


# ============================================================
# RESULT CHECK
# ============================================================

def check_result(result):
    error = result.get("error", "")

    if error:
        return False

    return True


# ============================================================
# EVALUATION
# ============================================================

def evaluate_agent():

    total = len(TEST_CASES)

    sql_valid_count = 0
    schema_correct_count = 0
    execution_success_count = 0
    task_success_count = 0

    total_latency = 0

    print("\n" + "=" * 70)
    print("TEXT-TO-SQL AGENT EVALUATION")
    print("=" * 70)

    for index, test_case in enumerate(TEST_CASES, start=1):

        question = test_case["question"]

        print(f"\nTest {index}")
        print("-" * 70)
        print("Question:", question)

        result, latency = run_test(question)

        total_latency += latency

        sql = result.get("sql", "")
        error = result.get("error", "")
        answer = result.get("answer", "")

        # -----------------------------------------
        # 1. SQL VALIDITY
        # -----------------------------------------

        sql_valid = check_sql_validity(result)

        if sql_valid:
            sql_valid_count += 1

        # -----------------------------------------
        # 2. SCHEMA ACCURACY
        # -----------------------------------------

        schema_correct = check_schema_accuracy(
            result,
            test_case["expected_sql_contains"]
        )

        if schema_correct:
            schema_correct_count += 1

        # -----------------------------------------
        # 3. EXECUTION SUCCESS
        # -----------------------------------------

        execution_success = check_result(result)

        if execution_success:
            execution_success_count += 1

        # -----------------------------------------
        # 4. TASK SUCCESS
        # -----------------------------------------

        # For this simple evaluation:
        # SQL must be valid + schema must be correct
        # + execution must succeed.

        task_success = (
            sql_valid
            and schema_correct
            and execution_success
        )

        if task_success:
            task_success_count += 1

        # -----------------------------------------
        # PRINT RESULTS
        # -----------------------------------------

        print("\nGenerated SQL:")
        print(sql)

        print("\nAnswer:")
        print(answer)

        if error:
            print("\nError:")
            print(error)

        print("\nMetrics:")
        print("SQL Valid:", sql_valid)
        print("Schema Correct:", schema_correct)
        print("Execution Successful:", execution_success)
        print("Task Successful:", task_success)
        print("Latency:", round(latency, 2), "seconds")

    # ========================================================
    # FINAL METRICS
    # ========================================================

    sql_validity_rate = (
        sql_valid_count / total
    ) * 100

    schema_accuracy = (
        schema_correct_count / total
    ) * 100

    execution_accuracy = (
        execution_success_count / total
    ) * 100

    task_success_rate = (
        task_success_count / total
    ) * 100

    average_latency = (
        total_latency / total
    )

    # ========================================================
    # PRINT FINAL REPORT
    # ========================================================

    print("\n" + "=" * 70)
    print("FINAL EVALUATION REPORT")
    print("=" * 70)

    print(f"\nTotal Test Cases       : {total}")

    print(
        f"SQL Validity Rate     : "
        f"{sql_validity_rate:.2f}%"
    )

    print(
        f"Schema Accuracy       : "
        f"{schema_accuracy:.2f}%"
    )

    print(
        f"Execution Accuracy    : "
        f"{execution_accuracy:.2f}%"
    )

    print(
        f"Task Success Rate     : "
        f"{task_success_rate:.2f}%"
    )

    print(
        f"Average Latency       : "
        f"{average_latency:.2f} seconds"
    )

    print("\n" + "=" * 70)


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    evaluate_agent()
