import os
import requests
from typing import List, Literal
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from urllib.parse import quote_plus

load_dotenv('.env')

search_google_web_key = os.getenv("GOOGLESEARCH_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")
cx_key = os.getenv("CX_KEY")

@tool
def google_search_api(query: str, api_key: str) -> dict:
    """
    Perform a Google search using the Custom Search JSON API.

    Args:
        query (str): The search query string.
        api_key (str): The API key for authenticating the request.

    Returns:
        dict: The JSON response from the Google Custom Search API.
    """
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        'key': api_key,
        'cx': cx_key,
        'q': query
    }
    response = requests.get(url, params=params)
    return response.json()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, api_key=openai_api_key)

tools = [google_search_api]

llm_with_tools = llm.bind_tools(tools)

prompt = """
1. Você é um agente de busca de informações.
2. Dadas apenas as ferramentas à sua disposição, mencione as chamadas de ferramentas para as seguintes tarefas: 
3.Não altere a consulta fornecida para nenhuma tarefa de pesquisa
4.Você deve usar a ferramenta de busca do Google para buscar informações.
"""

results = llm_with_tools.invoke(prompt)
print(results.tool_calls)

query = "Qual a receita de bolo de chocolate?"
response = llm.invoke(query)
print(response.content)
