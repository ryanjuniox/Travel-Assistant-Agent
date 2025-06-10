# Agent Guide

## Definição de Arestas e Nós


```python
# Definir os componentes (nós)
graph.add_node("model", call_model)            # Componente que chama o LLM
graph.add_node("tool_router", call_tools)      # Componente que decide o próximo passo
graph.add_node("tool_executor", tool_node)     # Componente que executa ferramentas

# Definir o fluxo (arestas)
graph.add_edge("model", "tool_router")                       # Modelo → Router (sempre)
graph.add_edge("tool_router", "tool_executor", condition="tools")  # Se retornar "tools"
graph.add_edge("tool_executor", "model")                     # Volta para o modelo
```
