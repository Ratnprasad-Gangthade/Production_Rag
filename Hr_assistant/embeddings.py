"""step 3 : convert raw text into the numerical format/ embedding """

from langchain_google_genai import GoogleGenerativeAIEmbedding
from Hr_assistant import config


def get_embedding_model():
    """ return the google embedding model 
    Reads the API key from the environment """
    return GoogleGenerativeAIEmbedding(model_name=config.EMBEDDING_MODEL_NAME)