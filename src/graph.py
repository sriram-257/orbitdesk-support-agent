"""
LangGraph workflow definition.
"""

from langgraph.graph import StateGraph, END

from src.state import AgentState
from src.nodes import (
    triage_node,
    retrieve_node,
    generate_node,
    verify_node,
)


def triage_router(state: AgentState):
    """
    Route after triage.
    """

    classification = state["classification"]

    if classification == "answerable":
        return "retrieve"

    return END


def verify_router(state: AgentState):
    """
    Retry generation once if verification fails.
    """

    if state["verified"]:
        return END

    if state["retry_count"] < 1:
        state["retry_count"] += 1
        return "generate"

    return END


builder = StateGraph(AgentState)

# -----------------------------
# Nodes
# -----------------------------

builder.add_node("triage", triage_node)
builder.add_node("retrieve", retrieve_node)
builder.add_node("generate", generate_node)
builder.add_node("verify", verify_node)

# -----------------------------
# Entry Point
# -----------------------------

builder.set_entry_point("triage")

# -----------------------------
# Routing
# -----------------------------

builder.add_conditional_edges(
    "triage",
    triage_router,
)

builder.add_edge("retrieve", "generate")

builder.add_edge("generate", "verify")

builder.add_conditional_edges(
    "verify",
    verify_router,
)

graph = builder.compile()