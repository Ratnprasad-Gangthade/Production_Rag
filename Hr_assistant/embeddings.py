
"""Step 3: Convert raw text into numerical embeddings."""

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from Hr_assistant import config


def get_embedding_model():
    """Return the Google embedding model.
    
    Reads the API key from the environment.
    """
    return GoogleGenerativeAIEmbeddings(
        model=config.EMBEDDING_MODEL_NAME
    )
