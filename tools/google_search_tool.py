from langchain_core.tools import tool
import requests
from dotenv import load_dotenv
import os

load_dotenv('.env')

@tool
def google_search_api(query: str) -> dict:
    """
    Perform a Google search using the Custom Search JSON API.

    Args:
        query (str): The search query string.

    Returns:
        dict: The JSON response from the Google Custom Search API.
    """

    api_key = os.getenv("GOOGLESEARCH_API_KEY")
    cx_key = os.getenv("CX_GOOGLESEARCH_KEY")

    if not api_key or not cx_key:
        return {"error": "API_KEY or CX not configured in environment variables"}
    
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        'key': api_key,
        'cx': cx_key,
        'q': query 
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {str(e)}"}