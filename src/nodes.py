"""
LangGraph nodes for the OrbitDesk Support Agent.
"""

from src.models import generator
from src.retriever import Retriever

retriever = Retriever()


# ==========================================================
# TRIAGE NODE
# ==========================================================

def triage_node(state):
    """
    Classify the user's request.
    """

    question = state["question"]
    question_lower = question.lower()

    # ------------------------------------------------------
    # OrbitDesk keywords
    # ------------------------------------------------------

    orbitdesk_keywords = [
        "orbitdesk",
        "api",
        "credential",
        "credentials",
        "workspace",
        "workspaces",
        "permission",
        "permissions",
        "role",
        "roles",
        "audit",
        "audit log",
        "export",
        "exports",
        "delivery",
        "destination",
        "connection",
        "connections",
        "refresh",
        "integration",
        "dataset",
        "schedule",
    ]

    # ------------------------------------------------------
    # Clarification keywords
    # ------------------------------------------------------

    vague_keywords = [
        "not working",
        "it is not working",
        "problem",
        "issue",
        "error",
        "help",
        "doesn't work",
        "does not work",
        "broken",
    ]

    # ------------------------------------------------------
    # Escalation keywords
    # ------------------------------------------------------

    escalation_keywords = [
        "delete my account",
        "refund",
        "billing",
        "payment",
        "cancel subscription",
        "human",
        "support agent",
        "complaint",
    ]

    # ------------------------------------------------------
    # Fast rule-based classification
    # ------------------------------------------------------

    if any(word in question_lower for word in orbitdesk_keywords):
        state["classification"] = "answerable"
        return state

    if any(word in question_lower for word in vague_keywords):
        state["classification"] = "clarification"
        return state

    if any(word in question_lower for word in escalation_keywords):
        state["classification"] = "escalation"
        return state

    # ------------------------------------------------------
    # LLM classification (fallback)
    # ------------------------------------------------------

    prompt = f"""
Classify the user's request into ONLY one category.

Categories:

answerable
clarification
escalation
out_of_scope

Question:
{question}

Return ONLY the category.
"""

    response = generator(
        prompt,
        max_new_tokens=10,
        do_sample=False,
        return_full_text=False,
        clean_up_tokenization_spaces=False,
    )

    classification = response[0]["generated_text"].strip().lower()

    valid = {
        "answerable",
        "clarification",
        "escalation",
        "out_of_scope",
    }

    if classification not in valid:
        classification = "out_of_scope"

    state["classification"] = classification

    return state


# ==========================================================
# RETRIEVE NODE
# ==========================================================

def retrieve_node(state):
    """
    Retrieve relevant documents.
    """

    question = state["question"]

    docs = retriever.search(question)

    state["retrieved_docs"] = docs

    return state


# ==========================================================
# GENERATE NODE
# ==========================================================

def generate_node(state):
    """
    Generate answer using retrieved documents.
    """

    context = "\n\n".join(
        doc.page_content[:700]
        for doc in state["retrieved_docs"]
    )

    prompt = f"""
You are OrbitDesk's AI Support Assistant.

Answer ONLY using the information provided in the context.

If the answer is not available in the context, reply exactly:

I don't have enough information from the knowledge base.

Context:
{context}

Question:
{state["question"]}

Answer:
"""

    response = generator(
        prompt,
        max_new_tokens=180,
        do_sample=False,
        return_full_text=False,
        clean_up_tokenization_spaces=False,
    )

    state["answer"] = response[0]["generated_text"].strip()

    return state


# ==========================================================
# VERIFY NODE
# ==========================================================

def verify_node(state):
    """
    Verify the generated answer.
    """

    answer = state["answer"]

    if (
        not answer.strip()
        or "I don't have enough information" in answer
    ):
        state["verified"] = False
    else:
        state["verified"] = True

    return state