""" step 7 : build the agent that tries the llm and search tool together"""
from langchain.agents import create_agent
from Hr_assistant import config

def create_hr_agent(llm, tools):
    """ Return a langchain agent that can  
    call our tool to answer query """
    return create_agent(model=llm , 
                        tools=tools, system_prompt=config.SYSTEM_PROMPT)