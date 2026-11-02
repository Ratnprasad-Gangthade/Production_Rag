""" step 6: connect to the llm (the "bain" of the assistant)"""

from Hr_assistant.gateway import get_gateway_llm

from Hr_assistant.logger import get_logger

logger = get_logger(__name__)

def get_llm():
    """return groq chat model. Reads Groq_api_key from the environment"""
    logger.info("Im initializing llm via portkey Gateway")
    return get_gateway_llm()
