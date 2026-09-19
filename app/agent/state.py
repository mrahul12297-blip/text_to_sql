from typing import TypedDict


class AgentState(TypedDict):
    question: str
    schema: dict
    sql: str
    result: list
    answer: str
    error: str
