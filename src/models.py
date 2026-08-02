from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    pipeline,
)

from sentence_transformers import SentenceTransformer

from src.config import (
    LLM_MODEL,
    EMBEDDING_MODEL,
)

print("Loading embedding model...")
embedding_model = SentenceTransformer(EMBEDDING_MODEL)

print("Loading tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(LLM_MODEL)

print("Loading LLM...")
model = AutoModelForCausalLM.from_pretrained(
    LLM_MODEL,
    trust_remote_code=True,
)

# Remove Qwen's default max_length
model.generation_config.max_length = None

generator = pipeline(
    task="text-generation",
    model=model,
    tokenizer=tokenizer,
)

print("Models loaded successfully.")