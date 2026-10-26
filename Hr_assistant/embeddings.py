
"""Step 3: Convert raw text into numerical embeddings."""

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from Hr_assistant import config
from Hr_assistant.logger import get_logger

logger = get_logger(__name__)


def get_embedding_model():
    """Return the Google embedding model.
    
    Reads the API key from the environment.
    """
    logger.info("Initializing embeddings model '%s'", config.EMBEDDING_MODEL_NAME)
    return GoogleGenerativeAIEmbeddings(
        model=config.EMBEDDING_MODEL_NAME
    )
