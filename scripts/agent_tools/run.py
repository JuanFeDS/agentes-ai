"""Script para ejecutar el agente"""
from tavily import create_tavily_tool
from retriever import create_web_retriever_tool
from tools import manage_tools

def run():
    """Entry point for running the program."""
    # tavily_tool = create_tavily_tool()
    # response = tavily_tool('Qué es nano banana?')

    # url = response['results'][0]['url']
    # print(url)

    # result = create_web_retriever_tool(url)
    # print(result)

    tools = manage_tools()
    print(tools)

if __name__ == '__main__':
    run()
