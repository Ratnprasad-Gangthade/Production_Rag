""" Read the raw document from the data folder."""

from langchain_community.document_loaders import TextLoader
from Hr_assistant import config

def load_document(file_path: str= config.DATA_FILE_PATH):
    """load a .txt file and return it as a list of langchain document"""
    loader=TextLoader(file_path , encoding="utf-8")
    return loader.load()

print("docuemnt loaded")