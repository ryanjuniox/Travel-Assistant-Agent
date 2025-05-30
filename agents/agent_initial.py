import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from tools.google_search_tool import google_search_api

load_dotenv('.env')

openai_api_key = os.getenv("OPENAI_API_KEY")

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
