""" write all the components together into one ready-to-use agent.

 this is the eingle entry point thst msin.py (CLI) and app.py (streamlit)
 both call . each step is handled by its own samll module."""

from Hr_assistant import config
from Hr_assistant.agent import create_hr_agent      
from Hr_assistant.document_loader import load_document
from Hr_assistant.llm import get_llm
from Hr_assistant.splitter import split_into_chunks
from Hr_assistant.tools import create_search_tool
from Hr_assistant.vector_store import ( 
    build_vector_store,
    get_retriever,
    load_vector_store,
    save_vector_store,
    vector_store_exists)

from Hr_assistant.logger import get_logger
logger = get_logger(__name__)


 
def build_vector_store_for_document(file_path: str= config.DATA_FILE_PATH):
    """load + split + embed the docuemnt , reusing a saved index if we have one. """
    if vector_store_exists():

        print("found a saved vector store on disk, loading it ( fast , no re-embedding.)")
        logger.info("vector store already exist in the disk reusing it ")
        return load_vector_store()

    print("No saved vector store found, building one from scratch...") 
    logger.info("No vector store on disk , building one from scratch ")
    documents= load_document(file_path)
    chunks=split_into_chunks(documents)
    print(f"Loaded '{file_path}' and split it into {len(chunks)} chunks.")


    vector_store = build_vector_store(chunks)
    save_vector_store(vector_store)
    print("Vector store built and saved to disk for next time.")
    return vector_store

def build_hr_assistant(file_path: str = config.DATA_FILE_PATH):
    """Build the full RAG agent, ready to answer questions."""
    logger.info("Building Hr assistant ")
    config.check_api_keys()

    vector_store = build_vector_store_for_document(file_path)
    retriever= get_retriever(vector_store)
    search_tool = create_search_tool(retriever)

    llm= get_llm()
    agent= create_hr_agent(llm , [search_tool])
    logger.info("Hr assistant is ready to tak questions")
    return agent

def ask(agent, question: str ) -> str:
    """Ask the agent a question and 
    return its final answer as plain text. """
    logger.info("user question '%s' " , question)
    response = agent.invoke({"messages":[{"role" : "user", "content":question}]}) 
    answer= response["messages"][-1].content
    logger.info("Final answer : '%s' ", answer)
    return answer 