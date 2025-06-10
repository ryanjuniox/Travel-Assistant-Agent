import sys
import os
from typing import Literal
from langgraph.prebuilt import ToolNode
from langgraph.graph import StateGraph, MessagesState, START, END
from langchain_openai import ChatOpenAI

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from tools.google_search_tool import google_search_api

openai_api_key = os.getenv("OPENAI_API_KEY")

tools = [google_search_api]

# Um Runnable LangChain que recebe o estado do gráfico (que inclui uma lista de mensagens) e produz um estado atualizado com as chamadas de ferramenta.
tool_node = ToolNode(tools)

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, api_key=openai_api_key)
llm_with_tools = llm.bind_tools(tools)

# Função para chamar o modelo
def call_model(state: MessagesState):
    messages = state['messages']
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

# Função para chamar as ferramentas
def call_tools(state: MessagesState) -> Literal["tools", END]:
    messages = state["messages"]
    last_message = messages[-1] # Obtém a mensagem mais recente
    if last_message.tool_calls:
        return "tools" # Identifica que a mensagem é uma chamada de ferramenta
    return END

# Inicializnado o Workflow com StateGraph
workflow = StateGraph(MessagesState)

workflow.add_node("LLM", call_model) # Este nó usa uma LLM para fazer decisões baseadas no input
workflow.add_node("tools", tool_node) # ToolNode

workflow.add_edge(START, "LLM") # O workflow inicia com a chamada de LLM
workflow.add_conditional_edges("LLM", call_tools) # Será encaminhado para o tool_node dependendo da saída da LLM
workflow.add_edge("tools", "LLM")

agent = workflow.compile()

for chunk in agent.stream({"messages": [("user", "Clima no Japão agora?")]}, stream_mode="values"):
    chunk["messages"][-1].pretty_print()
