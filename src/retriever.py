"""
Retriever module for the OrbitDesk Support Agent.
Builds a FAISS vector index from the knowledge base and resolved cases.
"""

import json

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

from src.config import (
    KB_DIR,
    RESOLVED_CASES_PATH,
    EMBEDDING_MODEL,
    TOP_K,
)


class Retriever:
    def __init__(self):
        self.embedding = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL
        )

        self.documents = []
        self.vectorstore = None

        self.load_knowledge_base()
        self.build_index()

    def load_knowledge_base(self):
        """Load markdown files and resolved cases."""

        # ----------------------------
        # Load Markdown Knowledge Base
        # ----------------------------
        for file in sorted(KB_DIR.glob("*.md")):
            text = file.read_text(encoding="utf-8")

            self.documents.append(
                Document(
                    page_content=text,
                    metadata={
                        "source": file.name,
                        "type": "knowledge_base",
                    },
                )
            )

        # ----------------------------
        # Load Resolved Cases
        # ----------------------------
        with open(RESOLVED_CASES_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)

        cases = data["cases"]

        for case in cases:

            # Skip superseded cases if the field exists
            if case.get("superseded", False):
                continue

            text = json.dumps(case, indent=2)

            self.documents.append(
                Document(
                    page_content=text,
                    metadata={
                        "source": "resolved_cases.json",
                        "case_id": case.get("id", ""),
                        "type": "resolved_case",
                    },
                )
            )

    def build_index(self):
        """Create FAISS vector index."""

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100,
        )

        chunks = splitter.split_documents(self.documents)

        self.vectorstore = FAISS.from_documents(
            chunks,
            self.embedding,
        )

    def search(self, query):
        """Return top-k similar documents."""

        return self.vectorstore.similarity_search(
            query,
            k=TOP_K,
        )