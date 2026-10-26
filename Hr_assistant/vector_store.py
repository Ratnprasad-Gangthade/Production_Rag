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
    """save  the FAISS idex to disk 
     so we dont have to rebuild it every time. """
    vector_store.save_local(path)

def load_vector_store(path : str = config.VECTOR_STORE_PATH):
    """ load a priviously saved FAISS index from disk. """
    embeddings_model= get_embedding_model()
    # allow_dangerous_deserialization is safe here because we only ever load 
    # an index that this same app created and saved 
    return FAISS.load_local(path , embeddings_model, allow_dangerous_deserialization=True)

def vector_store_exists(path : str= config.VECTOR_STORE_PATH) -> bool :
    """ check if a saved FAISS index already exists on disk. """
    return os.path.exists(os.path.join(path, "index.faiss")) 

def get_retriever(vector_store , k: int= config.TOP_K_RESULTS):
    """Turn a vector store into  retriever that returns the top-k mtching chunks. """
    return vector_store.as_retriever(search_kwargs={"k": k})