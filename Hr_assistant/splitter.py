""" step 2: split the document into the smaller chunks for better searchability"""

from langchain_text_splitters import RecursiveCharacterTextSplitter
from Hr_assistant import config

def split_into_chunks(documents):
    """ spli the docuemnt into smaller parts for better searchablility """
    splitter=RecursiveCharacterTextSplitter(
        chunk_size=config.CHUNK_SIZE,
        chunk_overlap=config.CHUNK_OVERLAP
    )

    return splitter.split_documents(documents=config.DATA_FILE_PATH)

print("document splitted")