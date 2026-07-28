from dotenv import load_dotenv
from langchain_tavily import TavilySearch

load_dotenv

tool_tavily_search = TavilySearch(max_results=5)
tools = [tool_tavily_search]
