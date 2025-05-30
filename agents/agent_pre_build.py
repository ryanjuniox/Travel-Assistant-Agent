from  langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
from tools import google_search_api

load_dotenv('.env')
openai_api_key = os.getenv("OPENAI_API_KEY")

def print_response(response):
    print(response["messages"][-1].content)

system_prompt = """You are a travel research agent with access to Google Search.

When users ask for ANY information that requires current data (weather, flights, hotels, etc.), 
you MUST use the google_search_api tool.

Available tools:
- google_search_api: Use this to search for any information on Google

Example: If user asks "What is the weather in Tokyo?", search for "Tokyo weather current"

Always use the tool before saying you cannot find information.
"""

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, api_key=openai_api_key)
tools = [google_search_api]

agent = create_react_agent(model=llm, tools=tools, prompt=system_prompt)

input_message = {"messages": [("user", "What is the weather in Tokyo?")]}
print_response(agent.invoke(input_message))