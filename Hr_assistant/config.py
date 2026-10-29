"""All settings for the app live here, in one place."""


import os 
from dotenv import load_dotenv

load_dotenv(override=True)

## ENV VAR / SECRET - LLMS 

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

## DEFINE PATH - DATA / VECTOR STORE 

DATA_FILE_PATH = os.path.join("data", "hr_policy.txt")

VECTOR_STORE_PATH=os.path.join("data", "faiss_index")

# cloud vector db
QDRANT_API_KEY=os.getenv("QDRANT_API_KEY")
QDRANT_URL= os.getenv("QDRANT_URL")

QDRANT_COLLECTION_NAME=os.getenv("QDRANT_COLLECTION_NAME", "hr_policy")


## MODELS 
LLM_MODEL_NAME = "openai/gpt-oss-20b"

# LLM and EMBEDING MODEL 
EMBEDDING_MODEL_NAME = "gemini-embedding-2"

# GUARD MODEL 
GUARD_MODEL_NAME = "openai/gpt-oss-safeguard-20b"

## CHUNK / TEXT SPLITTING CONFIG 

CHUNK_SIZE = 500
CHUNK_OVERLAP = 60

# RETRIVAL RESULTS 
TOP_K_RESULTS = 3


## SYSTEM INSTRUCTIONS 

SYSTEM_PROMPT = (
    "You are a friendly HR assistant. Always use the search_hr_policy tool to look up "
    "facts before answering. If the answer isn't in the search results, say you don't know "
    "instead of guessing."
)

def check_api_keys() -> None:
    """Stop early with a clear message if a required API key is missing."""
    if not GROQ_API_KEY:
        raise ValueError("Missing GROQ_API_KEY. Please add it to your .env file.")
    if not GOOGLE_API_KEY:
        raise ValueError("Missing GOOGLE_API_KEY. Please add it to your .env file.")