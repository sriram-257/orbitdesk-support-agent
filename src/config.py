"""
Configuration settings for the OrbitDesk Support Agent.
"""

from pathlib import Path

# ----------------------------
# Project Paths
# ----------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "data"
KB_DIR = DATA_DIR / "knowledge_base"

RESOLVED_CASES_PATH = DATA_DIR / "resolved_cases.json"
SAMPLE_QUESTIONS_PATH = DATA_DIR / "sample_questions.json"
OUTPUT_SCHEMA_PATH = DATA_DIR / "output_schema.json"

OUTPUT_DIR = PROJECT_ROOT / "outputs"
LOG_DIR = OUTPUT_DIR / "logs"
GRAPH_DIR = OUTPUT_DIR / "graph"
TEST_RESULTS_DIR = OUTPUT_DIR / "test_results"

# Create output folders if they don't exist
for directory in [OUTPUT_DIR, LOG_DIR, GRAPH_DIR, TEST_RESULTS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# ----------------------------
# Hugging Face Models
# ----------------------------

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

LLM_MODEL = "Qwen/Qwen2.5-1.5B-Instruct"

# ----------------------------
# Retrieval Settings
# ----------------------------

TOP_K = 3

MAX_RETRIES = 1

MAX_GENERATION_TOKENS = 512