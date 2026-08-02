"""
Main application for the OrbitDesk Support Agent.
"""

import json
from pathlib import Path

from src.graph import graph

LOG_FILE = Path("outputs/logs/chat_log.json")


def main():
    print("=" * 60)
    print("OrbitDesk AI Support Agent")
    print("Type 'exit' to quit")
    print("=" * 60)

    while True:

        question = input("\nUser: ")

        if question.lower() == "exit":
            print("\nGoodbye!")
            break

        state = {
            "question": question,
            "classification": "",
            "retrieved_docs": [],
            "answer": "",
            "verified": False,
            "retry_count": 0,
        }

        result = graph.invoke(state)

        print(f"\nClassification: {result['classification']}")

        # ----------------------------------------
        # Handle non-answerable requests
        # ----------------------------------------

        if result["classification"] == "clarification":
            result["answer"] = (
                "Could you please provide more details so I can assist you?"
            )

        elif result["classification"] == "escalation":
            result["answer"] = (
                "This request should be escalated to a human support representative."
            )

        elif result["classification"] == "out_of_scope":
            result["answer"] = (
                "This question is outside the OrbitDesk knowledge base."
            )

        # ----------------------------------------
        # Display sources only for answerable
        # ----------------------------------------

        sources = []

        if result["classification"] == "answerable":

            print("\nSources:")

            sources = sorted({
                doc.metadata["source"]
                for doc in result["retrieved_docs"]
            })

            for source in sources:
                print(f"- {source}")

        # ----------------------------------------
        # Assistant Response
        # ----------------------------------------

        print("\nAssistant:\n")
        print(result["answer"])

        # ----------------------------------------
        # Save Conversation Log
        # ----------------------------------------

        entry = {
            "question": question,
            "classification": result["classification"],
            "answer": result["answer"],
            "sources": sources,
            "verified": result["verified"],
        }

        if LOG_FILE.exists():
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                try:
                    logs = json.load(f)
                except json.JSONDecodeError:
                    logs = []
        else:
            logs = []

        logs.append(entry)

        with open(LOG_FILE, "w", encoding="utf-8") as f:
            json.dump(logs, f, indent=4)

        print("\n" + "=" * 60)


if __name__ == "__main__":
    main()