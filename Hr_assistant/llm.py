""" step 6: connect to the llm (the "bain" of the assistant)"""

from langchain_groq import ChatGroq
from Hr_assistant import config

from Hr_assistant.logger import get_logger

logger = get_logger(__name__)

def get_llm():
    """return groq chat model. Reads Groq_api_key from the environment"""
    logger.info("Im initializing my LLM model '%s'", config.LLM_MODEL_NAME)
    return ChatGroq(model=config.LLM_MODEL_NAME, temperature=0)
