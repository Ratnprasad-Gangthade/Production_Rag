""" step 6: connect to the llm (the "bain" of the assistant)"""

from langchain_groq import ChatGroq
from Hr_assistant import config

def get_llm():
    """return groq chat model. Reads Groq_api_key from the environment"""
    return ChatGroq(model=config.LLM_MODEL_NAME, temperature=0)
