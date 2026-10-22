""" step 4: store chunks into the FAISS vectore database """
import os
from langchain_community.vectorstores import FAISS

from Hr_assistant import config
from Hr_assistant.embeddings import get_embedding_model

def build_vector_store(chunks):
    """ embedded every chunk and 
    store into the FAISS serachable index in memory """
    embedding_model=get_embedding_model()
    return FAISS.from_documents(chunks, embedding_model)

def save_vector_store(vector_store, path: str=config.VECTOR_STORE_PATH )-> None:
    """"""
    vector_store.save_local(path)


