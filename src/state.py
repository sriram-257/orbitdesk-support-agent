from typing import TypedDict
from langchain_core.documents import Document


class AgentState(TypedDict):
    question: str
    classification: str
    retrieved_docs: list[Document]
    answer: str
    verified: bool
    retry_count: int