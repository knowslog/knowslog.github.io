import os
from dotenv import load_dotenv
load_dotenv()


def get_model(platform,config:dict):
    if platform=="OpenAI":
        from langchain_openai import ChatOpenAI
        chat_model = ChatOpenAI(**config)
        
    return chat_model

def read_markdown_file(filename):
    with open(filename, 'r') as file:
        content = file.read()
    return content

def markdown_to_documents(markdown_path):
    from langchain_community.document_loaders import UnstructuredMarkdownLoader
    loader = UnstructuredMarkdownLoader(markdown_path)
    data = loader.load()
    return data

base_path = "medium/origin_md/"
file_name = "2024-05-04-The_future_is_Agentic_—_crewAI._Easily_creating_Agentic_Workflows_with…__by_Gabriel_Rennó__Apr,_2024__Medium.md"

markdown_content = read_markdown_file(base_path+file_name)

print(markdown_content)

chat_model = get_model("OpenAI",{"model":"gpt-4-turbo",
                                 "temperature":0.1})

print(chat_model.invoke("hi"))