from langchain_core.tools import Tool
from langchain_experimental.utilities import PythonREPL
from langchain_core.tools import tool
from langchain_community.utilities import StackExchangeAPIWrapper
from langchain_community.utilities.wolfram_alpha import WolframAlphaAPIWrapper
from dotenv import load_dotenv

load_dotenv()

stackexchange = StackExchangeAPIWrapper()

STACKEXCHANGE_TOOL = Tool(
    name="Stackexchange",
    description="Stack Exchange tool retrieves community-driven Q&A content from sites like Stack Overflow, offering expert insights on technical and academic topics.",
    func=stackexchange.run
)


python_repl = PythonREPL()

# You can create the tool to pass to an agent
REPL_TOOL = Tool(
    name="python_repl",
    description="A Python shell. Use this to execute python commands. Input should be a valid python command. If you want to see the output of a value, you should print it out with `print(...)`.",
    func=python_repl.run,
)


wolfram = WolframAlphaAPIWrapper()

WOLFRAM_TOOL = Tool(
    name="wolfram",
    description="Wolfram Alpha tool performs step-by-step computations and returns structured, factual data across domains like math, science, and more.",
    func=wolfram.run
)
