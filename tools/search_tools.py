from dotenv import load_dotenv
from langchain_community.tools import BraveSearch
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_tavily import TavilySearch
from langchain_core.tools import tool

load_dotenv()

TAVILY_SEARCH = TavilySearch(max_results=3, search_depth="basic")

BRAVE_SEARCH = BraveSearch()

DUCK_DUCK_GO_SEARCH = DuckDuckGoSearchRun()



